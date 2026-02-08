"""
装载工况管理模块 (Loading Condition Management)
管理船舶装载工况，包括重量项、舱室装载等
"""

import sys
import os
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ship_data.ship_particulars import SHIP_PARTICULARS, DENSITIES
from ship_data.tank_data import ALL_TANKS


class WeightItem:
    """重量项"""
    
    def __init__(self, name, weight, lcg, vcg, tcg=0.0, fsm=0.0):
        """
        初始化重量项
        
        Args:
            name: 名称
            weight: 重量 (t)
            lcg: 纵向重心 (m from AP)
            vcg: 垂向重心 (m from BL)
            tcg: 横向重心 (m from CL)
            fsm: 自由液面力矩 (t·m)
        """
        self.name = name
        self.weight = weight
        self.lcg = lcg
        self.vcg = vcg
        self.tcg = tcg
        self.fsm = fsm
    
    def to_dict(self):
        """转换为字典"""
        return {
            'name': self.name,
            'weight': self.weight,
            'lcg': self.lcg,
            'vcg': self.vcg,
            'tcg': self.tcg,
            'fsm': self.fsm,
        }


class LoadingCondition:
    """装载工况"""
    
    def __init__(self, name, condition_type='TRANSIT'):
        """
        初始化装载工况
        
        Args:
            name: 工况名称
            condition_type: 工况类型 ('TRANSIT', 'SEMI_SUBMERGED', 'AFTLOAD', 'SIDELOAD')
        """
        self.name = name
        self.condition_type = condition_type
        self.weight_items = []
        
        # 添加空船重量
        self._add_lightship()
    
    def _add_lightship(self):
        """添加空船重量"""
        lightship = WeightItem(
            name='Lightship',
            weight=SHIP_PARTICULARS['lightship'],
            lcg=SHIP_PARTICULARS['lightship_lcg'],
            vcg=SHIP_PARTICULARS['lightship_vcg'],
            tcg=SHIP_PARTICULARS['lightship_tcg'],
            fsm=0.0
        )
        self.weight_items.append(lightship)
    
    def add_weight_item(self, weight_item):
        """添加重量项"""
        self.weight_items.append(weight_item)
    
    def add_tank_loading(self, tank_id, fill_percentage, density=None):
        """
        添加舱室装载
        
        Args:
            tank_id: 舱室编号
            fill_percentage: 装载百分比 (0-100)
            density: 液体密度 (t/m³)，如果为None则根据舱室类型自动选择
        """
        tank_info = ALL_TANKS.get(tank_id)
        if not tank_info:
            raise ValueError(f"Unknown tank: {tank_id}")
        
        # 确定密度
        if density is None:
            tank_type = tank_info['type']
            if tank_type == 'BALLAST':
                density = DENSITIES['seawater']
            elif tank_type == 'FUEL_OIL':
                density = DENSITIES['fuel_oil']
            elif tank_type == 'FRESH_WATER':
                density = DENSITIES['freshwater']
            else:
                density = DENSITIES['seawater']
        
        # 计算重量
        capacity = tank_info['capacity']
        volume = capacity * fill_percentage / 100.0
        weight = volume * density
        
        # 计算自由液面力矩
        # FSM = ρ * i * (1 - fill_percentage/100)^2
        # 简化计算：当装载率在10%-90%时考虑自由液面
        if 10 < fill_percentage < 90:
            fsi = tank_info['fsi']
            fsm = density * fsi / 1000.0  # 转换单位
        else:
            fsm = 0.0
        
        # 创建重量项
        weight_item = WeightItem(
            name=tank_info['name'],
            weight=weight,
            lcg=tank_info['lcg'],
            vcg=tank_info['vcg'],
            tcg=tank_info['tcg'],
            fsm=fsm
        )
        
        self.add_weight_item(weight_item)
    
    def add_cargo(self, name, weight, lcg, vcg, tcg=0.0):
        """
        添加货物
        
        Args:
            name: 货物名称
            weight: 重量 (t)
            lcg: 纵向重心 (m from AP)
            vcg: 垂向重心 (m from BL)
            tcg: 横向重心 (m from CL)
        """
        cargo = WeightItem(name, weight, lcg, vcg, tcg, 0.0)
        self.add_weight_item(cargo)
    
    def calculate_totals(self):
        """
        计算总重量和重心
        
        Returns:
            dict: 包含总重量、重心位置、自由液面力矩的字典
        """
        total_weight = 0.0
        total_moment_lcg = 0.0
        total_moment_vcg = 0.0
        total_moment_tcg = 0.0
        total_fsm = 0.0
        
        for item in self.weight_items:
            total_weight += item.weight
            total_moment_lcg += item.weight * item.lcg
            total_moment_vcg += item.weight * item.vcg
            total_moment_tcg += item.weight * item.tcg
            total_fsm += item.fsm
        
        if total_weight > 0:
            lcg = total_moment_lcg / total_weight
            vcg = total_moment_vcg / total_weight
            tcg = total_moment_tcg / total_weight
        else:
            lcg = vcg = tcg = 0.0
        
        return {
            'total_weight': total_weight,
            'lcg': lcg,
            'vcg': vcg,
            'tcg': tcg,
            'total_fsm': total_fsm,
            'weight_items': [item.to_dict() for item in self.weight_items],
        }
    
    def get_weight_items_list(self):
        """获取重量项列表（用于强度计算）"""
        return [{'weight': item.weight, 'lcg': item.lcg} for item in self.weight_items]

