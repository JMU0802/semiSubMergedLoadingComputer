"""
舱室详细信息数据模块
提供对所有舱室详细信息的访问接口
"""

import json
import os
from scipy import interpolate


# 加载舱室详细信息
_current_dir = os.path.dirname(os.path.abspath(__file__))
_json_file = os.path.join(_current_dir, 'tanks_details_data.json')

with open(_json_file, 'r', encoding='utf-8') as f:
    TANKS_DETAILS = json.load(f)


def get_tank_info(tank_id):
    """
    获取指定舱室的详细信息
    
    Args:
        tank_id: 舱室ID，例如 'WB01.11'
        
    Returns:
        dict: 舱室详细信息，如果不存在则返回None
    """
    return TANKS_DETAILS.get(tank_id)


def get_tank_spatial_extent(tank_id):
    """
    获取舱室的空间范围
    
    Args:
        tank_id: 舱室ID
        
    Returns:
        dict: 包含 aft_position, fore_position, lowest_point, highest_point
    """
    tank = get_tank_info(tank_id)
    if tank is None:
        return None
    
    return {
        'aft_position': tank['aft_position'],  # m from Frame 0
        'fore_position': tank['fore_position'],  # m from Frame 0
        'lowest_point': tank['lowest_point'],  # m above BL
        'highest_point': tank['highest_point']  # m above BL
    }


def get_tank_properties_at_fill(tank_id, fill_pct):
    """
    获取指定装载百分比下的舱室属性（使用插值）
    
    Args:
        tank_id: 舱室ID
        fill_pct: 装载百分比 (0-100)
        
    Returns:
        dict: 包含 mass, lcg, tcg, vcg, fsm, volume, height
    """
    tank = get_tank_info(tank_id)
    if tank is None or not tank['filling_table']:
        return None
    
    filling_table = tank['filling_table']
    
    # 提取数据
    fill_pcts = [entry['fill_pct'] for entry in filling_table]
    masses = [entry['mass'] for entry in filling_table]
    lcgs = [entry['lcg'] for entry in filling_table]
    tcgs = [entry['tcg'] for entry in filling_table]
    vcgs = [entry['vcg'] for entry in filling_table]
    fsms = [entry['fsm'] for entry in filling_table]
    volumes = [entry['volume'] for entry in filling_table]
    heights = [entry['height'] for entry in filling_table]
    
    # 如果正好在表格中，直接返回
    for entry in filling_table:
        if abs(entry['fill_pct'] - fill_pct) < 0.01:
            return {
                'mass': entry['mass'],
                'lcg': entry['lcg'],
                'tcg': entry['tcg'],
                'vcg': entry['vcg'],
                'fsm': entry['fsm'],
                'volume': entry['volume'],
                'height': entry['height']
            }
    
    # 否则使用线性插值
    if fill_pct < min(fill_pcts) or fill_pct > max(fill_pcts):
        return None  # 超出范围
    
    return {
        'mass': float(interpolate.interp1d(fill_pcts, masses, kind='linear')(fill_pct)),
        'lcg': float(interpolate.interp1d(fill_pcts, lcgs, kind='linear')(fill_pct)),
        'tcg': float(interpolate.interp1d(fill_pcts, tcgs, kind='linear')(fill_pct)),
        'vcg': float(interpolate.interp1d(fill_pcts, vcgs, kind='linear')(fill_pct)),
        'fsm': float(interpolate.interp1d(fill_pcts, fsms, kind='linear')(fill_pct)),
        'volume': float(interpolate.interp1d(fill_pcts, volumes, kind='linear')(fill_pct)),
        'height': float(interpolate.interp1d(fill_pcts, heights, kind='linear')(fill_pct))
    }


def list_all_tanks():
    """
    列出所有舱室ID
    
    Returns:
        list: 所有舱室ID列表
    """
    return list(TANKS_DETAILS.keys())


def get_tanks_count():
    """
    获取舱室总数
    
    Returns:
        int: 舱室数量
    """
    return len(TANKS_DETAILS)


if __name__ == '__main__':
    # 测试
    print(f"总舱室数: {get_tanks_count()}")
    print()
    
    # 测试获取舱室信息
    tank_id = 'WB01.11'
    info = get_tank_info(tank_id)
    print(f"舱室 {tank_id}:")
    print(f"  描述: {info['description']}")
    print(f"  密度: {info['density']} t/m³")
    print(f"  艉端位置: {info['aft_position']} m")
    print(f"  首端位置: {info['fore_position']} m")
    print()
    
    # 测试插值
    fill_pct = 50.0
    props = get_tank_properties_at_fill(tank_id, fill_pct)
    print(f"舱室 {tank_id} 在 {fill_pct}% 装载时:")
    print(f"  质量: {props['mass']:.2f} t")
    print(f"  LCG: {props['lcg']:.2f} m")
    print(f"  VCG: {props['vcg']:.2f} m")

