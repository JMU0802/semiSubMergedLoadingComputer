"""
舱室定义数据库
包含所有舱室的容积、重心位置、密度等参数
自动生成 - 2026-02-08
"""

# 密度定义 (t/m³)
DENSITIES = {
    'HFO': 0.991,      # Heavy Fuel Oil
    'MDO': 0.900,      # Marine Diesel Oil
    'MGO': 0.900,      # Marine Gas Oil
    'LO': 0.900,       # Lubricating Oil
    'FW': 1.000,       # Fresh Water
    'TW': 1.000,       # Technical Water
    'BW': 1.025,       # Ballast Water (seawater)
    'GW': 1.000,       # Gray Water
    'BILGE': 1.000,    # Bilge Water
    'SLUDGE': 2.380,   # Sludge
}

# Heavy Fuel Oil
HFO_TANKS = {
    'HFO1': {
        'name': 'HFO Storage Tank 1',
        'category': 'Heavy Fuel Oil',
        'max_volume': 1061.6,
        'lcg': 63.60,
        'tcg': 5.51,
        'vcg': 6.61,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {12.0: 11.33, 100.0: 0.0}
    },
    'HFO2': {
        'name': 'HFO Storage Tank 2',
        'category': 'Heavy Fuel Oil',
        'max_volume': 1273.9,
        'lcg': 64.80,
        'tcg': -5.51,
        'vcg': 6.61,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {12.0: 11.32, 100.0: 0.0}
    },
    'HFO3': {
        'name': 'HFO Storage Tank 3',
        'category': 'Heavy Fuel Oil',
        'max_volume': 833.8,
        'lcg': 76.72,
        'tcg': 5.32,
        'vcg': 5.47,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {12.0: 9.81, 69.5: 1.45, 100.0: 0.0}
    },
    'HFO4': {
        'name': 'HFO Storage Tank 4',
        'category': 'Heavy Fuel Oil',
        'max_volume': 834.0,
        'lcg': 76.72,
        'tcg': -5.32,
        'vcg': 5.47,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {12.0: 9.81, 69.5: 1.45, 100.0: 0.0}
    },
    'T09.03': {
        'name': 'HFO Settling Tank P',
        'category': 'Heavy Fuel Oil',
        'max_volume': 56.1,
        'lcg': 186.74,
        'tcg': 3.94,
        'vcg': 3.61,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {50.0: 0.21, 100.0: 0.0}
    },
    'T09.04': {
        'name': 'HFO Settling Tank S',
        'category': 'Heavy Fuel Oil',
        'max_volume': 44.4,
        'lcg': 187.16,
        'tcg': -3.94,
        'vcg': 3.65,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {50.0: 0.21, 100.0: 0.0}
    },
    'T09.05': {
        'name': 'HFO Service Tank P',
        'category': 'Heavy Fuel Oil',
        'max_volume': 37.3,
        'lcg': 186.74,
        'tcg': 6.13,
        'vcg': 3.61,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {50.0: 0.09, 100.0: 0.0}
    },
    'T09.06': {
        'name': 'HFO Service Tank S',
        'category': 'Heavy Fuel Oil',
        'max_volume': 29.7,
        'lcg': 187.16,
        'tcg': -6.13,
        'vcg': 3.65,
        'density': DENSITIES['HFO'],
        'fsm_coeff': {50.0: 0.1, 100.0: 0.0}
    },
}

# Diesel Oil
DIESEL_TANKS = {
    'MGO': {
        'name': 'MGO Storage Tank',
        'category': 'Diesel Oil',
        'max_volume': 212.0,
        'lcg': 70.80,
        'tcg': 5.69,
        'vcg': 3.08,
        'density': DENSITIES['MDO'],
        'fsm_coeff': {10.5: 12.92, 12.0: 11.34, 100.0: 0.0}
    },
    'T09.07': {
        'name': 'MDO Storage P',
        'category': 'Diesel Oil',
        'max_volume': 34.5,
        'lcg': 179.30,
        'tcg': 9.58,
        'vcg': 3.38,
        'density': DENSITIES['MDO'],
        'fsm_coeff': {12.0: 1.73, 78.6: 0.26, 100.0: 0.0}
    },
    'T09.08': {
        'name': 'MDO Storage S',
        'category': 'Diesel Oil',
        'max_volume': 34.5,
        'lcg': 179.30,
        'tcg': -9.58,
        'vcg': 3.38,
        'density': DENSITIES['MDO'],
        'fsm_coeff': {12.0: 1.73, 78.6: 0.26, 100.0: 0.0}
    },
    'T09.18': {
        'name': 'MDO Service P',
        'category': 'Diesel Oil',
        'max_volume': 12.4,
        'lcg': 181.20,
        'tcg': 8.63,
        'vcg': 2.88,
        'density': DENSITIES['MDO'],
        'fsm_coeff': {50.0: 0.11, 100.0: 0.0}
    },
    'T09.19': {
        'name': 'MDO Service S',
        'category': 'Diesel Oil',
        'max_volume': 12.4,
        'lcg': 181.20,
        'tcg': -8.63,
        'vcg': 2.88,
        'density': DENSITIES['MDO'],
        'fsm_coeff': {50.0: 0.11, 100.0: 0.0}
    },
}

# Lubricating Oil
LO_TANKS = {
    'T09.09': {
        'name': 'Used LO',
        'category': 'Lubricating Oil',
        'max_volume': 40.1,
        'lcg': 179.80,
        'tcg': 9.33,
        'vcg': 5.79,
        'density': DENSITIES['LO'],
        'fsm_coeff': {19.4: 1.3, 100.0: 0.0}
    },
}

# Technical Water
TW_TANKS = {
    'T09.10': {
        'name': 'Feed Water',
        'category': 'Technical Water',
        'max_volume': 40.2,
        'lcg': 179.80,
        'tcg': -9.33,
        'vcg': 6.25,
        'density': DENSITIES['TW'],
        'fsm_coeff': {10.0: 2.52, 49.8: 0.51, 100.0: 0.0}
    },
}

# Fresh Water
FW_TANKS = {
    'FW1': {
        'name': 'Fresh Water P',
        'category': 'Fresh Water',
        'max_volume': 219.2,
        'lcg': 194.80,
        'tcg': 4.81,
        'vcg': 17.46,
        'density': DENSITIES['FW'],
        'fsm_coeff': {10.0: 2.75, 36.5: 0.75, 100.0: 0.0}
    },
    'FW2': {
        'name': 'Fresh Water S',
        'category': 'Fresh Water',
        'max_volume': 219.2,
        'lcg': 194.80,
        'tcg': -4.81,
        'vcg': 17.46,
        'density': DENSITIES['FW'],
        'fsm_coeff': {10.0: 2.75, 36.5: 0.75, 100.0: 0.0}
    },
    'FW3': {
        'name': 'Fresh Water C',
        'category': 'Fresh Water',
        'max_volume': 156.6,
        'lcg': 196.40,
        'tcg': 0.00,
        'vcg': 20.64,
        'density': DENSITIES['FW'],
        'fsm_coeff': {10.0: 9.99, 44.7: 2.24, 100.0: 0.0}
    },
    'T10.01': {
        'name': 'Potable Water',
        'category': 'Fresh Water',
        'max_volume': 75.6,
        'lcg': 196.40,
        'tcg': 0.00,
        'vcg': 17.61,
        'density': DENSITIES['FW'],
        'fsm_coeff': {10.0: 8.71, 92.6: 0.95, 100.0: 0.0}
    },
}

# Ballast Water
BW_TANKS = {
    'WB02.05': {
        'name': 'Water Ballast 02.05',
        'category': 'Ballast Water',
        'max_volume': 1487.6,
        'lcg': 23.01,
        'tcg': 5.35,
        'vcg': 7.78,
        'density': DENSITIES['BW'],
        'fsm_coeff': {60.0: 2.79, 78.2: 2.15, 100.0: 0.0}
    },
    'WB02.06': {
        'name': 'Water Ballast 02.06',
        'category': 'Ballast Water',
        'max_volume': 1489.4,
        'lcg': 23.02,
        'tcg': -5.35,
        'vcg': 7.78,
        'density': DENSITIES['BW'],
        'fsm_coeff': {60.0: 2.85, 78.1: 2.15, 100.0: 0.0}
    },
    'WB02.07': {
        'name': 'Water Ballast 02.07',
        'category': 'Ballast Water',
        'max_volume': 928.9,
        'lcg': 25.82,
        'tcg': 15.38,
        'vcg': 7.31,
        'density': DENSITIES['BW'],
        'fsm_coeff': {60.0: 2.71, 100.0: 0.0}
    },
    'WB02.08': {
        'name': 'Water Ballast 02.08',
        'category': 'Ballast Water',
        'max_volume': 928.9,
        'lcg': 25.82,
        'tcg': -15.38,
        'vcg': 7.31,
        'density': DENSITIES['BW'],
        'fsm_coeff': {60.0: 2.71, 100.0: 0.0}
    },
    'WB03.01': {
        'name': 'Water Ballast 03.01',
        'category': 'Ballast Water',
        'max_volume': 470.5,
        'lcg': 47.42,
        'tcg': 5.24,
        'vcg': 1.46,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB03.02': {
        'name': 'Water Ballast 03.02',
        'category': 'Ballast Water',
        'max_volume': 478.0,
        'lcg': 47.48,
        'tcg': -5.17,
        'vcg': 1.46,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB03.06': {
        'name': 'Water Ballast 03.06',
        'category': 'Ballast Water',
        'max_volume': 937.3,
        'lcg': 39.21,
        'tcg': 0.00,
        'vcg': 5.18,
        'density': DENSITIES['BW'],
        'fsm_coeff': {8.9: 11.06, 59.1: 1.79, 100.0: 0.0}
    },
    'WB03.07': {
        'name': 'Water Ballast 03.07',
        'category': 'Ballast Water',
        'max_volume': 2076.5,
        'lcg': 46.50,
        'tcg': 16.11,
        'vcg': 6.30,
        'density': DENSITIES['BW'],
        'fsm_coeff': {49.8: 1.89, 54.1: 1.77, 55.2: 1.74, 69.9: 1.4, 86.8: 1.13, 93.7: 1.05, 100.0: 0.0}
    },
    'WB03.08': {
        'name': 'Water Ballast 03.08',
        'category': 'Ballast Water',
        'max_volume': 2076.5,
        'lcg': 46.50,
        'tcg': -16.11,
        'vcg': 6.30,
        'density': DENSITIES['BW'],
        'fsm_coeff': {46.1: 2.01, 52.3: 1.82, 55.2: 1.74, 69.9: 1.4, 86.8: 1.13, 93.7: 1.05, 100.0: 0.0}
    },
    'WB04.01': {
        'name': 'Water Ballast 04.01',
        'category': 'Ballast Water',
        'max_volume': 1277.0,
        'lcg': 69.62,
        'tcg': 10.53,
        'vcg': 1.31,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB04.02': {
        'name': 'Water Ballast 04.02',
        'category': 'Ballast Water',
        'max_volume': 1277.0,
        'lcg': 69.62,
        'tcg': -10.53,
        'vcg': 1.31,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB04.07': {
        'name': 'Water Ballast 04.07',
        'category': 'Ballast Water',
        'max_volume': 1952.8,
        'lcg': 69.60,
        'tcg': 16.44,
        'vcg': 6.70,
        'density': DENSITIES['BW'],
        'fsm_coeff': {18.8: 5.54, 93.2: 1.12, 95.1: 1.1, 100.0: 0.0}
    },
    'WB04.08': {
        'name': 'Water Ballast 04.08',
        'category': 'Ballast Water',
        'max_volume': 1952.8,
        'lcg': 69.60,
        'tcg': -16.44,
        'vcg': 6.70,
        'density': DENSITIES['BW'],
        'fsm_coeff': {18.8: 5.54, 91.6: 1.14, 94.3: 1.1, 100.0: 0.0}
    },
    'WB05.01': {
        'name': 'Water Ballast 05.01',
        'category': 'Ballast Water',
        'max_volume': 1288.1,
        'lcg': 93.51,
        'tcg': 10.63,
        'vcg': 1.30,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB05.02': {
        'name': 'Water Ballast 05.02',
        'category': 'Ballast Water',
        'max_volume': 1288.1,
        'lcg': 93.51,
        'tcg': -10.63,
        'vcg': 1.30,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB05.05': {
        'name': 'Water Ballast 05.05',
        'category': 'Ballast Water',
        'max_volume': 2106.1,
        'lcg': 93.47,
        'tcg': 5.48,
        'vcg': 4.62,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 2.05, 100.0: 0.0}
    },
    'WB05.06': {
        'name': 'Water Ballast 05.06',
        'category': 'Ballast Water',
        'max_volume': 2106.1,
        'lcg': 93.47,
        'tcg': -5.48,
        'vcg': 4.62,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 2.05, 100.0: 0.0}
    },
    'WB05.07': {
        'name': 'Water Ballast 05.07',
        'category': 'Ballast Water',
        'max_volume': 1952.8,
        'lcg': 93.60,
        'tcg': 16.44,
        'vcg': 6.70,
        'density': DENSITIES['BW'],
        'fsm_coeff': {51.9: 2.01, 75.0: 1.39, 77.4: 1.35, 100.0: 0.0}
    },
    'WB05.08': {
        'name': 'Water Ballast 05.08',
        'category': 'Ballast Water',
        'max_volume': 1952.8,
        'lcg': 93.60,
        'tcg': -16.44,
        'vcg': 6.70,
        'density': DENSITIES['BW'],
        'fsm_coeff': {51.9: 2.01, 73.9: 1.41, 75.0: 1.39, 100.0: 0.0}
    },
    'WB06.01': {
        'name': 'Water Ballast 06.01',
        'category': 'Ballast Water',
        'max_volume': 1288.1,
        'lcg': 117.51,
        'tcg': 10.63,
        'vcg': 1.30,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB06.02': {
        'name': 'Water Ballast 06.02',
        'category': 'Ballast Water',
        'max_volume': 1288.1,
        'lcg': 117.51,
        'tcg': -10.63,
        'vcg': 1.30,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB06.05': {
        'name': 'Water Ballast 06.05',
        'category': 'Ballast Water',
        'max_volume': 2106.1,
        'lcg': 117.47,
        'tcg': 5.48,
        'vcg': 4.62,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 2.05, 100.0: 0.0}
    },
    'WB06.06': {
        'name': 'Water Ballast 06.06',
        'category': 'Ballast Water',
        'max_volume': 2106.1,
        'lcg': 117.47,
        'tcg': -5.48,
        'vcg': 4.62,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 2.05, 100.0: 0.0}
    },
    'WB06.07': {
        'name': 'Water Ballast 06.07',
        'category': 'Ballast Water',
        'max_volume': 1952.8,
        'lcg': 117.60,
        'tcg': 16.44,
        'vcg': 6.70,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB06.08': {
        'name': 'Water Ballast 06.08',
        'category': 'Ballast Water',
        'max_volume': 1952.8,
        'lcg': 117.60,
        'tcg': -16.44,
        'vcg': 6.70,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB07.01': {
        'name': 'Water Ballast 07.01',
        'category': 'Ballast Water',
        'max_volume': 1517.8,
        'lcg': 143.70,
        'tcg': 10.44,
        'vcg': 1.31,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB07.02': {
        'name': 'Water Ballast 07.02',
        'category': 'Ballast Water',
        'max_volume': 1517.8,
        'lcg': 143.70,
        'tcg': -10.44,
        'vcg': 1.31,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB07.05': {
        'name': 'Water Ballast 07.05',
        'category': 'Ballast Water',
        'max_volume': 2536.4,
        'lcg': 143.85,
        'tcg': 5.49,
        'vcg': 4.62,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 2.03, 100.0: 0.0}
    },
    'WB07.06': {
        'name': 'Water Ballast 07.06',
        'category': 'Ballast Water',
        'max_volume': 2536.4,
        'lcg': 143.85,
        'tcg': -5.49,
        'vcg': 4.62,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 2.03, 100.0: 0.0}
    },
    'WB07.07': {
        'name': 'Water Ballast 07.07',
        'category': 'Ballast Water',
        'max_volume': 2332.3,
        'lcg': 143.94,
        'tcg': 16.42,
        'vcg': 6.71,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB07.08': {
        'name': 'Water Ballast 07.08',
        'category': 'Ballast Water',
        'max_volume': 2332.3,
        'lcg': 143.94,
        'tcg': -16.42,
        'vcg': 6.71,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB08.01': {
        'name': 'Water Ballast 08.01',
        'category': 'Ballast Water',
        'max_volume': 833.2,
        'lcg': 167.59,
        'tcg': -0.04,
        'vcg': 1.03,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB08.03': {
        'name': 'Water Ballast 08.03',
        'category': 'Ballast Water',
        'max_volume': 185.0,
        'lcg': 165.55,
        'tcg': 14.11,
        'vcg': 1.49,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB08.04': {
        'name': 'Water Ballast 08.04',
        'category': 'Ballast Water',
        'max_volume': 185.0,
        'lcg': 165.55,
        'tcg': -14.11,
        'vcg': 1.49,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB08.07': {
        'name': 'Water Ballast 08.07',
        'category': 'Ballast Water',
        'max_volume': 1170.3,
        'lcg': 167.13,
        'tcg': 15.42,
        'vcg': 7.04,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 1.58, 82.3: 1.19, 93.5: 1.1, 100.0: 0.0}
    },
    'WB08.08': {
        'name': 'Water Ballast 08.08',
        'category': 'Ballast Water',
        'max_volume': 1170.3,
        'lcg': 167.13,
        'tcg': -15.42,
        'vcg': 7.04,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 1.58, 76.7: 1.24, 93.5: 1.1, 100.0: 0.0}
    },
    'WB09.01': {
        'name': 'Water Ballast 09.01',
        'category': 'Ballast Water',
        'max_volume': 427.9,
        'lcg': 182.90,
        'tcg': -0.00,
        'vcg': 1.12,
        'density': DENSITIES['BW'],
        'fsm_coeff': {100.0: 0.0}
    },
    'WB09.07': {
        'name': 'Water Ballast 09.07',
        'category': 'Ballast Water',
        'max_volume': 618.0,
        'lcg': 183.26,
        'tcg': 12.72,
        'vcg': 8.16,
        'density': DENSITIES['BW'],
        'fsm_coeff': {65.0: 0.37, 100.0: 0.0}
    },
    'WB09.08': {
        'name': 'Water Ballast 09.08',
        'category': 'Ballast Water',
        'max_volume': 618.0,
        'lcg': 183.26,
        'tcg': -12.72,
        'vcg': 8.16,
        'density': DENSITIES['BW'],
        'fsm_coeff': {65.0: 0.37, 100.0: 0.0}
    },
    'WB10.01': {
        'name': 'Water Ballast 10.01',
        'category': 'Ballast Water',
        'max_volume': 306.5,
        'lcg': 194.02,
        'tcg': 0.00,
        'vcg': 1.44,
        'density': DENSITIES['BW'],
        'fsm_coeff': {50.0: 12.91, 100.0: 0.0}
    },
    'WB10.05': {
        'name': 'Water Ballast 10.05',
        'category': 'Ballast Water',
        'max_volume': 1020.5,
        'lcg': 194.09,
        'tcg': 4.65,
        'vcg': 4.14,
        'density': DENSITIES['BW'],
        'fsm_coeff': {25.0: 3.4, 100.0: 0.0}
    },
    'WB10.06': {
        'name': 'Water Ballast 10.06',
        'category': 'Ballast Water',
        'max_volume': 1020.5,
        'lcg': 194.09,
        'tcg': -4.65,
        'vcg': 4.14,
        'density': DENSITIES['BW'],
        'fsm_coeff': {25.0: 3.4, 100.0: 0.0}
    },
    'WB11.01': {
        'name': 'Water Ballast 11.01',
        'category': 'Ballast Water',
        'max_volume': 1599.7,
        'lcg': 205.73,
        'tcg': -0.00,
        'vcg': 5.95,
        'density': DENSITIES['BW'],
        'fsm_coeff': {12.8: 3.01, 22.1: 3.08, 28.7: 3.63, 30.5: 3.57, 40.2: 3.25, 42.6: 3.18, 49.4: 2.98, 56.5: 2.8, 68.2: 2.44, 72.0: 2.33, 100.0: 0.0}
    },
}

# Fixed FW ballast
FIXED_BW_TANKS = {
    'WB02.01': {
        'name': 'Water Ballast 02.01',
        'category': 'Fixed FW ballast',
        'max_volume': 321.1,
        'lcg': 14.73,
        'tcg': 0.00,
        'vcg': 3.55,
        'density': DENSITIES['FW'],
        'fsm_coeff': {100.0: 0.0}
    },
}

# Gray Water
GW_TANKS = {
    'T09.11': {
        'name': 'Black Water',
        'category': 'Gray Water',
        'max_volume': 18.5,
        'lcg': 180.00,
        'tcg': 4.16,
        'vcg': 7.00,
        'density': DENSITIES['GW'],
        'fsm_coeff': {50.0: 0.1, 100.0: 0.0}
    },
    'T09.13': {
        'name': 'Gray Water',
        'category': 'Gray Water',
        'max_volume': 30.9,
        'lcg': 180.00,
        'tcg': 5.91,
        'vcg': 7.00,
        'density': DENSITIES['GW'],
        'fsm_coeff': {50.0: 0.27, 100.0: 0.0}
    },
}

# Bilge Water
BILGE_TANKS = {
    'T09.20': {
        'name': 'Bilge Water Settling',
        'category': 'Bilge Water',
        'max_volume': 10.4,
        'lcg': 188.38,
        'tcg': -0.73,
        'vcg': 3.97,
        'density': DENSITIES['BILGE'],
        'fsm_coeff': {50.0: 0.12, 100.0: 0.0}
    },
    'T09.22': {
        'name': 'Bilge Water',
        'category': 'Bilge Water',
        'max_volume': 30.5,
        'lcg': 187.07,
        'tcg': -3.20,
        'vcg': 1.74,
        'density': DENSITIES['BILGE'],
        'fsm_coeff': {50.0: 8.71, 100.0: 0.0}
    },
}

# Sludge
SLUDGE_TANKS = {
    'T09.21': {
        'name': 'Sludge',
        'category': 'Sludge',
        'max_volume': 30.4,
        'lcg': 187.03,
        'tcg': 3.22,
        'vcg': 1.73,
        'density': DENSITIES['SLUDGE'],
        'fsm_coeff': {50.0: 8.7, 100.0: 0.0}
    },
}

# 合并所有舱室定义
ALL_TANKS = {}
ALL_TANKS.update(HFO_TANKS)
ALL_TANKS.update(DIESEL_TANKS)
ALL_TANKS.update(LO_TANKS)
ALL_TANKS.update(TW_TANKS)
ALL_TANKS.update(FW_TANKS)
ALL_TANKS.update(BW_TANKS)
ALL_TANKS.update(FIXED_BW_TANKS)
ALL_TANKS.update(GW_TANKS)
ALL_TANKS.update(BILGE_TANKS)
ALL_TANKS.update(SLUDGE_TANKS)

# 固定重量项 (Stores, Crew, Miscellaneous)
# 这些不是舱室，而是固定的重量项，没有容积
FIXED_ITEMS = {
    'Stores': {
        'name': 'Stores',
        'category': 'Fixed Items',
        'max_volume': 0,  # 无容积
        'lcg': 199.20,
        'tcg': 0.00,
        'vcg': 29.05,
        'density': 1.000,
        'fsm_coeff': {100: 0.0}
    },
    'Crew': {
        'name': 'Crew',
        'category': 'Fixed Items',
        'max_volume': 0,  # 无容积
        'lcg': 199.20,
        'tcg': 0.00,
        'vcg': 35.70,
        'density': 1.000,
        'fsm_coeff': {100: 0.0}
    },
    'Miscellaneous': {
        'name': 'Miscellaneous',
        'category': 'Fixed Items',
        'max_volume': 0,  # 无容积
        'lcg': 178.40,
        'tcg': 0.00,
        'vcg': 5.00,
        'density': 1.000,
        'fsm_coeff': {100: 0.0}
    },
}

ALL_TANKS.update(FIXED_ITEMS)

# 舱室类别
TANK_CATEGORIES = [
    'Heavy Fuel Oil',
    'Diesel Oil',
    'Lubricating Oil',
    'Technical Water',
    'Fresh Water',
    'Ballast Water',
    'Fixed FW ballast',
    'Gray Water',
    'Bilge Water',
    'Sludge',
    'Fixed Items',  # 新增类别
]


def get_tank_info(tank_id):
    """获取舱室信息"""
    return ALL_TANKS.get(tank_id, None)


def get_tanks_by_category(category):
    """获取指定类别的所有舱室"""
    return {k: v for k, v in ALL_TANKS.items() if v.get('category') == category}
