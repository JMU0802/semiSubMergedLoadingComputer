"""
船舶主要参数 (Ship Particulars)
根据装载手册定义的船舶基本参数
READ ONLY - DO NOT MODIFY
"""

# 船舶基本尺度 (Principal Dimensions)
SHIP_PARTICULARS = {
    # 船名 (Ship Name)
    'ship_name': 'Semi-Submersible Heavy Lift Vessel',
    'ship_number': 'B3598.1174.102',
    
    # 主尺度 (Main Dimensions)
    'loa': 216.70,          # 总长 Length Overall (m)
    'lpp': 212.13,          # 垂线间长 Length Between Perpendiculars (m)
    'breadth': 40.0,        # 型宽 Breadth Moulded (m)
    'depth': 12.5,          # 型深 Depth Moulded (m)

    # 吃水限制 (Draught Limits) - Section 3.2.1
    'max_draught_transit': 7.5,        # 航行工况最大吃水 (m)
    'max_draught_submerged': 25.0,     # 半潜工况最大吃水 (m)
    'min_draught_transit': 4.0,        # 航行工况最小吃水 (m)

    # 基准点 (Reference Points) - 从Frame 0开始测量
    'frame_0_position': 0.0,    # Frame 0位置（坐标原点）
    'ap_position': 4.24,        # 艉垂线位置 Aft Perpendicular (m from Frame 0)
    'fp_position': 216.37,      # 首垂线位置 Forward Perpendicular (m from Frame 0)
    'midship': 110.305,         # 舷中位置 Midship (m from Frame 0) = (AP+FP)/2
    
    # 设计参数 (Design Parameters) - 来自装载手册 Section 5.5
    'lightship': 20871.4,    # 空船重量 Lightship Weight (t)
    'lightship_lcg': 113.44,  # 空船重心纵向位置 LCG (m from AP)
    'lightship_vcg': 10.41,   # 空船重心垂向位置 VCG (m from BL)
    'lightship_tcg': -0.01,   # 空船重心横向位置 TCG (m from CL)
    
    # 舱容 (Tank Capacities) - 示例数据
    'ballast_capacity': 45000.0,  # 总压载水舱容 (m³)
    'fuel_capacity': 2500.0,      # 燃油舱容 (m³)
    'fw_capacity': 800.0,         # 淡水舱容 (m³)
    
    # 设计载荷 (Design Loads) - Section 3.2.2
    'max_deck_load': 50000.0,     # 最大甲板载荷 (t)
    'max_displacement': 65000.0,  # 最大排水量 (t)
}

# 工况类型 (Loading Conditions)
LOADING_CONDITIONS = {
    'TRANSIT': 'Transit Condition',              # 航行工况
    'SEMI_SUBMERGED': 'Semi-Submerged Condition',  # 半潜工况
    'AFTLOAD': 'Aftload Condition',              # 艉部装载工况
    'SIDELOAD': 'Sideload Condition',            # 侧向装载工况
}

# 压力限制 (Pressure Limitations) - Section 3.2.4
PRESSURE_LIMITS = {
    'max_deck_pressure': 15.0,    # 最大甲板压力 (t/m²)
    'max_tank_pressure': 2.5,     # 最大舱内压力 (bar)
}

# 天气限制 (Weather Limitations) - Section 3.2.3
WEATHER_LIMITS = {
    'max_wind_speed_transit': 25.0,      # 航行工况最大风速 (m/s)
    'max_wave_height_transit': 4.0,      # 航行工况最大波高 (m)
    'max_wind_speed_submerging': 15.0,   # 半潜作业最大风速 (m/s)
    'max_wave_height_submerging': 2.5,   # 半潜作业最大波高 (m)
}

# 密度常数 (Density Constants)
DENSITIES = {
    'seawater': 1.025,      # 海水密度 (t/m³)
    'freshwater': 1.000,    # 淡水密度 (t/m³)
    'fuel_oil': 0.950,      # 燃油密度 (t/m³)
    'diesel_oil': 0.900,    # 柴油密度 (t/m³)
    'lube_oil': 0.900,      # 滑油密度 (t/m³)
}

# 重力加速度 (Gravity)
GRAVITY = 9.81  # m/s²

