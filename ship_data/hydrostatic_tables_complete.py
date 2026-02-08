"""
完整的静水力表模块 - 包括LCB和MCT
支持纵倾计算
"""

import numpy as np
from scipy import interpolate

# 吃水范围 (m)
_DRAUGHTS = np.array([
    0.00, 0.20, 0.40, 0.60, 0.80, 1.00, 1.20, 1.40, 1.60, 1.80,
    2.00, 2.20, 2.40, 2.60, 2.80, 3.00, 3.20, 3.40, 3.60, 3.80,
    4.00, 4.20, 4.40, 4.60, 4.80, 5.00, 5.20, 5.40, 5.60, 5.80,
    6.00, 6.20, 6.40, 6.60, 6.80, 7.00, 7.20, 7.40, 7.60, 7.80,
    8.00, 8.20, 8.40, 8.60, 8.80, 9.00, 9.20, 9.40, 9.60, 9.68,
    9.80, 10.00, 10.20, 10.40, 10.60, 10.80, 11.00, 11.20
])

# 纵倾范围 (m)
_TRIMS = np.array([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

# LCB表数据 (long. centre of buoy. m) - 从data.txt第168行开始
_LCB_TABLE = None

# MCT表数据 (moment to change trim tm/cm) - 从data.txt第834行开始
_MCT_TABLE = None

# LCF表数据 (long. centre of flotatio m) - 从data.txt第1498行开始
_LCF_TABLE = None

# 是否已加载数据
_DATA_LOADED = False


def _ensure_data_loaded():
    """确保数据已加载"""
    global _LCB_TABLE, _MCT_TABLE, _LCF_TABLE, _DATA_LOADED

    if not _DATA_LOADED:
        # 从lcb_mct_data.py加载数据
        try:
            from ship_data.lcb_mct_data import LCB_TABLE, MCT_TABLE, LCF_TABLE
            _LCB_TABLE = LCB_TABLE
            _MCT_TABLE = MCT_TABLE
            _LCF_TABLE = LCF_TABLE
            _DATA_LOADED = True
        except ImportError as e:
            raise ImportError(f"无法加载LCB、MCT和LCF数据: {e}。请先运行parse_lcb_mct_tables.py生成数据文件")


def get_lcb_at_draught(draught: float, trim: float = 0.0) -> float:
    """
    根据吃水和纵倾查询LCB（浮心纵向位置）
    
    Args:
        draught: 吃水 (m)
        trim: 纵倾 (m), 正值表示尾倾(by stern), 负值表示首倾(by head)
    
    Returns:
        LCB: 浮心纵向位置 (m from AP)
    """
    _ensure_data_loaded()
    
    if _LCB_TABLE is None:
        raise ValueError("LCB表数据未加载")
    
    # 使用二维插值
    interp_func = interpolate.RectBivariateSpline(_DRAUGHTS, _TRIMS, _LCB_TABLE, kx=1, ky=1)
    lcb = float(interp_func(draught, trim)[0, 0])
    
    return lcb


def get_mct_at_draught(draught: float, trim: float = 0.0) -> float:
    """
    根据吃水和纵倾查询MCT（改变纵倾一米所需力矩）

    Args:
        draught: 吃水 (m)
        trim: 纵倾 (m)

    Returns:
        MCT: 改变纵倾一米所需力矩 (tm/cm)
    """
    _ensure_data_loaded()

    if _MCT_TABLE is None:
        raise ValueError("MCT表数据未加载")

    # 使用二维插值
    interp_func = interpolate.RectBivariateSpline(_DRAUGHTS, _TRIMS, _MCT_TABLE, kx=1, ky=1)
    mct = float(interp_func(draught, trim)[0, 0])

    return mct


def get_lcf_at_draught(draught: float, trim: float = 0.0) -> float:
    """
    根据吃水和纵倾查询LCF（漂心纵向位置）

    Args:
        draught: 吃水 (m)
        trim: 纵倾 (m)

    Returns:
        LCF: 漂心纵向位置 (m from AP)
    """
    _ensure_data_loaded()

    if _LCF_TABLE is None:
        raise ValueError("LCF表数据未加载")

    # 使用二维插值
    interp_func = interpolate.RectBivariateSpline(_DRAUGHTS, _TRIMS, _LCF_TABLE, kx=1, ky=1)
    lcf = float(interp_func(draught, trim)[0, 0])

    return lcf


def calculate_trim_iterative(displacement: float, lcg: float, lpp: float = 212.13,
                             max_iterations: int = 10, tolerance: float = 0.001, debug: bool = False) -> dict:
    """
    迭代计算纵倾

    理论基础:
    1. 纵倾力矩 = (LCG - LCB) × Displacement
    2. 纵倾 = 纵倾力矩 / MCT
    3. 迭代更新直到收敛

    符号约定:
    - trim > 0: 尾倾 (by stern), Ta > Tf
    - trim < 0: 首倾 (by head), Tf > Ta
    - trim = Ta - Tf

    Args:
        displacement: 排水量 (t)
        lcg: 重心纵向位置 (m from AP)
        lpp: 垂线间长 (m)
        max_iterations: 最大迭代次数
        tolerance: 收敛容差 (m)
        debug: 是否打印调试信息

    Returns:
        dict: {
            'trim': 纵倾 (m),
            'draught_mean': 平均吃水 (m),
            'draught_ap': 尾吃水 (m),
            'draught_fp': 首吃水 (m),
            'lcb': 浮心纵向位置 (m),
            'iterations': 迭代次数
        }
    """
    from ship_data.hydrostatic_tables_2d import get_draught_from_displacement

    # 初始猜测：trim = 0
    trim = 0.0

    if debug:
        print(f"\n开始纵倾迭代计算:")
        print(f"  排水量: {displacement:.2f} t")
        print(f"  LCG: {lcg:.2f} m")

    for iteration in range(max_iterations):
        # 步骤1: 根据排水量和当前纵倾查询吃水
        draught_mean = get_draught_from_displacement(displacement, trim)

        # 步骤2: 查询LCB和MCT
        lcb = get_lcb_at_draught(draught_mean, trim)
        mct = get_mct_at_draught(draught_mean, trim)

        # 步骤3: 计算纵倾力矩
        trim_moment = (lcg - lcb) * displacement  # tm

        # 步骤4: 计算新的纵倾
        # MCT单位是tm/cm，所以纵倾单位是cm
        trim_new_cm = trim_moment / mct  # cm
        trim_new = trim_new_cm / 100.0  # 转换为m

        if debug:
            print(f"\n  迭代 {iteration + 1}:")
            print(f"    当前trim: {trim:.4f} m")
            print(f"    吃水: {draught_mean:.4f} m")
            print(f"    LCB: {lcb:.2f} m")
            print(f"    MCT: {mct:.1f} tm/cm")
            print(f"    纵倾力矩: (LCG-LCB)×Δ = ({lcg:.2f}-{lcb:.2f})×{displacement:.0f} = {trim_moment:.0f} tm")
            print(f"    新trim: {trim_new:.4f} m")
            print(f"    变化: {abs(trim_new - trim):.4f} m")

        # 检查收敛
        if abs(trim_new - trim) < tolerance:
            # 计算首尾吃水
            # trim = Ta - Tf (尾吃水 - 首吃水)
            # draught_mean = (Ta + Tf) / 2
            # 解得: Ta = draught_mean + trim/2, Tf = draught_mean - trim/2
            draught_ap = draught_mean + trim_new / 2
            draught_fp = draught_mean - trim_new / 2

            if debug:
                print(f"\n  ✓ 收敛！")
                print(f"    最终trim: {trim_new:.4f} m")
                print(f"    平均吃水: {draught_mean:.4f} m")
                print(f"    尾吃水: {draught_ap:.4f} m")
                print(f"    首吃水: {draught_fp:.4f} m")

            return {
                'trim': trim_new,
                'draught_mean': draught_mean,
                'draught_ap': draught_ap,
                'draught_fp': draught_fp,
                'lcb': lcb,
                'iterations': iteration + 1,
                'converged': True
            }

        # 更新纵倾
        trim = trim_new
    
    # 未收敛
    print(f"  警告: 纵倾计算未在{max_iterations}次迭代内收敛")
    
    draught_ap = draught_mean + trim / 2
    draught_fp = draught_mean - trim / 2
    
    return {
        'trim': trim,
        'draught_mean': draught_mean,
        'draught_ap': draught_ap,
        'draught_fp': draught_fp,
        'lcb': lcb,
        'iterations': max_iterations,
        'converged': False
    }

