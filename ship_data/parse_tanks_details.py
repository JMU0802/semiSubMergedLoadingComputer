"""
解析 tanksdetails.txt 文件
提取所有舱室的详细信息，包括空间位置和不同装载百分比下的参数
"""

import re
import json


def parse_tanks_details(file_path='ship_data/tanksdetails.txt'):
    """
    解析舱室详细信息文件
    
    Returns:
        dict: 舱室详细信息字典
    """
    
    tanks_details = {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 按舱室分割（每个舱室以 "Compartment ident:" 开始）
    compartments = re.split(r'Compartment ident:', content)[1:]  # 跳过第一个空部分
    
    for comp_text in compartments:
        lines = comp_text.strip().split('\n')
        
        # 提取舱室标识
        tank_id = lines[0].strip()
        
        # 初始化舱室数据
        tank_data = {
            'id': tank_id,
            'description': '',
            'contents': '',
            'density': 0.0,
            'aft_frame': 0.0,
            'aft_position': 0.0,  # m from Frame 0
            'fore_frame': 0.0,
            'fore_position': 0.0,  # m from Frame 0
            'lowest_point': 0.0,  # m above BL
            'highest_point': 0.0,  # m above BL
            'filling_table': []  # 不同装载百分比下的数据
        }
        
        # 解析描述
        for line in lines:
            if 'Compartment descr:' in line:
                tank_data['description'] = line.split(':', 1)[1].strip()
            
            elif 'Contents' in line and 'RHO' in line:
                # 提取内容物和密度
                # 例如: "Contents         : Ballast Water (BW, RHO = 1.025)"
                content_part = line.split(':', 1)[1].strip()
                tank_data['contents'] = content_part
                
                # 提取密度
                rho_match = re.search(r'RHO\s*=\s*([\d.]+)', content_part)
                if rho_match:
                    tank_data['density'] = float(rho_match.group(1))
            
            elif 'Aft end at frame' in line:
                # 例如: "Aft end at frame     3.00 (  2.40 m)"
                match = re.search(r'frame\s+([\d.]+)\s*\(\s*([\d.]+)\s*m\)', line)
                if match:
                    tank_data['aft_frame'] = float(match.group(1))
                    tank_data['aft_position'] = float(match.group(2))
            
            elif 'Fore end at frame' in line:
                # 例如: "Fore end at frame   15.00 ( 12.00 m)"
                match = re.search(r'frame\s+([\d.]+)\s*\(\s*([\d.]+)\s*m\)', line)
                if match:
                    tank_data['fore_frame'] = float(match.group(1))
                    tank_data['fore_position'] = float(match.group(2))
            
            elif 'Lowest point' in line:
                # 例如: "Lowest point        13.00 m above BL"
                match = re.search(r'([\d.]+)\s*m\s*above\s*BL', line)
                if match:
                    tank_data['lowest_point'] = float(match.group(1))
            
            elif 'Highest point' in line:
                # 例如: "Highest point       27.70 m above BL"
                match = re.search(r'([\d.]+)\s*m\s*above\s*BL', line)
                if match:
                    tank_data['highest_point'] = float(match.group(1))
        
        # 解析装载表格
        # 查找表格数据行（格式：数字开头，包含多个浮点数）
        in_table = False
        for line in lines:
            # 跳过表头和分隔线
            if '----' in line or 'FILL' in line or 'filling degree' in line:
                if 'FILL' in line and 'VNET' in line:
                    in_table = True
                continue
            
            if in_table:
                # 尝试解析数据行
                # 格式: FILL H VNET MASS LCG TCG VCG FSM
                # 例如: "  5.0   0.73     39.8   40.8   7.20 17.83 13.37   155.89"
                # 注意TCG可能是负数，格式可能是 "7.20-17.83" 或 "7.20 -17.83"
                
                # 清理行，处理负号粘连的情况
                cleaned_line = line.strip()
                # 将 "数字-数字" 替换为 "数字 -数字"
                cleaned_line = re.sub(r'(\d)(-\d)', r'\1 \2', cleaned_line)
                
                parts = cleaned_line.split()
                
                if len(parts) >= 8:
                    try:
                        fill_data = {
                            'fill_pct': float(parts[0]),
                            'height': float(parts[1]),
                            'volume': float(parts[2]),
                            'mass': float(parts[3]),
                            'lcg': float(parts[4]),
                            'tcg': float(parts[5]),
                            'vcg': float(parts[6]),
                            'fsm': float(parts[7])
                        }
                        tank_data['filling_table'].append(fill_data)
                    except ValueError:
                        # 不是数据行，可能是说明文字
                        pass
        
        # 存储舱室数据
        tanks_details[tank_id] = tank_data
    
    return tanks_details


def save_tanks_details_to_json(tanks_details, output_file='ship_data/tanks_details_data.json'):
    """保存舱室详细信息到JSON文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(tanks_details, f, indent=2, ensure_ascii=False)
    print(f"舱室详细信息已保存到: {output_file}")
    print(f"共解析 {len(tanks_details)} 个舱室")


if __name__ == '__main__':
    # 解析舱室详细信息
    tanks_details = parse_tanks_details()
    
    # 显示统计信息
    print(f"解析完成！共 {len(tanks_details)} 个舱室")
    print()
    
    # 显示前3个舱室的信息作为示例
    for i, (tank_id, tank_data) in enumerate(list(tanks_details.items())[:3]):
        print(f"舱室 {i+1}: {tank_id}")
        print(f"  描述: {tank_data['description']}")
        print(f"  内容物: {tank_data['contents']}")
        print(f"  密度: {tank_data['density']} t/m³")
        print(f"  艉端: Frame {tank_data['aft_frame']} ({tank_data['aft_position']} m)")
        print(f"  首端: Frame {tank_data['fore_frame']} ({tank_data['fore_position']} m)")
        print(f"  最低点: {tank_data['lowest_point']} m above BL")
        print(f"  最高点: {tank_data['highest_point']} m above BL")
        print(f"  装载表格: {len(tank_data['filling_table'])} 个装载状态")
        if tank_data['filling_table']:
            print(f"    100%装载: {tank_data['filling_table'][-1]}")
        print()
    
    # 保存到JSON文件
    save_tanks_details_to_json(tanks_details)

