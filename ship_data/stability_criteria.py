"""
稳性衡准 (Stability Criteria)
根据装载手册 Section 3.3 定义的稳性要求
READ ONLY - DO NOT MODIFY
"""

# 航行工况完整稳性衡准 (Intact Stability Criteria for Transit Condition)
# Section 3.3.1
TRANSIT_CRITERIA = {
    # IMO Weather Criterion
    'weather_criterion': {
        'name': 'IMO Weather Criterion',
        'description': '气象衡准',
        'required': True,
        'min_value': 1.0,  # 面积比 b/a ≥ 1.0
    },
    
    # Area under GZ curve
    'area_0_30': {
        'name': 'Area 0-30°',
        'description': 'GZ曲线0-30°面积',
        'required': True,
        'min_value': 0.055,  # m·rad
        'unit': 'm·rad',
    },
    
    'area_0_40': {
        'name': 'Area 0-40°',
        'description': 'GZ曲线0-40°面积',
        'required': True,
        'min_value': 0.090,  # m·rad
        'unit': 'm·rad',
    },
    
    'area_30_40': {
        'name': 'Area 30-40°',
        'description': 'GZ曲线30-40°面积',
        'required': True,
        'min_value': 0.030,  # m·rad
        'unit': 'm·rad',
    },
    
    # Maximum GZ
    'max_gz': {
        'name': 'Maximum GZ',
        'description': '最大复原力臂',
        'required': True,
        'min_value': 0.20,  # m
        'unit': 'm',
    },
    
    # Angle of maximum GZ
    'angle_max_gz': {
        'name': 'Angle of Max GZ',
        'description': '最大GZ对应横倾角',
        'required': True,
        'min_value': 25.0,  # degrees
        'unit': 'deg',
    },
    
    # Initial GMT
    'gmt': {
        'name': 'GMT',
        'description': '初稳性高',
        'required': True,
        'min_value': 0.15,  # m
        'unit': 'm',
    },
    
    # GZ at 30 degrees
    'gz_30': {
        'name': 'GZ at 30°',
        'description': '30度横倾时的复原力臂',
        'required': True,
        'min_value': 0.20,  # m
        'unit': 'm',
    },
}

# 半潜工况完整稳性衡准 - DNV规范 (Section 3.3.2.1)
SUBMERGED_CRITERIA_DNV = {
    # DNV specific criteria for semi-submersible vessels
    'gmt': {
        'name': 'GMT (DNV)',
        'description': '初稳性高 - DNV要求',
        'required': True,
        'min_value': 1.0,  # m
        'unit': 'm',
    },
    
    'area_0_30': {
        'name': 'Area 0-30° (DNV)',
        'description': 'GZ曲线0-30°面积 - DNV要求',
        'required': True,
        'min_value': 0.040,  # m·rad
        'unit': 'm·rad',
    },
    
    'max_gz': {
        'name': 'Maximum GZ (DNV)',
        'description': '最大复原力臂 - DNV要求',
        'required': True,
        'min_value': 0.15,  # m
        'unit': 'm',
    },
    
    'angle_max_gz': {
        'name': 'Angle of Max GZ (DNV)',
        'description': '最大GZ对应横倾角 - DNV要求',
        'required': True,
        'min_value': 15.0,  # degrees
        'unit': 'deg',
    },
}

# 半潜工况完整稳性衡准 - CCS规范 (Section 3.3.2.2)
SUBMERGED_CRITERIA_CCS = {
    # CCS specific criteria for semi-submersible vessels
    'gmt': {
        'name': 'GMT (CCS)',
        'description': '初稳性高 - CCS要求',
        'required': True,
        'min_value': 0.80,  # m
        'unit': 'm',
    },
    
    'area_0_25': {
        'name': 'Area 0-25° (CCS)',
        'description': 'GZ曲线0-25°面积 - CCS要求',
        'required': True,
        'min_value': 0.035,  # m·rad
        'unit': 'm·rad',
    },
    
    'area_0_30': {
        'name': 'Area 0-30° (CCS)',
        'description': 'GZ曲线0-30°面积 - CCS要求',
        'required': True,
        'min_value': 0.055,  # m·rad
        'unit': 'm·rad',
    },
    
    'max_gz': {
        'name': 'Maximum GZ (CCS)',
        'description': '最大复原力臂 - CCS要求',
        'required': True,
        'min_value': 0.20,  # m
        'unit': 'm',
    },
    
    'gz_15': {
        'name': 'GZ at 15° (CCS)',
        'description': '15度横倾时的复原力臂 - CCS要求',
        'required': True,
        'min_value': 0.10,  # m
        'unit': 'm',
    },
}

def get_stability_criteria(condition='TRANSIT', standard='IMO'):
    """
    获取指定工况和规范的稳性衡准
    
    Args:
        condition: 'TRANSIT' 或 'SEMI_SUBMERGED'
        standard: 'IMO', 'DNV', 或 'CCS'
    
    Returns:
        dict: 稳性衡准字典
    """
    if condition == 'TRANSIT':
        return TRANSIT_CRITERIA
    elif condition == 'SEMI_SUBMERGED':
        if standard == 'DNV':
            return SUBMERGED_CRITERIA_DNV
        elif standard == 'CCS':
            return SUBMERGED_CRITERIA_CCS
        else:
            # 默认使用DNV标准
            return SUBMERGED_CRITERIA_DNV
    else:
        raise ValueError(f"Unknown condition: {condition}")

