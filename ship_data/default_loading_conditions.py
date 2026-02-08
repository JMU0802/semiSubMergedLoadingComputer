"""
默认装载工况数据
包含LC01、LC03、LC26的完整装载数据
"""

# 空船数据
LIGHTWEIGHT = {
    'weight': 20871.4,  # t
    'lcg': 113.44,      # m
    'vcg': 10.44,       # m
    'tcg': -0.01,       # m
}

# LC01: Light ballast, departure
LC01_DATA = {
    'name': 'LC01: Light ballast, departure',
    'description': '轻压载，出港',
    'lightweight': LIGHTWEIGHT,
    'tanks': {
        # 重油 - 全部空载
        # 柴油 - 全部空载
        # 润滑油 - 全部空载
        # 技术水 - 全部空载
        # 淡水 - 全部空载
        # 压载水 - 部分装载
        # 其他 - 全部空载
    },
    'other_items': [
        {'name': 'Stores', 'weight': 10.0, 'lcg': 199.20, 'tcg': 0.00, 'vcg': 29.05, 'fsm': 0.0},
        {'name': 'Crew', 'weight': 6.0, 'lcg': 199.20, 'tcg': 0.00, 'vcg': 35.70, 'fsm': 0.0},
        {'name': 'Miscellaneous', 'weight': 87.0, 'lcg': 178.40, 'tcg': 0.00, 'vcg': 5.00, 'fsm': 0.0},
    ],
    # 手册参考值
    'manual_values': {
        'displacement': 47516.5,
        'lcg': 109.80,
        'vcg': 6.66,
        'fsm': 12370.2,
        'draught': 7.00,
        'km': 26.10,
        'gm0': 19.44,
        'dgm': 0.26,
        'gmf': 19.18,
    }
}

# LC03: Heavy ballast / min. ice draught, departure  
LC03_DATA = {
    'name': 'LC03: Heavy ballast / min. ice draught, departure',
    'description': '重压载/最小冰区吃水，出港',
    'lightweight': LIGHTWEIGHT,
    'tanks': {
        # 重油
        'HFO1': {'filling': 12.0},
        'HFO2': {'filling': 12.0},
        'HFO3': {'filling': 12.0},
        'HFO4': {'filling': 12.0},
        'T09.03': {'filling': 50.0},
        'T09.04': {'filling': 50.0},
        'T09.05': {'filling': 50.0},
        'T09.06': {'filling': 50.0},
        # 柴油
        'MGO': {'filling': 12.0},
        'T09.07': {'filling': 12.0},
        'T09.08': {'filling': 12.0},
        'T09.18': {'filling': 50.0},
        'T09.19': {'filling': 50.0},
        # 润滑油
        'T09.09': {'filling': 19.4},
        # 技术水
        'T09.10': {'filling': 10.0},
        # 淡水
        'FW1': {'filling': 10.0},
        'FW2': {'filling': 10.0},
        'FW3': {'filling': 10.0},
        'T10.01': {'filling': 10.0},
        # 压载水
        'WB03.01': {'filling': 100.0},
        'WB03.02': {'filling': 100.0},
        'WB03.07': {'filling': 54.1},
        'WB03.08': {'filling': 55.2},
        'WB11.01': {'filling': 56.5},
        # 固定淡水压载
        'WB02.01': {'filling': 100.0},
        # 灰水
        'T09.11': {'filling': 100.0},
        'T09.13': {'filling': 100.0},
        # 舱底水
        'T09.20': {'filling': 100.0},
        'T09.22': {'filling': 100.0},
        # 油泥
        'T09.21': {'filling': 98.0},
    },
    'other_items': [
        {'name': 'Stores', 'weight': 10.0, 'lcg': 199.20, 'tcg': 0.00, 'vcg': 29.05, 'fsm': 0.0},
        {'name': 'Crew', 'weight': 6.0, 'lcg': 199.20, 'tcg': 0.00, 'vcg': 35.70, 'fsm': 0.0},
        {'name': 'Miscellaneous', 'weight': 87.0, 'lcg': 178.40, 'tcg': 0.00, 'vcg': 5.00, 'fsm': 0.0},
    ],
    # 手册参考值
    'manual_values': {
        'displacement': 55395.1,
        'lcg': 109.05,
        'vcg': 6.64,
        'fsm': 12421.7,
        'draught': 8.00,
        'km': 24.23,
        'gm0': 17.58,
        'dgm': 0.22,
        'gmf': 17.36,
    }
}

# LC26: Buoyant Cargo Super Gorilla 16000t, arr.
LC26_DATA = {
    'name': 'LC26: Buoyant Cargo Super Gorilla 16000t, arr.',
    'description': '浮力货物Super Gorilla 16000吨，到港',
    'lightweight': LIGHTWEIGHT,
    'tanks': {
        # 重油 - 5%
        'HFO1': {'filling': 5.0},
        'HFO2': {'filling': 5.0},
        'HFO3': {'filling': 5.0},
        'HFO4': {'filling': 5.0},
        'T09.03': {'filling': 50.0},
        'T09.04': {'filling': 50.0},
        'T09.05': {'filling': 50.0},
        'T09.06': {'filling': 50.0},
        # 柴油 - 5%
        'MGO': {'filling': 5.0},
        'T09.07': {'filling': 5.0},
        'T09.08': {'filling': 5.0},
        'T09.18': {'filling': 50.0},
        'T09.19': {'filling': 50.0},
        # 润滑油
        'T09.09': {'filling': 10.0},
        # 技术水
        'T09.10': {'filling': 10.0},
        # 淡水
        'FW1': {'filling': 10.0},
        'FW2': {'filling': 10.0},
        'FW3': {'filling': 10.0},
        'T10.01': {'filling': 10.0},
        # 压载水 - 部分装载
        # 其他舱室根据需要
    },
    'other_items': [
        {'name': 'Stores', 'weight': 10.0, 'lcg': 199.20, 'tcg': 0.00, 'vcg': 29.05, 'fsm': 0.0},
        {'name': 'Crew', 'weight': 6.0, 'lcg': 199.20, 'tcg': 0.00, 'vcg': 35.70, 'fsm': 0.0},
        {'name': 'Miscellaneous', 'weight': 87.0, 'lcg': 178.40, 'tcg': 0.00, 'vcg': 5.00, 'fsm': 0.0},
        # 货物
        {'name': 'Cargo: Super Gorilla', 'weight': 16000.0, 'lcg': 105.00, 'tcg': 0.00, 'vcg': 37.00, 'fsm': 0.0},
    ],
    # 手册参考值
    'manual_values': {
        'displacement': 67493.4,
        'lcg': 107.82,
        'vcg': 13.93,
        'fsm': 9227.2,
        'draught': 9.48,
        'km': 22.37,
        'gm0': 8.45,
        'dgm': 0.14,
        'gmf': 8.31,
    }
}

# 所有默认工况
DEFAULT_CONDITIONS = {
    'LC01': LC01_DATA,
    'LC03': LC03_DATA,
    'LC26': LC26_DATA,
}


def get_loading_condition(lc_name):
    """获取指定的装载工况数据"""
    return DEFAULT_CONDITIONS.get(lc_name, None)


def get_all_condition_names():
    """获取所有工况名称"""
    return list(DEFAULT_CONDITIONS.keys())

