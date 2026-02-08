"""
舱室数据 (Tank Data)
定义船舶所有舱室的容积、重心位置、自由液面惯性矩等
READ ONLY - DO NOT MODIFY
"""

# 压载水舱数据 (Ballast Tanks)
BALLAST_TANKS = {
    # 舱室编号: {参数}
    'BT1P': {
        'name': 'No.1 Ballast Tank Port',
        'type': 'BALLAST',
        'capacity': 2850.0,      # 容积 (m³)
        'lcg': 155.0,            # 重心纵向位置 (m from AP)
        'vcg': 3.5,              # 重心垂向位置 (m from BL)
        'tcg': -8.5,             # 重心横向位置 (m from CL, 负值为左舷)
        'fsi': 12500.0,          # 自由液面惯性矩 (m⁴)
        'max_fill': 98.0,        # 最大装载百分比 (%)
    },
    'BT1S': {
        'name': 'No.1 Ballast Tank Starboard',
        'type': 'BALLAST',
        'capacity': 2850.0,
        'lcg': 155.0,
        'vcg': 3.5,
        'tcg': 8.5,
        'fsi': 12500.0,
        'max_fill': 98.0,
    },
    'BT2P': {
        'name': 'No.2 Ballast Tank Port',
        'type': 'BALLAST',
        'capacity': 3200.0,
        'lcg': 125.0,
        'vcg': 3.8,
        'tcg': -9.0,
        'fsi': 14200.0,
        'max_fill': 98.0,
    },
    'BT2S': {
        'name': 'No.2 Ballast Tank Starboard',
        'type': 'BALLAST',
        'capacity': 3200.0,
        'lcg': 125.0,
        'vcg': 3.8,
        'tcg': 9.0,
        'fsi': 14200.0,
        'max_fill': 98.0,
    },
    'BT3P': {
        'name': 'No.3 Ballast Tank Port',
        'type': 'BALLAST',
        'capacity': 3500.0,
        'lcg': 95.0,
        'vcg': 4.0,
        'tcg': -9.5,
        'fsi': 15800.0,
        'max_fill': 98.0,
    },
    'BT3S': {
        'name': 'No.3 Ballast Tank Starboard',
        'type': 'BALLAST',
        'capacity': 3500.0,
        'lcg': 95.0,
        'vcg': 4.0,
        'tcg': 9.5,
        'fsi': 15800.0,
        'max_fill': 98.0,
    },
    'BT4P': {
        'name': 'No.4 Ballast Tank Port',
        'type': 'BALLAST',
        'capacity': 3500.0,
        'lcg': 65.0,
        'vcg': 4.0,
        'tcg': -9.5,
        'fsi': 15800.0,
        'max_fill': 98.0,
    },
    'BT4S': {
        'name': 'No.4 Ballast Tank Starboard',
        'type': 'BALLAST',
        'capacity': 3500.0,
        'lcg': 65.0,
        'vcg': 4.0,
        'tcg': 9.5,
        'fsi': 15800.0,
        'max_fill': 98.0,
    },
    'BT5P': {
        'name': 'No.5 Ballast Tank Port',
        'type': 'BALLAST',
        'capacity': 3200.0,
        'lcg': 35.0,
        'vcg': 3.8,
        'tcg': -9.0,
        'fsi': 14200.0,
        'max_fill': 98.0,
    },
    'BT5S': {
        'name': 'No.5 Ballast Tank Starboard',
        'type': 'BALLAST',
        'capacity': 3200.0,
        'lcg': 35.0,
        'vcg': 3.8,
        'tcg': 9.0,
        'fsi': 14200.0,
        'max_fill': 98.0,
    },
    'BT6P': {
        'name': 'No.6 Ballast Tank Port',
        'type': 'BALLAST',
        'capacity': 2850.0,
        'lcg': 10.0,
        'vcg': 3.5,
        'tcg': -8.5,
        'fsi': 12500.0,
        'max_fill': 98.0,
    },
    'BT6S': {
        'name': 'No.6 Ballast Tank Starboard',
        'type': 'BALLAST',
        'capacity': 2850.0,
        'lcg': 10.0,
        'vcg': 3.5,
        'tcg': 8.5,
        'fsi': 12500.0,
        'max_fill': 98.0,
    },
    # 底部压载舱
    'DBT1': {
        'name': 'Double Bottom Tank No.1',
        'type': 'BALLAST',
        'capacity': 1800.0,
        'lcg': 140.0,
        'vcg': 1.5,
        'tcg': 0.0,
        'fsi': 18500.0,
        'max_fill': 98.0,
    },
    'DBT2': {
        'name': 'Double Bottom Tank No.2',
        'type': 'BALLAST',
        'capacity': 2200.0,
        'lcg': 84.0,
        'vcg': 1.5,
        'tcg': 0.0,
        'fsi': 22000.0,
        'max_fill': 98.0,
    },
    'DBT3': {
        'name': 'Double Bottom Tank No.3',
        'type': 'BALLAST',
        'capacity': 1800.0,
        'lcg': 28.0,
        'vcg': 1.5,
        'tcg': 0.0,
        'fsi': 18500.0,
        'max_fill': 98.0,
    },
}

# 燃油舱数据 (Fuel Oil Tanks)
FUEL_TANKS = {
    'FO1P': {
        'name': 'Fuel Oil Tank No.1 Port',
        'type': 'FUEL_OIL',
        'capacity': 450.0,
        'lcg': 75.0,
        'vcg': 2.8,
        'tcg': -6.5,
        'fsi': 3200.0,
        'max_fill': 95.0,
    },
    'FO1S': {
        'name': 'Fuel Oil Tank No.1 Starboard',
        'type': 'FUEL_OIL',
        'capacity': 450.0,
        'lcg': 75.0,
        'vcg': 2.8,
        'tcg': 6.5,
        'fsi': 3200.0,
        'max_fill': 95.0,
    },
}

# 其他液体舱 (Other Liquid Tanks)
OTHER_TANKS = {
    'FW1': {
        'name': 'Fresh Water Tank No.1',
        'type': 'FRESH_WATER',
        'capacity': 400.0,
        'lcg': 90.0,
        'vcg': 3.2,
        'tcg': 0.0,
        'fsi': 2800.0,
        'max_fill': 95.0,
    },
}

# 合并所有舱室
ALL_TANKS = {**BALLAST_TANKS, **FUEL_TANKS, **OTHER_TANKS}

def get_tank_info(tank_id):
    """获取指定舱室信息"""
    return ALL_TANKS.get(tank_id, None)

def get_tanks_by_type(tank_type):
    """获取指定类型的所有舱室"""
    return {k: v for k, v in ALL_TANKS.items() if v['type'] == tank_type}

