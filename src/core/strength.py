"""
强度计算模块 (Strength Calculation)
计算船舶纵向强度，包括剪力、弯矩
使用精确的邦金曲线和重量分布计算
"""

import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ship_data.ship_particulars import SHIP_PARTICULARS, DENSITIES
from ship_data.frame_data import FRAME_POSITION_DATA, LIGHTSHIP_WEIGHT_DATA
from ship_data.tanks_details_data import get_tank_info
from src.core.buoyancy_calculator import BuoyancyCalculator


class StrengthCalculator:
    """强度计算器"""
    
    def __init__(self, condition='TRANSIT'):
        """
        初始化强度计算器
        
        Args:
            condition: 工况类型 ('TRANSIT', 'SEMI_SUBMERGED', 'AFTLOAD', 'SIDELOAD')
        """
        self.condition = condition
        self.lpp = SHIP_PARTICULARS['lpp']
        
        # 设置许用应力限制 (根据Section 3.4)
        self._set_allowable_limits()
    
    def _set_allowable_limits(self):
        """设置许用剪力和弯矩限制"""
        if self.condition == 'TRANSIT':
            # 航行工况 (Section 3.4.1)
            self.max_sagging_moment = 850000.0  # 中拱弯矩 (kN·m)
            self.max_hogging_moment = 750000.0  # 中垂弯矩 (kN·m)
            self.max_shear_force = 45000.0      # 剪力 (kN)
        elif self.condition == 'SEMI_SUBMERGED':
            # 半潜工况 (Section 3.4.2)
            self.max_sagging_moment = 650000.0
            self.max_hogging_moment = 550000.0
            self.max_shear_force = 35000.0
        elif self.condition in ['AFTLOAD', 'SIDELOAD']:
            # 装载工况 (Section 3.4.3)
            self.max_sagging_moment = 700000.0
            self.max_hogging_moment = 600000.0
            self.max_shear_force = 40000.0
        else:
            # 默认值
            self.max_sagging_moment = 850000.0
            self.max_hogging_moment = 750000.0
            self.max_shear_force = 45000.0
    
    def calculate_lightship_weight_distribution(self):
        """
        计算空船重量沿船长的分布
        使用梯形积分并缩放到精确的空船重量

        Returns:
            dict: 包含positions, weights, weight_density
        """
        frames = FRAME_POSITION_DATA['frames']
        positions = FRAME_POSITION_DATA['positions']
        weight_densities = LIGHTSHIP_WEIGHT_DATA['weights']  # t/m (相对分布)

        # 计算每个Frame的重量（使用梯形积分）
        weights = np.zeros(len(frames))
        for i in range(1, len(frames)):
            dx = positions[i] - positions[i-1]
            # 梯形积分: (f[i-1] + f[i]) / 2 * dx
            weights[i] = (weight_densities[i-1] + weight_densities[i]) / 2.0 * dx

        # 计算总重量
        total_weight_raw = np.sum(weights)

        # 缩放使总重量=20871.40 t（空船重量）
        target_lightship_weight = 20871.40
        if total_weight_raw > 0:
            scale_factor = target_lightship_weight / total_weight_raw
            weights *= scale_factor
            weight_densities_scaled = weight_densities * scale_factor
        else:
            weight_densities_scaled = weight_densities.copy()

        return {
            'frames': frames,
            'positions': positions,
            'weights': weights,
            'weight_density': weight_densities_scaled
        }

    def distribute_tank_weight_along_ship(self, tank_id, tank_weight, tank_info):
        """
        将舱室重量分布到船长方向

        Args:
            tank_id: 舱室ID
            tank_weight: 舱室重量 (t)
            tank_info: 舱室详细信息

        Returns:
            dict: 包含aft_position, fore_position, weight_density
        """
        if tank_info is None:
            return None

        # 获取舱室的艏艉位置
        aft_frame = tank_info['aft_frame']
        fore_frame = tank_info['fore_frame']
        aft_pos = tank_info['aft_position']
        fore_pos = tank_info['fore_position']

        # 计算舱室长度
        length = fore_pos - aft_pos

        if length <= 0:
            return None

        # 均匀分布重量密度
        weight_density = tank_weight / length  # t/m

        return {
            'aft_position': aft_pos,
            'fore_position': fore_pos,
            'weight_density': weight_density
        }

    def calculate_total_weight_distribution(self, weight_items):
        """
        计算总重量分布（空船+舱室）

        Args:
            weight_items: 重量项列表，每项包含 {'name': str, 'weight': float, 'lcg': float, ...}

        Returns:
            dict: 包含positions, weights, weight_density
        """
        frame_positions = FRAME_POSITION_DATA['positions']
        weight_density = np.zeros(len(frame_positions))

        # 1. 添加空船重量分布
        lightship_dist = self.calculate_lightship_weight_distribution()
        weight_density += lightship_dist['weight_density']

        # 2. 添加舱室重量分布
        total_tanks_distributed = 0.0
        tanks_with_info = 0
        tanks_without_info = 0

        for item in weight_items:
            # 支持字典和WeightItem对象两种格式
            if hasattr(item, 'weight'):
                # WeightItem对象
                tank_weight = item.weight
                tank_id = item.name
            else:
                # 字典格式
                tank_weight = item.get('weight', 0)
                tank_id = item.get('name', '')

            if tank_weight <= 0:
                continue

            # 获取舱室信息
            tank_info = get_tank_info(tank_id)

            if tank_info is None:
                # 使用LCG作为中心，将重量分布到一个合理的长度范围
                if hasattr(item, 'lcg'):
                    lcg = item.lcg
                else:
                    lcg = item.get('lcg', 0)

                # 对于没有详细信息的舱室，将其重量均匀分布到整个船长
                # 这样可以避免产生异常的密度峰值
                # 使用与空船重量相同的分布模式
                total_length = frame_positions[-1] - frame_positions[0]
                uniform_density = tank_weight / total_length

                # 将密度添加到所有Frame
                weight_density += uniform_density
                total_tanks_distributed += tank_weight
                tanks_without_info += 1

                print(f"  舱室 {tank_id}: {tank_weight:.1f}t 均匀分布到整船 ({total_length:.1f}m), 密度: {uniform_density:.2f} t/m")
                continue

            # 分布舱室重量
            tank_dist = self.distribute_tank_weight_along_ship(tank_id, tank_weight, tank_info)

            if tank_dist is None:
                continue

            # 将舱室重量密度添加到对应的Frame区间
            aft_pos = tank_dist['aft_position']
            fore_pos = tank_dist['fore_position']
            wd = tank_dist['weight_density']

            # 找到覆盖的Frame范围
            for i in range(len(frame_positions)):
                if frame_positions[i] >= aft_pos and frame_positions[i] <= fore_pos:
                    weight_density[i] += wd

            total_tanks_distributed += tank_weight
            tanks_with_info += 1

        # 计算每个Frame的重量（使用梯形积分）
        weights = np.zeros(len(frame_positions))
        for i in range(1, len(frame_positions)):
            dx = frame_positions[i] - frame_positions[i-1]
            # 梯形积分: (f[i-1] + f[i]) / 2 * dx
            weights[i] = (weight_density[i-1] + weight_density[i]) / 2.0 * dx

        # 计算总重量并缩放使其精确匹配目标值
        total_weight_calculated = np.sum(weights)
        target_total_weight = 20871.40 + total_tanks_distributed  # 空船 + 舱室

        if total_weight_calculated > 0:
            scale_factor = target_total_weight / total_weight_calculated
            weights *= scale_factor
            weight_density *= scale_factor
        else:
            scale_factor = 1.0

        return {
            'positions': frame_positions,
            'weights': weights,
            'weight_density': weight_density,
            'total_tanks_distributed': total_tanks_distributed,
            'tanks_with_info': tanks_with_info,
            'tanks_without_info': tanks_without_info
        }
    
    def calculate_buoyancy_distribution(self, draught_mean, trim, weight_dist, calibration_factor=1.006):
        """
        计算浮力沿船长的分布
        使用邦金曲线和纵倾修正，并调整使浮力=重力且LCB=LCG

        Args:
            draught_mean: 平均吃水 (m)
            trim: 纵倾 (m, 正值表示尾倾)
            weight_dist: 重量分布字典
            calibration_factor: 校准系数 (默认1.006)

        Returns:
            dict: 包含positions, buoyancies, buoyancy_density
        """
        # 初始化浮力计算器
        buoyancy_calc = BuoyancyCalculator(calibration_factor=calibration_factor)

        # 获取Frame位置
        frame_positions = FRAME_POSITION_DATA['positions']

        # 计算每个Frame的吃水（考虑纵倾）
        # AP位置 = 4.24m, FP位置 = 216.37m, LPP = 212.13m
        ap_position = 4.24
        lpp = 212.13

        # 计算每个Frame的吃水
        draughts_at_frames = []
        x_positions = []
        buoyancy_densities = []

        for pos in frame_positions:
            # 计算相对于AP的位置
            x_from_ap = pos - ap_position
            # 计算该位置的吃水（纵倾修正）
            # trim > 0: 尾倾，船首吃水减小
            draught_local = draught_mean - trim * (0.5 - x_from_ap / lpp)
            draughts_at_frames.append(draught_local)
            x_positions.append(pos)

            # 使用邦金曲线计算该位置的横剖面面积
            # get_area_at_station 需要 x_position (from Frame 0) 和 draught
            area = buoyancy_calc.get_area_at_station(pos, draught_local)

            # 浮力密度 = 面积 × 密度 × 校准系数
            rho = 1.025  # 海水密度 t/m³
            buoyancy_density = area * rho * calibration_factor  # t/m
            buoyancy_densities.append(buoyancy_density)

        # 转换为numpy数组
        buoyancy_density_at_frames = np.array(buoyancy_densities)

        # 计算每个Frame的浮力（使用梯形积分）
        buoyancies = np.zeros(len(frame_positions))
        for i in range(1, len(frame_positions)):
            dx = frame_positions[i] - frame_positions[i-1]
            # 梯形积分: (f[i-1] + f[i]) / 2 * dx
            buoyancies[i] = (buoyancy_density_at_frames[i-1] + buoyancy_density_at_frames[i]) / 2.0 * dx

        # 计算总浮力和浮心位置
        total_buoyancy_before = np.sum(buoyancies)
        lcb_before = np.sum(buoyancies * frame_positions) / total_buoyancy_before if total_buoyancy_before > 0 else 0.0

        # 计算重力的总量和重心位置
        total_weight = np.sum(weight_dist['weights'])
        lcg = np.sum(weight_dist['weights'] * weight_dist['positions']) / total_weight if total_weight > 0 else 0.0

        # 调整浮力分布使其满足：
        # 1. 总浮力 = 总重力（垂向力平衡）
        # 2. 浮力重心 = 重力重心（力矩平衡）

        W = total_weight
        LCG = lcg

        # 步骤1：缩放使总浮力=总重力
        if total_buoyancy_before > 0:
            k1 = W / total_buoyancy_before
            buoyancy_density_at_frames *= k1
            for i in range(1, len(frame_positions)):
                dx = frame_positions[i] - frame_positions[i-1]
                buoyancies[i] = (buoyancy_density_at_frames[i-1] + buoyancy_density_at_frames[i]) / 2.0 * dx

        # 步骤2：叠加线性分布使LCB=LCG
        # 计算x_ref使得 ∫(x-x_ref)dx = 0
        total_length = 0.0
        weighted_length = 0.0
        for i in range(1, len(frame_positions)):
            dx = frame_positions[i] - frame_positions[i-1]
            x_mid = (frame_positions[i-1] + frame_positions[i]) / 2.0
            total_length += dx
            weighted_length += x_mid * dx

        x_ref = weighted_length / total_length if total_length > 0 else (frame_positions[0] + frame_positions[-1]) / 2.0

        # 计算需要的力矩调整量
        delta_moment = W * LCG - np.sum(buoyancies * frame_positions)

        # 计算 ∫x*(x-x_ref)dx
        I_moment = 0.0
        for i in range(1, len(frame_positions)):
            dx = frame_positions[i] - frame_positions[i-1]
            x1 = frame_positions[i-1]
            x2 = frame_positions[i]
            I_moment += (x2**3 - x1**3) / 3.0 - x_ref * (x2**2 - x1**2) / 2.0

        # 求解a
        if abs(I_moment) > 1e-6:
            a = delta_moment / I_moment
        else:
            a = 0.0

        # 应用线性调整
        for i in range(len(frame_positions)):
            buoyancy_density_at_frames[i] += a * (frame_positions[i] - x_ref)

        # 重新计算浮力
        for i in range(1, len(frame_positions)):
            dx = frame_positions[i] - frame_positions[i-1]
            buoyancies[i] = (buoyancy_density_at_frames[i-1] + buoyancy_density_at_frames[i]) / 2.0 * dx

        return {
            'positions': frame_positions,
            'buoyancies': buoyancies,
            'buoyancy_density': buoyancy_density_at_frames,
            'total_buoyancy_before_adjust': total_buoyancy_before,
            'lcb_before_adjust': lcb_before
        }
    
    def calculate_shear_force_and_bending_moment(self, weight_items, draught, displacement, trim=0.0):
        """
        计算剪力和弯矩曲线
        使用精确的重量分布和浮力分布（基于邦金曲线）

        Args:
            weight_items: 重量项列表
            draught: 平均吃水 (m)
            displacement: 总排水量 (t)
            trim: 纵倾 (m, 默认0)

        Returns:
            dict: 包含站位、剪力、弯矩的字典
        """
        # 计算重量分布
        weight_dist = self.calculate_total_weight_distribution(weight_items)
        positions = weight_dist['positions']
        weight_density = weight_dist['weight_density']

        # 计算浮力分布
        buoyancy_dist = self.calculate_buoyancy_distribution(
            draught, trim, weight_dist, calibration_factor=1.006
        )
        buoyancy_density = buoyancy_dist['buoyancy_density']

        # 计算载荷分布 q(x) = weight_density(x) - buoyancy_density(x)
        load_density = weight_density - buoyancy_density

        # 计算剪力 V(x) = ∫q(ξ)dξ from 0 to x (使用梯形积分)
        shear_force = np.zeros(len(positions))
        for i in range(1, len(positions)):
            dx = positions[i] - positions[i-1]
            # 梯形积分
            dV = (load_density[i-1] + load_density[i]) / 2.0 * dx
            shear_force[i] = shear_force[i-1] + dV

        # 计算弯矩 M(x) = ∫V(ξ)dξ from 0 to x (使用梯形积分)
        bending_moment = np.zeros(len(positions))
        for i in range(1, len(positions)):
            dx = positions[i] - positions[i-1]
            # 梯形积分
            dM = (shear_force[i-1] + shear_force[i]) / 2.0 * dx
            bending_moment[i] = bending_moment[i-1] + dM

        # 转换单位：t -> kN, t·m -> kN·m (1 t = 9.81 kN)
        shear_force_kn = shear_force * 9.81
        bending_moment_knm = bending_moment * 9.81

        # 找到最大值
        max_sf_abs = np.max(np.abs(shear_force_kn))
        max_sf_pos = np.max(shear_force_kn)
        max_sf_neg = np.min(shear_force_kn)

        max_bm_pos = np.max(bending_moment_knm)  # 中拱（sagging）
        max_bm_neg = np.min(bending_moment_knm)  # 中垂（hogging）

        # 找到最大值位置
        idx_max_sf = np.argmax(np.abs(shear_force_kn))
        idx_max_sagging = np.argmax(bending_moment_knm)
        idx_max_hogging = np.argmin(bending_moment_knm)

        # 检查边界条件
        v_at_0 = shear_force[0]
        v_at_l = shear_force[-1]
        m_at_0 = bending_moment[0]
        m_at_l = bending_moment[-1]

        # 检查是否超过许用值
        shear_force_ok = max_sf_abs <= self.max_shear_force
        sagging_moment_ok = max_bm_pos <= self.max_sagging_moment
        hogging_moment_ok = abs(max_bm_neg) <= self.max_hogging_moment

        all_ok = shear_force_ok and sagging_moment_ok and hogging_moment_ok

        return {
            'stations': positions,
            'shear_force': shear_force_kn,  # kN
            'bending_moment': bending_moment_knm,  # kN·m
            'load_density': load_density,  # t/m
            'weight_density': weight_density,  # t/m
            'buoyancy_density': buoyancy_density,  # t/m

            # 最大值
            'max_shear_force': max_sf_abs,  # kN
            'max_shear_force_positive': max_sf_pos,  # kN
            'max_shear_force_negative': abs(max_sf_neg),  # kN
            'max_sagging_moment': max_bm_pos,  # kN·m (中拱)
            'max_hogging_moment': abs(max_bm_neg),  # kN·m (中垂)

            # 最大值位置
            'position_max_shear': positions[idx_max_sf],  # m
            'position_max_sagging': positions[idx_max_sagging],  # m
            'position_max_hogging': positions[idx_max_hogging],  # m

            # 边界条件检查
            'boundary_check': {
                'V(0)': v_at_0,
                'V(L)': v_at_l,
                'M(0)': m_at_0,
                'M(L)': m_at_l,
            },

            # 许用值检查
            'shear_force_ok': shear_force_ok,
            'sagging_moment_ok': sagging_moment_ok,
            'hogging_moment_ok': hogging_moment_ok,
            'all_ok': all_ok,

            # 许用限制
            'allowable_shear_force': self.max_shear_force,
            'allowable_sagging_moment': self.max_sagging_moment,
            'allowable_hogging_moment': self.max_hogging_moment,
        }
    
    def get_allowable_limits(self):
        """获取许用限制值"""
        return {
            'max_sagging_moment': self.max_sagging_moment,
            'max_hogging_moment': self.max_hogging_moment,
            'max_shear_force': self.max_shear_force,
        }

