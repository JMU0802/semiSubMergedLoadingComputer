"""
船上稳性计算模块 (Onboard Stability Calculation)
实现Form 0, 1, 2的计算流程

基于装载手册 3.8 Determination of stability on board
"""

import numpy as np
from typing import Dict, List, Tuple
from ship_data.tank_data import get_tank_info
from ship_data.ship_particulars import SHIP_PARTICULARS


class OnboardStabilityCalculator:
    """船上稳性计算类"""
    
    def __init__(self):
        """初始化船上稳性计算器"""
        self.weight_items = []
        self.lightship_added = False
        
    def reset(self):
        """重置计算器"""
        self.weight_items = []
        self.lightship_added = False
        
    def add_lightship(self):
        """添加空船重量"""
        if not self.lightship_added:
            self.add_weight_item(
                name="Lightship",
                weight=SHIP_PARTICULARS['lightship'],
                lcg=SHIP_PARTICULARS['lightship_lcg'],
                vcg=SHIP_PARTICULARS['lightship_vcg'],
                tcg=SHIP_PARTICULARS['lightship_tcg'],
                fsm=0.0,
                item_type="LIGHTSHIP"
            )
            self.lightship_added = True
            
    def add_weight_item(
        self,
        name: str,
        weight: float,
        lcg: float,
        vcg: float,
        tcg: float = 0.0,
        fsm: float = 0.0,
        item_type: str = "CARGO"
    ):
        """
        添加重量项 (Form 1)
        
        Args:
            name: 重量项名称
            weight: 重量 (t)
            lcg: 纵向重心 (m, from AP)
            vcg: 垂向重心 (m, from BL)
            tcg: 横向重心 (m, from CL, port is negative)
            fsm: 自由液面力矩 (t·m)
            item_type: 类型 (LIGHTSHIP/TANK/CARGO/CREW/PROVISION)
        """
        item = {
            'name': name,
            'weight': weight,
            'lcg': lcg,
            'vcg': vcg,
            'tcg': tcg,
            'fsm': fsm,
            'type': item_type,
            'mv': weight * vcg,  # 垂向力矩
            'ml': weight * lcg,  # 纵向力矩
            'mt': weight * tcg,  # 横向力矩
        }
        self.weight_items.append(item)
        
    def add_tank_loading(self, tank_id: str, fill_percentage: float):
        """
        添加舱室装载 (Form 0 -> Form 1)

        Args:
            tank_id: 舱室ID
            fill_percentage: 装载率 (0-100)
        """
        tank_info = get_tank_info(tank_id)
        if tank_info is None:
            raise ValueError(f"Tank {tank_id} not found")

        # 根据舱室类型确定密度
        tank_type = tank_info['type']
        if tank_type == 'BALLAST':
            density = 1.025  # 海水
        elif tank_type == 'FUEL':
            density = 0.950  # 燃油
        elif tank_type == 'FRESHWATER':
            density = 1.000  # 淡水
        else:
            density = 1.025  # 默认海水

        # 计算实际装载量
        fill_ratio = fill_percentage / 100.0
        weight = tank_info['capacity'] * fill_ratio * density

        # 自由液面力矩 (10%-90%之间才有)
        if 10 <= fill_percentage <= 90:
            fsm = tank_info['fsi'] * density / 1.025
        else:
            fsm = 0.0

        self.add_weight_item(
            name=f"{tank_id} ({fill_percentage}%)",
            weight=weight,
            lcg=tank_info['lcg'],
            vcg=tank_info['vcg'],
            tcg=tank_info['tcg'],
            fsm=fsm,
            item_type="TANK"
        )
        
    def calculate_form1_results(self) -> Dict:
        """
        计算Form 1结果（重量和力矩计算）
        
        Returns:
            Form 1计算结果
        """
        if not self.lightship_added:
            self.add_lightship()
            
        # 汇总计算
        total_weight = sum(item['weight'] for item in self.weight_items)  # (1)
        total_ml = sum(item['ml'] for item in self.weight_items)  # (2)
        total_mv = sum(item['mv'] for item in self.weight_items)  # (3)
        total_fsm = sum(item['fsm'] for item in self.weight_items)  # (4)
        total_mt = sum(item['mt'] for item in self.weight_items)
        
        # 重心计算
        vcg = total_mv / total_weight if total_weight > 0 else 0  # (5)
        lcg = total_ml / total_weight if total_weight > 0 else 0  # (6)
        tcg = total_mt / total_weight if total_weight > 0 else 0
        
        # 自由液面修正
        free_surface_correction = total_fsm / total_weight if total_weight > 0 else 0  # (7)
        
        return {
            'weight_items': self.weight_items.copy(),
            'displacement': total_weight,  # (1)
            'total_ml': total_ml,  # (2)
            'total_mv': total_mv,  # (3)
            'total_fsm': total_fsm,  # (4)
            'vcg': vcg,  # (5) - KG
            'lcg': lcg,  # (6)
            'tcg': tcg,
            'free_surface_correction': free_surface_correction,  # (7) - dGM
        }
        
    def calculate_form2_stability(
        self,
        form1_results: Dict,
        hydrostatic_calculator,
        water_density: float = 1.025
    ) -> Dict:
        """
        计算Form 2结果（稳性和纵倾计算）
        
        Args:
            form1_results: Form 1的计算结果
            hydrostatic_calculator: 静水力计算器
            water_density: 水密度 (t/m³)
            
        Returns:
            Form 2计算结果
        """
        # 从Form 1获取数据
        displacement = form1_results['displacement']  # (1)
        lcg = form1_results['lcg']  # (6)
        vcg = form1_results['vcg']  # (5) = KG
        d_gm = form1_results['free_surface_correction']  # (7)
        
        # 密度修正
        if water_density != 1.025:
            displacement_corrected = displacement * water_density / 1.025
        else:
            displacement_corrected = displacement
            
        # 从静水力表获取参数
        hydro_params = hydrostatic_calculator.get_hydrostatic_properties_by_displacement(
            displacement_corrected
        )
        
        draught = hydro_params['draught']  # (8)
        kmt = hydro_params['kmt']  # (9) - 横稳心高
        lcb = hydro_params['lcb']  # (11)
        mct = hydro_params['mct']  # (13)
        lca = hydro_params['lcf']  # (16)
        
        # 稳性计算
        gm0 = kmt - vcg  # (10) - 初稳性高（固体）
        gmf = gm0 - d_gm  # 流体稳性高
        kgf = vcg + d_gm  # (19) - 修正重心高度
        
        # 纵倾计算
        trim_arm = lcb - lcg  # (12)
        trim_moment = trim_arm * displacement  # (14)
        trim_cm = trim_moment / mct if mct > 0 else 0  # 纵倾 (cm)
        trim = trim_cm / 100.0  # (15) 纵倾 (m)
        
        # 首尾吃水计算
        # Ta = Draught + LCA * trim / Lpp
        lpp = SHIP_PARTICULARS['lpp']
        draught_aft = draught + lca * trim / lpp  # (17)
        draught_fwd = draught_aft - trim  # (18)
        
        return {
            'displacement': displacement,  # (1)
            'lcg': lcg,  # (6)
            'vcg': vcg,  # (5) = KG
            'free_surface_correction': d_gm,  # (7)
            'draught': draught,  # (8)
            'kmt': kmt,  # (9)
            'gm0': gm0,  # (10)
            'gmf': gmf,  # GM fluid
            'lcb': lcb,  # (11)
            'trim_arm': trim_arm,  # (12)
            'mct': mct,  # (13)
            'trim_moment': trim_moment,  # (14)
            'trim': trim,  # (15)
            'lca': lca,  # (16)
            'draught_aft': draught_aft,  # (17)
            'draught_fwd': draught_fwd,  # (18)
            'kgf': kgf,  # (19)
            'water_density': water_density,
        }

