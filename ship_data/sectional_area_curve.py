"""
横剖面面积曲线数据 (Sectional Area Curve)
用于更精确的浮力分布计算

如果有装载手册中的邦金曲线或分站排水量数据，可以在这里定义
READ ONLY - DO NOT MODIFY
"""

import numpy as np

# 标准站位定义（从AP到FP，共21站）
# 站位0 = AP, 站位20 = FP
STANDARD_STATIONS = {
    'n_stations': 21,
    'station_spacing': 10.0,  # 站距 (m)，根据实际船长调整
}

# 示例：横剖面面积系数曲线（相对于最大横剖面面积）
# 如果有实际数据，请替换这些值
# 数据来源：装载手册或船体型线图
SECTIONAL_AREA_COEFFICIENTS = {
    # 站位号: 面积系数 (0-1)
    # 这是一个示例数据，实际应该从装载手册获取
    0: 0.00,    # AP
    1: 0.15,
    2: 0.35,
    3: 0.55,
    4: 0.72,
    5: 0.85,
    6: 0.93,
    7: 0.97,
    8: 0.99,
    9: 1.00,    # 最大横剖面（通常在中部）
    10: 1.00,
    11: 0.99,
    12: 0.97,
    13: 0.93,
    14: 0.85,
    15: 0.72,
    16: 0.55,
    17: 0.35,
    18: 0.15,
    19: 0.05,
    20: 0.00,   # FP
}

# 不同吃水下的分站排水量（如果有的话）
# 格式：{吃水: {站位: 累计排水量}}
CUMULATIVE_DISPLACEMENT_BY_DRAUGHT = {
    # 示例：吃水6m时的分站排水量
    6.0: {
        0: 0,
        1: 850,
        2: 2100,
        3: 3800,
        4: 5900,
        5: 8300,
        6: 11000,
        7: 13800,
        8: 16500,
        9: 19000,
        10: 21300,
        11: 23400,
        12: 25300,
        13: 27000,
        14: 28500,
        15: 29800,
        16: 30900,
        17: 31700,
        18: 32300,
        19: 32700,
        20: 33000,
    },
    # 可以添加更多吃水的数据
    8.0: {
        0: 0,
        1: 1200,
        2: 3000,
        3: 5400,
        4: 8300,
        5: 11600,
        6: 15200,
        7: 19000,
        8: 22800,
        9: 26400,
        10: 29700,
        11: 32700,
        12: 35400,
        13: 37800,
        14: 39900,
        15: 41700,
        16: 43200,
        17: 44400,
        18: 45300,
        19: 45900,
        20: 46200,
    },
}


def get_sectional_buoyancy_distribution(draught: float, displacement: float, lpp: float) -> dict:
    """
    根据横剖面面积曲线计算浮力分布
    
    Args:
        draught: 吃水 (m)
        displacement: 总排水量 (t)
        lpp: 垂线间长 (m)
    
    Returns:
        dict: 包含站位位置和浮力分布的字典
    """
    n_stations = STANDARD_STATIONS['n_stations']
    
    # 站位位置
    stations = np.linspace(0, lpp, n_stations)
    
    # 获取横剖面面积系数
    area_coeffs = np.array([SECTIONAL_AREA_COEFFICIENTS[i] for i in range(n_stations)])
    
    # 计算每段的浮力（通过差分）
    # 浮力密度 ∝ 横剖面面积
    buoyancy_density = area_coeffs
    
    # 归一化使总浮力 = 排水量
    total = np.sum(buoyancy_density)
    if total > 0:
        buoyancy_distribution = buoyancy_density * displacement / total
    else:
        buoyancy_distribution = np.ones(n_stations) * displacement / n_stations
    
    return {
        'stations': stations,
        'buoyancy': buoyancy_distribution,
        'area_coefficients': area_coeffs,
    }


def get_buoyancy_from_cumulative_displacement(draught: float, lpp: float) -> dict:
    """
    从累计排水量数据计算浮力分布
    
    Args:
        draught: 吃水 (m)
        lpp: 垂线间长 (m)
    
    Returns:
        dict: 包含站位位置和浮力分布的字典
    """
    # 找到最接近的吃水数据
    available_draughts = sorted(CUMULATIVE_DISPLACEMENT_BY_DRAUGHT.keys())
    
    if not available_draughts:
        return None
    
    # 简单选择最接近的吃水
    closest_draught = min(available_draughts, key=lambda d: abs(d - draught))
    
    cum_disp = CUMULATIVE_DISPLACEMENT_BY_DRAUGHT[closest_draught]
    n_stations = len(cum_disp)
    
    # 站位位置
    stations = np.linspace(0, lpp, n_stations)
    
    # 通过差分计算每段的浮力
    cum_values = np.array([cum_disp[i] for i in range(n_stations)])
    buoyancy = np.diff(cum_values, prepend=0)
    
    return {
        'stations': stations,
        'buoyancy': buoyancy,
        'cumulative_displacement': cum_values,
        'draught_used': closest_draught,
    }

