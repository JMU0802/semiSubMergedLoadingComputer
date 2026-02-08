"""
高级总纵强度计算模块 (Advanced Longitudinal Strength Calculation)
基于肋位的精确强度计算，不使用邦金曲线

核心思想：
纵强度计算是力学问题，不是几何问题
- 需要的是"浮力分布函数 b(x)"，而不是精确的每站体积
- 使用静水力参数（DISP, LCB, CP）构造标准浮力分布
- 重量分布来自实际装载数据

计算流程：
1. 构造浮力分布曲线 b(x)：使用抛物线分布 + CP修正
2. 构造重量分布曲线 w(x)：将装载项分配到各肋位
3. 计算净载荷：q(x) = b(x) - w(x)
4. 积分得剪力：S(x) = ∫ q(x) dx
5. 积分得弯矩：M(x) = ∫ S(x) dx
"""

import numpy as np
from typing import Dict, List
from ship_data.ship_particulars import SHIP_PARTICULARS


class AdvancedStrengthCalculator:
    """高级强度计算器 - 基于肋位的精确计算"""
    
    def __init__(self, condition='TRANSIT', frame_spacing=0.8):
        """
        初始化强度计算器
        
        Args:
            condition: 工况类型
            frame_spacing: 肋距 (m)，默认0.8m
        """
        self.condition = condition
        self.lpp = SHIP_PARTICULARS['lpp']  # 垂线间长
        self.frame_spacing = frame_spacing
        
        # 计算肋位数量
        self.n_frames = int(self.lpp / frame_spacing) + 1
        
        # 生成肋位位置 (从AP起算)
        self.frame_positions = np.linspace(0, self.lpp, self.n_frames)
        self.frame_numbers = np.arange(0, self.n_frames)
        
        # 设置许用应力限制
        self._set_allowable_limits()
        
    def _set_allowable_limits(self):
        """设置许用剪力和弯矩限制"""
        if self.condition == 'TRANSIT':
            self.max_sagging_moment = 850000.0  # kN·m
            self.max_hogging_moment = 750000.0  # kN·m
            self.max_shear_force = 45000.0      # kN
        elif self.condition == 'SEMI_SUBMERGED':
            self.max_sagging_moment = 650000.0
            self.max_hogging_moment = 550000.0
            self.max_shear_force = 35000.0
        elif self.condition in ['AFTLOAD', 'SIDELOAD']:
            self.max_sagging_moment = 700000.0
            self.max_hogging_moment = 600000.0
            self.max_shear_force = 40000.0
        else:
            self.max_sagging_moment = 850000.0
            self.max_hogging_moment = 750000.0
            self.max_shear_force = 45000.0
    
    def distribute_weights_to_frames(self, weight_items: List) -> np.ndarray:
        """
        将重量项分配到各肋位

        Args:
            weight_items: 重量项列表，可以是WeightItem对象或字典

        Returns:
            np.ndarray: 每个肋位的重量 (t)
        """
        frame_weights = np.zeros(self.n_frames)

        for item in weight_items:
            # 支持WeightItem对象和字典两种格式
            if hasattr(item, 'weight'):
                weight = item.weight
                lcg = item.lcg
            else:
                weight = item['weight']
                lcg = item['lcg']
            
            # 找到该重量项所在的肋位区间
            if lcg <= 0:
                frame_weights[0] += weight
            elif lcg >= self.lpp:
                frame_weights[-1] += weight
            else:
                # 线性插值分配到相邻两个肋位
                frame_idx = lcg / self.frame_spacing
                lower_idx = int(np.floor(frame_idx))
                upper_idx = int(np.ceil(frame_idx))
                
                if lower_idx == upper_idx:
                    frame_weights[lower_idx] += weight
                else:
                    # 按距离比例分配
                    ratio = frame_idx - lower_idx
                    frame_weights[lower_idx] += weight * (1 - ratio)
                    frame_weights[upper_idx] += weight * ratio
        
        return frame_weights
    
    def calculate_buoyancy_distribution_from_hydrostatic(
        self,
        displacement: float,
        draught: float,
        lcb: float,
        cp: float = 0.85,
        cb: float = 0.80,
        lcf: float = None
    ) -> np.ndarray:
        """
        根据静水力参数构造浮力分布曲线

        改进方法：使用分段函数 + 多参数修正
        - 考虑船型特征（CP, CB）
        - 考虑浮心位置（LCB, LCF）
        - 使用更复杂的分布函数

        Args:
            displacement: 总排水量 (t)
            draught: 平均吃水 (m)
            lcb: 浮心纵向位置 (m from AP)
            cp: 棱形系数，默认0.85
            cb: 方形系数，默认0.80
            lcf: 浮面中心，默认None（使用LCB）

        Returns:
            np.ndarray: 每个肋位的浮力 (t)
        """
        if lcf is None:
            lcf = lcb

        # 归一化位置：x_norm ∈ [0, 1]
        x_norm = self.frame_positions / self.lpp

        # 归一化LCB和LCF
        lcb_norm = lcb / self.lpp
        lcf_norm = lcf / self.lpp

        # === 方法：分段多项式分布 ===
        # 使用4次多项式来模拟真实船型的浮力分布
        # b(x) = a0 + a1*x + a2*x^2 + a3*x^3 + a4*x^4

        # 基于CP和CB构造分布
        # CP影响首尾的尖削程度
        # CB影响整体的丰满程度

        # 使用修正的抛物线分布
        # 中部使用高次多项式，首尾使用指数衰减

        shape_factor = np.zeros_like(x_norm)

        for i, x in enumerate(x_norm):
            if x < 0.15:  # 首部（0-15%）
                # 首部：指数增长
                t = x / 0.15
                shape_factor[i] = 0.3 * (1 - np.exp(-3 * t))
            elif x > 0.85:  # 尾部（85%-100%）
                # 尾部：指数衰减
                t = (1 - x) / 0.15
                shape_factor[i] = 0.3 * (1 - np.exp(-3 * t))
            else:  # 中部（15%-85%）
                # 中部：使用4次多项式
                # 归一化到[-1, 1]
                t = (x - 0.5) / 0.35
                # 4次多项式：1 - a*t^2 - b*t^4
                a = 0.5 * (1 - cp)  # CP影响2次项
                b = 0.3 * (1 - cb)  # CB影响4次项
                shape_factor[i] = 1.0 - a * t**2 - b * t**4

        # 确保非负
        shape_factor = np.maximum(shape_factor, 0.01)

        # === LCB位置修正 ===
        # 计算当前分布的浮心位置
        current_lcb_norm = np.sum(shape_factor * x_norm) / np.sum(shape_factor)
        lcb_error = lcb_norm - current_lcb_norm

        # 如果浮心偏差较大，使用不对称修正
        if abs(lcb_error) > 0.01:  # 偏差超过1%才修正
            # 线性倾斜修正
            tilt = 2 * lcb_error * (x_norm - 0.5)
            shape_factor = shape_factor * (1.0 + tilt)
            shape_factor = np.maximum(shape_factor, 0.01)

            # 再次检查并微调
            current_lcb_norm = np.sum(shape_factor * x_norm) / np.sum(shape_factor)
            lcb_error2 = lcb_norm - current_lcb_norm
            if abs(lcb_error2) > 0.01:
                tilt2 = 1.5 * lcb_error2 * (x_norm - 0.5)
                shape_factor = shape_factor * (1.0 + tilt2)
                shape_factor = np.maximum(shape_factor, 0.01)

        # === 归一化使总浮力 = 总排水量 ===
        total_buoyancy = np.sum(shape_factor) * self.frame_spacing
        frame_buoyancy = shape_factor * (displacement / total_buoyancy) * self.frame_spacing

        return frame_buoyancy
    
    def calculate_weight_distribution_detailed(
        self,
        weight_items: List,
        lightship_distribution: str = 'uniform'
    ) -> Dict:
        """
        详细的重量分布计算

        Args:
            weight_items: 重量项列表
            lightship_distribution: 空船重量分布方式
                - 'uniform': 均匀分布
                - 'parabolic': 抛物线分布（中部重，首尾轻）
                - 'actual': 使用实际分布数据（如果有）

        Returns:
            dict: 包含各类重量分布的详细信息
        """
        frame_weights = np.zeros(self.n_frames)

        # 分类统计
        lightship_weight = 0
        cargo_weight = 0
        ballast_weight = 0
        fuel_weight = 0

        for item in weight_items:
            # 支持WeightItem对象和字典
            if hasattr(item, 'weight'):
                weight = item.weight
                lcg = item.lcg
                name = item.name
            else:
                weight = item['weight']
                lcg = item['lcg']
                name = item.get('name', '')

            # 分类
            if 'lightship' in name.lower() or '空船' in name:
                lightship_weight += weight
                # 空船重量按指定方式分布
                if lightship_distribution == 'uniform':
                    frame_weights += weight / self.n_frames
                elif lightship_distribution == 'parabolic':
                    # 抛物线分布：中部重，首尾轻
                    x_norm = self.frame_positions / self.lpp
                    dist = 4 * x_norm * (1 - x_norm)
                    dist = dist / np.sum(dist)
                    frame_weights += weight * dist
            else:
                # 其他重量：分配到相邻肋位
                if 'ballast' in name.lower() or '压载' in name:
                    ballast_weight += weight
                elif 'fuel' in name.lower() or 'oil' in name.lower() or '油' in name:
                    fuel_weight += weight
                elif 'cargo' in name.lower() or '货' in name:
                    cargo_weight += weight

                # 线性插值分配
                if lcg <= 0:
                    frame_weights[0] += weight
                elif lcg >= self.lpp:
                    frame_weights[-1] += weight
                else:
                    frame_idx = lcg / self.frame_spacing
                    lower_idx = int(np.floor(frame_idx))
                    upper_idx = int(np.ceil(frame_idx))

                    if lower_idx == upper_idx:
                        frame_weights[lower_idx] += weight
                    else:
                        ratio = frame_idx - lower_idx
                        frame_weights[lower_idx] += weight * (1 - ratio)
                        frame_weights[upper_idx] += weight * ratio

        return {
            'frame_weights': frame_weights,
            'lightship_weight': lightship_weight,
            'cargo_weight': cargo_weight,
            'ballast_weight': ballast_weight,
            'fuel_weight': fuel_weight,
            'total_weight': lightship_weight + cargo_weight + ballast_weight + fuel_weight
        }

    def calculate_shear_force_and_bending_moment(
        self,
        weight_items: List,
        displacement: float,
        draught: float,
        lcb: float,
        cp: float = 0.85,
        cb: float = 0.80,
        lcf: float = None,
        lightship_distribution: str = 'uniform'
    ) -> Dict:
        """
        计算每个肋位的剪力和弯矩

        核心算法：
        1. 构造浮力分布 b(x)：抛物线分布 + CP修正
        2. 构造重量分布 w(x)：实际装载数据
        3. 净载荷：q(x) = b(x) - w(x)
        4. 剪力：S(x) = ∫ q(x) dx （梯形积分）
        5. 弯矩：M(x) = ∫ S(x) dx （梯形积分）

        边界条件：
        - 首端（AP）：S(0) = 0, M(0) = 0
        - 尾端（FP）：理论上 S(L) ≈ 0（平衡）

        Args:
            weight_items: 重量项列表
            displacement: 总排水量 (t)
            draught: 平均吃水 (m)
            lcb: 浮心纵向位置 (m from AP)
            cp: 棱形系数（默认0.85）
            cb: 方形系数（默认0.80）
            lcf: 浮面中心（默认None，使用LCB）
            lightship_distribution: 空船重量分布方式

        Returns:
            dict: 包含详细计算结果的字典
        """
        # 1. 计算重量分布 w(x)
        weight_dist = self.calculate_weight_distribution_detailed(
            weight_items,
            lightship_distribution
        )
        frame_weights = weight_dist['frame_weights']

        # 2. 计算浮力分布 b(x)
        frame_buoyancy = self.calculate_buoyancy_distribution_from_hydrostatic(
            displacement, draught, lcb, cp, cb, lcf
        )

        # 3. 计算净载荷 q(x) = b(x) - w(x)
        # 注意符号约定：
        # - 浮力向上为正
        # - 重量向下，所以是负贡献
        # - q(x) > 0 表示该处浮力大于重量（向上的净力）
        net_load = frame_buoyancy - frame_weights

        # 验证总平衡（理论上应该接近0）
        total_net_load = np.sum(net_load)
        balance_error = abs(total_net_load / displacement * 100) if displacement > 0 else 0

        # 4. 计算剪力 S(x) = ∫[0 to x] q(ξ) dξ
        # 从船尾(AP, x=0)向船首(FP, x=L)积分
        # 边界条件：S(0) = 0
        shear_force = np.zeros(self.n_frames)
        for i in range(1, self.n_frames):
            # 梯形法则：∫[x_{i-1} to x_i] q(x)dx ≈ (q_{i-1} + q_i)/2 * Δx
            shear_force[i] = shear_force[i-1] + \
                           (net_load[i-1] + net_load[i]) / 2 * self.frame_spacing

        # 5. 计算弯矩 M(x) = ∫[0 to x] S(ξ) dξ
        # 边界条件：M(0) = 0
        bending_moment = np.zeros(self.n_frames)
        for i in range(1, self.n_frames):
            # 梯形法则：∫[x_{i-1} to x_i] S(x)dx ≈ (S_{i-1} + S_i)/2 * Δx
            bending_moment[i] = bending_moment[i-1] + \
                              (shear_force[i-1] + shear_force[i]) / 2 * self.frame_spacing

        # 6. 单位转换：t → kN, t·m → kN·m
        # 1 t = 1000 kg, 1 kN = 1000 N, g = 9.81 m/s²
        # 1 t = 9.81 kN
        g = 9.81
        shear_force_kn = shear_force * g
        bending_moment_knm = bending_moment * g

        # 7. 找出最大值和位置
        max_sf_abs = np.max(np.abs(shear_force_kn))
        max_sf_idx = np.argmax(np.abs(shear_force_kn))

        max_sagging = np.max(bending_moment_knm)
        max_sagging_idx = np.argmax(bending_moment_knm)

        min_hogging = np.min(bending_moment_knm)
        max_hogging_idx = np.argmin(bending_moment_knm)
        max_hogging_abs = abs(min_hogging)

        # 8. 强度检查
        sf_ok = max_sf_abs <= self.max_shear_force
        sagging_ok = max_sagging <= self.max_sagging_moment
        hogging_ok = max_hogging_abs <= self.max_hogging_moment
        all_ok = sf_ok and sagging_ok and hogging_ok

        # 9. 返回详细结果
        return {
            # === 基本信息 ===
            'frame_numbers': self.frame_numbers,
            'frame_positions': self.frame_positions,
            'frame_spacing': self.frame_spacing,
            'n_frames': self.n_frames,

            # === 载荷分布 ===
            'frame_weights': frame_weights,  # t (每个肋位)
            'frame_buoyancy': frame_buoyancy,  # t (每个肋位)
            'net_load': net_load,  # t (每个肋位)

            # === 重量统计 ===
            'lightship_weight': weight_dist['lightship_weight'],
            'cargo_weight': weight_dist['cargo_weight'],
            'ballast_weight': weight_dist['ballast_weight'],
            'fuel_weight': weight_dist['fuel_weight'],
            'total_weight': weight_dist['total_weight'],

            # === 平衡检查 ===
            'total_buoyancy': displacement,
            'balance_error_percent': balance_error,

            # === 剪力和弯矩 ===
            'shear_force': shear_force_kn,  # kN (每个肋位)
            'bending_moment': bending_moment_knm,  # kN·m (每个肋位)

            # === 最大剪力 ===
            'max_shear_force': max_sf_abs,
            'max_shear_force_frame': int(self.frame_numbers[max_sf_idx]),
            'max_shear_force_position': self.frame_positions[max_sf_idx],

            # === 最大中拱弯矩 (Sagging) ===
            'max_sagging_moment': max_sagging,
            'max_sagging_frame': int(self.frame_numbers[max_sagging_idx]),
            'max_sagging_position': self.frame_positions[max_sagging_idx],

            # === 最大中垂弯矩 (Hogging) ===
            'max_hogging_moment': max_hogging_abs,
            'max_hogging_frame': int(self.frame_numbers[max_hogging_idx]),
            'max_hogging_position': self.frame_positions[max_hogging_idx],

            # === 许用值 ===
            'allowable_shear_force': self.max_shear_force,
            'allowable_sagging_moment': self.max_sagging_moment,
            'allowable_hogging_moment': self.max_hogging_moment,

            # === 检查结果 ===
            'shear_force_ok': sf_ok,
            'sagging_moment_ok': sagging_ok,
            'hogging_moment_ok': hogging_ok,
            'all_ok': all_ok,

            # === 利用率 ===
            'shear_force_utilization': (max_sf_abs / self.max_shear_force * 100) if self.max_shear_force > 0 else 0,
            'sagging_utilization': (max_sagging / self.max_sagging_moment * 100) if self.max_sagging_moment > 0 else 0,
            'hogging_utilization': (max_hogging_abs / self.max_hogging_moment * 100) if self.max_hogging_moment > 0 else 0,
        }

    def get_frame_details(self, results: Dict, frame_number: int) -> Dict:
        """
        获取指定肋位的详细信息

        Args:
            results: calculate_shear_force_and_bending_moment的返回结果
            frame_number: 肋位号

        Returns:
            dict: 该肋位的详细信息
        """
        if frame_number < 0 or frame_number >= self.n_frames:
            raise ValueError(f"Frame number {frame_number} out of range [0, {self.n_frames-1}]")

        idx = frame_number

        return {
            'frame_number': frame_number,
            'position': results['frame_positions'][idx],
            'weight': results['frame_weights'][idx],
            'buoyancy': results['frame_buoyancy'][idx],
            'net_load': results['net_load'][idx],
            'shear_force': results['shear_force'][idx],
            'bending_moment': results['bending_moment'][idx],
        }

    def export_to_table(self, results: Dict) -> List[Dict]:
        """
        将结果导出为表格格式

        Args:
            results: calculate_shear_force_and_bending_moment的返回结果

        Returns:
            list: 表格数据列表
        """
        table_data = []

        for i in range(self.n_frames):
            row = {
                'Frame': int(results['frame_numbers'][i]),
                'Position (m)': round(results['frame_positions'][i], 2),
                'Weight (t)': round(results['frame_weights'][i], 2),
                'Buoyancy (t)': round(results['frame_buoyancy'][i], 2),
                'Net Load (t)': round(results['net_load'][i], 2),
                'Shear Force (kN)': round(results['shear_force'][i], 2),
                'Bending Moment (kN·m)': round(results['bending_moment'][i], 2),
            }
            table_data.append(row)

        return table_data

