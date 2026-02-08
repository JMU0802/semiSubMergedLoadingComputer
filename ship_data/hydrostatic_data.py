"""
静水力数据 (Hydrostatic Data)
根据装载手册提供的静水力曲线数据
READ ONLY - DO NOT MODIFY
"""

import numpy as np

# 静水力数据表 - 航行工况 (Transit Condition)
# 吃水范围: 4.0m - 7.5m
HYDROSTATIC_TRANSIT = {
    # 吃水 (Draught in meters)
    'draught': np.array([4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 7.5]),
    
    # 排水量 (Displacement in tonnes)
    'displacement': np.array([12500, 15800, 19200, 22800, 26500, 30400, 34500, 38800]),
    
    # 浮心纵向位置 (LCB - Longitudinal Center of Buoyancy, m from AP)
    'lcb': np.array([84.2, 84.1, 84.0, 83.9, 83.8, 83.7, 83.6, 83.5]),
    
    # 浮心垂向位置 (VCB - Vertical Center of Buoyancy, m from BL)
    'vcb': np.array([2.2, 2.5, 2.8, 3.1, 3.4, 3.7, 4.0, 4.3]),
    
    # 漂心纵向位置 (LCF - Longitudinal Center of Flotation, m from AP)
    'lcf': np.array([86.5, 86.2, 85.9, 85.6, 85.3, 85.0, 84.7, 84.4]),
    
    # 每厘米吃水吨数 (TPC - Tonnes Per Centimeter)
    'tpc': np.array([58.5, 59.2, 59.8, 60.5, 61.2, 61.9, 62.6, 63.3]),
    
    # 纵稳性高 (MCT - Moment to Change Trim 1cm, t·m)
    'mct': np.array([1850, 1920, 1990, 2060, 2130, 2200, 2270, 2340]),
    
    # 横稳心高 (GMT - Transverse Metacentric Height, m)
    'gmt': np.array([4.5, 4.3, 4.1, 3.9, 3.7, 3.5, 3.3, 3.1]),
    
    # 纵稳心高 (GML - Longitudinal Metacentric Height, m)
    'gml': np.array([285, 290, 295, 300, 305, 310, 315, 320]),
    
    # 水线面积 (AWP - Area of Waterplane, m²)
    'awp': np.array([5700, 5780, 5850, 5920, 5990, 6050, 6120, 6180]),
    
    # 横稳心半径 (BMT - Transverse Metacentric Radius, m)
    'bmt': np.array([12.8, 12.5, 12.2, 11.9, 11.6, 11.3, 11.0, 10.7]),
    
    # 纵稳心半径 (BML - Longitudinal Metacentric Radius, m)
    'bml': np.array([293, 298, 303, 308, 313, 318, 323, 328]),
}

# 静水力数据表 - 半潜工况 (Semi-Submerged Condition)
# 吃水范围: 10.0m - 25.0m
HYDROSTATIC_SUBMERGED = {
    # 吃水 (Draught in meters)
    'draught': np.array([10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 25.0]),
    
    # 排水量 (Displacement in tonnes)
    'displacement': np.array([42000, 48500, 54200, 58800, 62500, 65200, 67100, 68500, 69200]),
    
    # 浮心纵向位置 (LCB, m from AP)
    'lcb': np.array([83.0, 82.5, 82.0, 81.8, 81.6, 81.5, 81.4, 81.3, 81.3]),
    
    # 浮心垂向位置 (VCB, m from BL)
    'vcb': np.array([5.8, 7.2, 8.5, 9.8, 11.0, 12.2, 13.3, 14.4, 14.9]),
    
    # 漂心纵向位置 (LCF, m from AP)
    'lcf': np.array([84.0, 83.8, 83.6, 83.5, 83.4, 83.3, 83.2, 83.1, 83.1]),
    
    # 每厘米吃水吨数 (TPC)
    'tpc': np.array([42.5, 38.2, 35.8, 34.2, 33.1, 32.3, 31.7, 31.2, 31.0]),
    
    # 纵稳性高 (MCT, t·m)
    'mct': np.array([1580, 1420, 1310, 1230, 1170, 1125, 1090, 1065, 1055]),
    
    # 横稳心高 (GMT, m) - 需要根据装载情况计算
    'gmt': np.array([2.8, 2.5, 2.3, 2.1, 1.9, 1.8, 1.7, 1.6, 1.55]),
    
    # 纵稳心高 (GML, m)
    'gml': np.array([180, 165, 155, 148, 142, 138, 135, 132, 131]),
    
    # 水线面积 (AWP, m²)
    'awp': np.array([4150, 3730, 3490, 3340, 3230, 3150, 3090, 3040, 3020]),
    
    # 横稳心半径 (BMT, m)
    'bmt': np.array([8.5, 7.8, 7.2, 6.8, 6.5, 6.3, 6.1, 6.0, 5.9]),
    
    # 纵稳心半径 (BML, m)
    'bml': np.array([186, 172, 163, 157, 153, 150, 148, 146, 145]),
}

# 稳性横截曲线数据 (Cross Curves of Stability)
# 用于计算不同排水量和横倾角下的KN值（形状臂）
# 格式: {displacement: {heel_angle: KN_value}}
# 注意：这里存储的是KN值，GZ = KN - KG*sin(θ)
CROSS_CURVES_TRANSIT = {
    # 排水量 (tonnes): {横倾角(度): KN值(m)}
    15000: {0: 0.00, 10: 1.50, 20: 2.85, 30: 4.05, 40: 4.95, 50: 5.45, 60: 5.38, 70: 4.75},
    20000: {0: 0.00, 10: 1.55, 20: 2.95, 30: 4.20, 40: 5.15, 50: 5.68, 60: 5.62, 70: 4.98},
    25000: {0: 0.00, 10: 1.60, 20: 3.05, 30: 4.35, 40: 5.35, 50: 5.90, 60: 5.85, 70: 5.20},
    30000: {0: 0.00, 10: 1.65, 20: 3.15, 30: 4.50, 40: 5.55, 50: 6.12, 60: 6.08, 70: 5.42},
    35000: {0: 0.00, 10: 1.70, 20: 3.25, 30: 4.65, 40: 5.75, 50: 6.35, 60: 6.32, 70: 5.65},
    40000: {0: 0.00, 10: 1.75, 20: 3.35, 30: 4.80, 40: 5.95, 50: 6.58, 60: 6.55, 70: 5.88},
}

CROSS_CURVES_SUBMERGED = {
    # 半潜工况的稳性横截曲线（KN值）
    45000: {0: 0.00, 10: 1.20, 20: 2.30, 30: 3.25, 40: 3.95, 50: 4.30, 60: 4.20, 70: 3.65},
    50000: {0: 0.00, 10: 1.25, 20: 2.40, 30: 3.40, 40: 4.15, 50: 4.52, 60: 4.42, 70: 3.85},
    55000: {0: 0.00, 10: 1.30, 20: 2.50, 30: 3.55, 40: 4.35, 50: 4.75, 60: 4.65, 70: 4.05},
    60000: {0: 0.00, 10: 1.35, 20: 2.60, 30: 3.70, 40: 4.55, 50: 4.98, 60: 4.88, 70: 4.25},
    65000: {0: 0.00, 10: 1.40, 20: 2.70, 30: 3.85, 40: 4.75, 50: 5.20, 60: 5.10, 70: 4.45},
    70000: {0: 0.00, 10: 1.45, 20: 2.80, 30: 4.00, 40: 4.95, 50: 5.42, 60: 5.32, 70: 4.65},
}

def get_hydrostatic_data(condition='TRANSIT'):
    """
    获取指定工况的静水力数据
    
    Args:
        condition: 'TRANSIT' 或 'SEMI_SUBMERGED'
    
    Returns:
        dict: 静水力数据字典
    """
    if condition == 'TRANSIT':
        return HYDROSTATIC_TRANSIT
    elif condition == 'SEMI_SUBMERGED':
        return HYDROSTATIC_SUBMERGED
    else:
        raise ValueError(f"Unknown condition: {condition}")

def get_cross_curves(condition='TRANSIT'):
    """
    获取指定工况的稳性横截曲线
    
    Args:
        condition: 'TRANSIT' 或 'SEMI_SUBMERGED'
    
    Returns:
        dict: 稳性横截曲线数据
    """
    if condition == 'TRANSIT':
        return CROSS_CURVES_TRANSIT
    elif condition == 'SEMI_SUBMERGED':
        return CROSS_CURVES_SUBMERGED
    else:
        raise ValueError(f"Unknown condition: {condition}")

