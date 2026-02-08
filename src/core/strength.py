"""
强度计算模块 (Strength Calculation)
计算船舶纵向强度，包括剪力、弯矩
根据装载手册 Section 3.4
"""

import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ship_data.ship_particulars import SHIP_PARTICULARS, DENSITIES


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
    
    def calculate_weight_distribution(self, weight_items):
        """
        计算重量沿船长的分布
        
        Args:
            weight_items: 重量项列表，每项包含 {'weight': float, 'lcg': float}
        
        Returns:
            dict: 包含站位、重量分布、浮力分布的字典
        """
        # 将船长分为20个站位
        n_stations = 21
        stations = np.linspace(0, self.lpp, n_stations)
        station_spacing = self.lpp / (n_stations - 1)
        
        # 初始化每个站位的重量
        weight_distribution = np.zeros(n_stations)
        
        # 将每个重量项分配到最近的站位
        for item in weight_items:
            weight = item['weight']
            lcg = item['lcg']
            
            # 找到最近的站位
            station_idx = int(np.round(lcg / station_spacing))
            station_idx = np.clip(station_idx, 0, n_stations - 1)
            
            weight_distribution[station_idx] += weight
        
        return {
            'stations': stations,
            'weight_distribution': weight_distribution,
            'station_spacing': station_spacing,
        }
    
    def calculate_buoyancy_distribution(self, draught, displacement):
        """
        计算浮力沿船长的分布
        
        Args:
            draught: 平均吃水 (m)
            displacement: 总排水量 (t)
        
        Returns:
            np.array: 浮力分布 (t/station)
        """
        # 简化模型：假设浮力均匀分布
        # 实际应用中应根据船体型线计算
        n_stations = 21
        buoyancy_distribution = np.ones(n_stations) * (displacement / n_stations)
        
        # 考虑船首船尾的浮力减小
        # 使用抛物线分布近似
        x = np.linspace(0, 1, n_stations)
        shape_factor = 1.0 - 0.3 * (2 * x - 1) ** 2  # 中部浮力大，首尾浮力小
        buoyancy_distribution *= shape_factor
        
        # 归一化使总浮力等于排水量
        buoyancy_distribution *= displacement / np.sum(buoyancy_distribution)
        
        return buoyancy_distribution
    
    def calculate_shear_force_and_bending_moment(self, weight_items, draught, displacement):
        """
        计算剪力和弯矩曲线
        
        Args:
            weight_items: 重量项列表
            draught: 平均吃水 (m)
            displacement: 总排水量 (t)
        
        Returns:
            dict: 包含站位、剪力、弯矩的字典
        """
        # 计算重量分布
        weight_dist = self.calculate_weight_distribution(weight_items)
        stations = weight_dist['stations']
        weights = weight_dist['weight_distribution']
        spacing = weight_dist['station_spacing']
        
        # 计算浮力分布
        buoyancy = self.calculate_buoyancy_distribution(draught, displacement)
        
        # 计算载荷分布 (浮力 - 重量)
        load_distribution = buoyancy - weights
        
        # 计算剪力 (从船首向船尾积分)
        shear_force = np.zeros_like(stations)
        for i in range(1, len(stations)):
            shear_force[i] = shear_force[i-1] + load_distribution[i-1] * spacing
        
        # 计算弯矩 (从船首向船尾积分剪力)
        bending_moment = np.zeros_like(stations)
        for i in range(1, len(stations)):
            bending_moment[i] = bending_moment[i-1] + shear_force[i-1] * spacing
        
        # 转换单位：t·m -> kN·m (1 t·m = 9.81 kN·m)
        shear_force_kn = shear_force * 9.81
        bending_moment_knm = bending_moment * 9.81
        
        # 检查是否超过许用值
        max_sf = np.max(np.abs(shear_force_kn))
        max_sagging = np.max(bending_moment_knm)
        max_hogging = np.min(bending_moment_knm)
        
        return {
            'stations': stations,
            'shear_force': shear_force_kn,  # kN
            'bending_moment': bending_moment_knm,  # kN·m
            'max_shear_force': max_sf,
            'max_sagging_moment': max_sagging,
            'max_hogging_moment': abs(max_hogging),
            'shear_force_ok': max_sf <= self.max_shear_force,
            'sagging_moment_ok': max_sagging <= self.max_sagging_moment,
            'hogging_moment_ok': abs(max_hogging) <= self.max_hogging_moment,
            'all_ok': (max_sf <= self.max_shear_force and 
                      max_sagging <= self.max_sagging_moment and
                      abs(max_hogging) <= self.max_hogging_moment),
        }
    
    def get_allowable_limits(self):
        """获取许用限制值"""
        return {
            'max_sagging_moment': self.max_sagging_moment,
            'max_hogging_moment': self.max_hogging_moment,
            'max_shear_force': self.max_shear_force,
        }

