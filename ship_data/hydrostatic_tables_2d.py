"""
二维静水力表数据解析和查询模块
从data.txt中解析完整的静水力表数据（draught × trim）

包含的表格：
- Total displacement (t)
- Transverse metacentric height KM (m)
- LCB (m)
- VCB/KB (m)
等
"""

import numpy as np
from scipy import interpolate
import os

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.txt')

# 全局变量存储解析后的数据
_DRAUGHTS = None
_TRIMS = None
_DISP_TABLE = None
_KM_TABLE = None
_LCB_TABLE = None
_VCB_TABLE = None

def _parse_table_from_file(start_marker: str, num_rows: int = 57) -> tuple:
    """
    从data.txt中解析一个二维表格
    
    Args:
        start_marker: 表格的标识字符串（如 "total displacement"）
        num_rows: 数据行数（默认57行吃水数据）
    
    Returns:
        (draughts, trims, data_table)
    """
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 查找表格起始位置
    start_line = None
    for i, line in enumerate(lines):
        if start_marker.lower() in line.lower():
            start_line = i
            break
    
    if start_line is None:
        raise ValueError(f"找不到表格标识: {start_marker}")
    
    # 解析trim行（表头）
    trim_line = None
    for i in range(start_line, min(start_line + 10, len(lines))):
        if 'trim' in lines[i].lower():
            trim_line = i
            break
    
    if trim_line is None:
        raise ValueError(f"找不到trim行")
    
    # 提取trim值
    trim_parts = lines[trim_line].split()
    trim_idx = trim_parts.index('trim') if 'trim' in trim_parts else 0
    trims = [float(x) for x in trim_parts[trim_idx+1:]]
    
    # 解析数据行
    draughts = []
    data_rows = []
    
    data_start = trim_line + 2  # 跳过trim行和draught标题行
    for i in range(data_start, min(data_start + num_rows, len(lines))):
        line = lines[i].strip()
        if not line or line.startswith('-'):
            continue
        
        parts = line.split()
        if len(parts) < 2:
            continue
        
        try:
            draught = float(parts[0])
            values = [float(x) for x in parts[1:1+len(trims)]]
            
            draughts.append(draught)
            data_rows.append(values)
        except (ValueError, IndexError):
            continue
    
    draughts = np.array(draughts)
    trims = np.array(trims)
    data_table = np.array(data_rows)
    
    return draughts, trims, data_table


def _load_tables():
    """加载所有静水力表数据"""
    global _DRAUGHTS, _TRIMS, _DISP_TABLE, _KM_TABLE, _LCB_TABLE, _VCB_TABLE
    
    if _DISP_TABLE is not None:
        return  # 已经加载过了
    
    # 解析DISP表
    _DRAUGHTS, _TRIMS, _DISP_TABLE = _parse_table_from_file("total displacement")
    
    # 解析KM表
    _, _, _KM_TABLE = _parse_table_from_file("transv. metac. height")
    
    # 解析LCB表
    try:
        _, _, _LCB_TABLE = _parse_table_from_file("long. centre buoyancy")
    except:
        _LCB_TABLE = None
    
    # 解析VCB表
    try:
        _, _, _VCB_TABLE = _parse_table_from_file("vert. centre buoyancy")
    except:
        _VCB_TABLE = None
    
    print(f"✓ 已加载静水力表数据:")
    print(f"  - 吃水范围: {_DRAUGHTS[0]:.2f} ~ {_DRAUGHTS[-1]:.2f} m ({len(_DRAUGHTS)}个点)")
    print(f"  - 纵倾范围: {_TRIMS[0]:.2f} ~ {_TRIMS[-1]:.2f} m ({len(_TRIMS)}个点)")
    print(f"  - DISP表: {_DISP_TABLE.shape}")
    print(f"  - KM表: {_KM_TABLE.shape}")


def get_displacement_at_draught(draught: float, trim: float = 0.0) -> float:
    """
    根据吃水和纵倾查询排水量
    
    Args:
        draught: 平均吃水 (m)
        trim: 纵倾 (m, 正值表示尾倾)
    
    Returns:
        排水量 (t)
    """
    _load_tables()
    
    # 使用二维插值
    interp_func = interpolate.RectBivariateSpline(_DRAUGHTS, _TRIMS, _DISP_TABLE, kx=1, ky=1)
    displacement = float(interp_func(draught, trim)[0, 0])
    
    return displacement


def get_draught_from_displacement(displacement: float, trim: float = 0.0, initial_guess: float = 5.0) -> float:
    """
    根据排水量反查吃水（使用牛顿迭代法）
    
    Args:
        displacement: 排水量 (t)
        trim: 纵倾 (m)
        initial_guess: 初始猜测吃水 (m)
    
    Returns:
        吃水 (m)
    """
    _load_tables()
    
    # 使用牛顿迭代法反查吃水
    draught = initial_guess
    max_iter = 20
    tolerance = 0.001  # 1kg误差
    
    for i in range(max_iter):
        disp_calc = get_displacement_at_draught(draught, trim)
        error = disp_calc - displacement
        
        if abs(error) < tolerance:
            return draught
        
        # 计算导数（数值微分）
        delta = 0.01
        disp_plus = get_displacement_at_draught(draught + delta, trim)
        derivative = (disp_plus - disp_calc) / delta
        
        if abs(derivative) < 1e-6:
            break
        
        # 牛顿迭代
        draught = draught - error / derivative
    
    return draught


def get_km_at_draught(draught: float, trim: float = 0.0) -> float:
    """
    根据吃水和纵倾查询KM值
    
    Args:
        draught: 平均吃水 (m)
        trim: 纵倾 (m)
    
    Returns:
        KM (m)
    """
    _load_tables()
    
    interp_func = interpolate.RectBivariateSpline(_DRAUGHTS, _TRIMS, _KM_TABLE, kx=1, ky=1)
    km = float(interp_func(draught, trim)[0, 0])
    
    return km

