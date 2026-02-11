"""
邦金曲线数据解析
Bonjean Curve Data Parser

邦金曲线表示在不同吃水和不同纵向位置处的横剖面面积和对基线的力矩
"""

import numpy as np

def parse_bonjean_curve():
    """
    解析bonjeancurve.txt文件

    返回:
        dict: {
            'x_positions': 纵向位置列表 (距离AP的距离, m)
            'draughts': 吃水列表 (m)
            'areas': 面积数据 (m²) - shape: (n_draughts, n_positions)
            'moments': 对基线的力矩数据 (m³) - shape: (n_draughts, n_positions)
        }
    """

    with open('ship_data/bonjeancurve.txt', 'r') as f:
        lines = f.readlines()

    x_positions = []
    draughts_set = set()
    areas_dict = {}  # {x_position: {draught: area}}
    moments_dict = {}  # {x_position: {draught: moment}}

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # 查找X位置标题行
        if 'X' in line and i+1 < len(lines) and 'AREA' in lines[i+1]:
            # 解析X位置
            parts = line.split()
            current_x_positions = []
            j = 0
            while j < len(parts):
                if parts[j] == 'X' and j+1 < len(parts):
                    try:
                        x_val = float(parts[j+1])
                        current_x_positions.append(x_val)
                        if x_val not in x_positions:
                            x_positions.append(x_val)
                            areas_dict[x_val] = {}
                            moments_dict[x_val] = {}
                    except:
                        pass
                j += 1

            # 跳过标题行和空行
            i += 2
            while i < len(lines) and not lines[i].strip():
                i += 1

            # 读取数据行
            while i < len(lines):
                line = lines[i].strip()
                if not line:
                    i += 1
                    continue
                if 'X' in line:
                    break

                parts = line.split()
                if len(parts) >= 3:
                    try:
                        draught = float(parts[0])
                        draughts_set.add(draught)

                        # 每个X位置有2个值: AREA和MOM BL
                        # 格式: T AREA1 MOM1 AREA2 MOM2 ... T
                        for idx, x_pos in enumerate(current_x_positions):
                            area_idx = 1 + idx * 2
                            mom_idx = 2 + idx * 2
                            if area_idx < len(parts) - 1 and mom_idx < len(parts) - 1:
                                area = float(parts[area_idx])
                                moment = float(parts[mom_idx])
                                areas_dict[x_pos][draught] = area
                                moments_dict[x_pos][draught] = moment
                    except Exception as e:
                        pass
                i += 1
        else:
            i += 1

    # 排序
    x_positions.sort()
    draughts = sorted(list(draughts_set))

    # 转换为numpy数组
    n_draughts = len(draughts)
    n_positions = len(x_positions)

    areas = np.zeros((n_draughts, n_positions))
    moments = np.zeros((n_draughts, n_positions))

    for j, x_pos in enumerate(x_positions):
        for i, draught in enumerate(draughts):
            areas[i, j] = areas_dict[x_pos].get(draught, 0.0)
            moments[i, j] = moments_dict[x_pos].get(draught, 0.0)

    return {
        'x_positions': np.array(x_positions),
        'draughts': np.array(draughts),
        'areas': areas,
        'moments': moments
    }


# 加载数据
BONJEAN_CURVE_DATA = parse_bonjean_curve()

if __name__ == '__main__':
    data = BONJEAN_CURVE_DATA
    print(f"X位置数量: {len(data['x_positions'])}")
    print(f"X位置范围: {data['x_positions'][0]:.2f} - {data['x_positions'][-1]:.2f} m")
    print(f"吃水数量: {len(data['draughts'])}")
    print(f"吃水范围: {data['draughts'][0]:.2f} - {data['draughts'][-1]:.2f} m")
    print(f"面积数据形状: {data['areas'].shape}")
    print(f"力矩数据形状: {data['moments'].shape}")

