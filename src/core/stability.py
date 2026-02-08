"""
稳性计算模块 (Stability Calculation)
计算船舶的稳性参数、GZ曲线、稳性衡准检查等
"""

import numpy as np
from scipy import interpolate
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ship_data.hydrostatic_data import get_hydrostatic_data, get_cross_curves
from ship_data.stability_criteria import get_stability_criteria
from ship_data.ship_particulars import DENSITIES
from ship_data.crosscurves_data import get_crosscurves_data


class StabilityCalculator:
    """稳性计算器"""
    
    def __init__(self, condition='TRANSIT', standard='IMO'):
        """
        初始化稳性计算器
        
        Args:
            condition: 工况类型 ('TRANSIT' 或 'SEMI_SUBMERGED')
            standard: 规范标准 ('IMO', 'DNV', 'CCS')
        """
        self.condition = condition
        self.standard = standard
        self.hydro_data = get_hydrostatic_data(condition)
        self.cross_curves = get_cross_curves(condition)
        self.criteria = get_stability_criteria(condition, standard)
    
    def calculate_kg(self, total_weight, vcg_total, free_surface_moment):
        """
        计算考虑自由液面修正后的KG
        
        Args:
            total_weight: 总重量 (t)
            vcg_total: 总重心垂向位置 (m from BL)
            free_surface_moment: 自由液面力矩 (t·m)
        
        Returns:
            dict: 包含KG, KG_corrected, FSM的字典
        """
        kg = vcg_total
        
        # 自由液面修正
        # ΔKG = FSM / Displacement
        delta_kg = free_surface_moment / total_weight if total_weight > 0 else 0
        kg_corrected = kg + delta_kg
        
        return {
            'kg': kg,
            'kg_corrected': kg_corrected,
            'fsm': free_surface_moment,
            'delta_kg': delta_kg,
        }
    
    def calculate_gm(self, draught, kg_corrected):
        """
        计算初稳性高GM
        
        Args:
            draught: 吃水 (m)
            kg_corrected: 修正后的KG (m)
        
        Returns:
            dict: 包含KB, BM, KM, GM的字典
        """
        # 从静水力数据插值获取VCB和BMT
        draughts = self.hydro_data['draught']
        vcb_values = self.hydro_data['vcb']
        bmt_values = self.hydro_data['bmt']
        
        interp_vcb = interpolate.interp1d(draughts, vcb_values, kind='cubic', fill_value='extrapolate')
        interp_bmt = interpolate.interp1d(draughts, bmt_values, kind='cubic', fill_value='extrapolate')
        
        kb = float(interp_vcb(draught))  # KB = VCB
        bm = float(interp_bmt(draught))  # BM = BMT
        km = kb + bm
        gm = km - kg_corrected
        
        return {
            'kb': kb,
            'bm': bm,
            'km': km,
            'gm': gm,
        }
    
    def calculate_gz_curve(self, displacement, kg_corrected, draught=None, trim=0.0,
                          tank_fsm_data=None, heel_angles=None):
        """
        计算GZ曲线（复原力臂曲线）

        使用Cross Curves数据，根据吃水和trim查询KN值，然后计算GZ

        Args:
            displacement: 排水量 (t)
            kg_corrected: 修正后的KG (m) = KGf
            draught: 吃水 (m)，如果为None则从排水量推算
            trim: 纵倾 (m)，默认为0
            tank_fsm_data: 舱室FSM数据列表，用于计算GZ修正
                          格式: [{'name': str, 'fsm': float, 'fill_pct': float}, ...]
            heel_angles: 横倾角数组 (degrees)，默认为0-60度

        Returns:
            dict: 包含heel_angles, gz_values, kn_values的字典
        """
        if heel_angles is None:
            # 使用Cross Curves中的标准角度
            heel_angles = np.array([0.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0])

        # 如果没有提供吃水，从排水量推算（使用旧方法）
        if draught is None:
            # 从静水力数据推算吃水
            displacements = self.hydro_data['displacement']
            draughts = self.hydro_data['draught']
            interp_draught = interpolate.interp1d(
                displacements, draughts,
                kind='linear', fill_value='extrapolate'
            )
            draught = float(interp_draught(displacement))

        # 获取Cross Curves数据
        cc_data = get_crosscurves_data()

        # 对每个横倾角，查询KN值
        kn_values = []
        for angle in heel_angles:
            kn = cc_data.get_kn(draught, trim, angle)
            kn_values.append(kn)

        kn_values = np.array(kn_values)

        # 计算 KGf * sin(θ)
        heel_angles_rad = np.radians(heel_angles)
        kg_sin_theta = kg_corrected * np.sin(heel_angles_rad)

        # 计算GZ修正（来自自由液面）
        # TODO: 这里需要从GZ Corrections Table查询每个舱在不同横倾角下的修正值
        # 目前简化处理：假设修正值为0
        gz_correction_fsm = np.zeros_like(heel_angles)

        # 如果提供了tank_fsm_data，计算GZ修正
        # 注意：这需要GZ Corrections Table数据，目前暂时使用简化方法
        if tank_fsm_data is not None and displacement > 0:
            # 简化方法：使用FSM / Displacement作为近似修正
            # 实际应该从GZ Corrections Table查询
            total_fsm = sum(tank['fsm'] for tank in tank_fsm_data if 'fsm' in tank)
            # 这是一个简化，实际的GZ修正应该随横倾角变化
            # gz_correction_fsm = np.full_like(heel_angles, total_fsm / displacement, dtype=float)
            pass  # 暂时不应用FSM修正，等待GZ Corrections Table数据

        # 计算GZ = KN - KGf*sin(θ) - GZ_Correction_FSM
        gz_values = kn_values - kg_sin_theta - gz_correction_fsm

        return {
            'heel_angles': heel_angles,
            'gz_values': gz_values,
            'kn_values': kn_values,
            'kg_sin_theta': kg_sin_theta,
            'gz_correction_fsm': gz_correction_fsm,
        }
    
    def calculate_gz_areas(self, heel_angles, gz_values):
        """
        计算GZ曲线下的面积
        
        Args:
            heel_angles: 横倾角数组 (degrees)
            gz_values: GZ值数组 (m)
        
        Returns:
            dict: 包含各区间面积的字典
        """
        # 转换为弧度
        heel_rad = np.radians(heel_angles)
        
        # 使用梯形积分计算面积
        def integrate_area(angle_start, angle_end):
            """计算指定角度区间的面积"""
            mask = (heel_angles >= angle_start) & (heel_angles <= angle_end)
            if np.sum(mask) < 2:
                return 0.0
            angles_subset = heel_rad[mask]
            gz_subset = gz_values[mask]
            # 使用trapezoid代替已弃用的trapz
            try:
                return float(np.trapezoid(gz_subset, angles_subset))
            except AttributeError:
                # 兼容旧版本numpy
                return float(np.trapz(gz_subset, angles_subset))
        
        area_0_30 = integrate_area(0, 30)
        area_0_40 = integrate_area(0, 40)
        area_30_40 = integrate_area(30, 40)
        area_0_25 = integrate_area(0, 25)  # For CCS criteria
        
        return {
            'area_0_30': area_0_30,
            'area_0_40': area_0_40,
            'area_30_40': area_30_40,
            'area_0_25': area_0_25,
        }
    
    def check_stability_criteria(self, gm, gz_curve_data, areas):
        """
        检查稳性衡准
        
        Args:
            gm: 初稳性高 (m)
            gz_curve_data: GZ曲线数据
            areas: GZ曲线面积数据
        
        Returns:
            dict: 衡准检查结果
        """
        heel_angles = gz_curve_data['heel_angles']
        gz_values = gz_curve_data['gz_values']
        
        # 找到最大GZ及其对应角度
        max_gz_idx = np.argmax(gz_values)
        max_gz = gz_values[max_gz_idx]
        angle_max_gz = heel_angles[max_gz_idx]
        
        # 获取特定角度的GZ值
        gz_30 = np.interp(30, heel_angles, gz_values)
        gz_15 = np.interp(15, heel_angles, gz_values)
        
        # 检查各项衡准
        results = {}
        all_passed = True
        
        for criterion_name, criterion in self.criteria.items():
            if not criterion.get('required', True):
                continue
            
            # 获取实际值
            if criterion_name == 'gmt':
                actual_value = gm
            elif criterion_name == 'max_gz':
                actual_value = max_gz
            elif criterion_name == 'angle_max_gz':
                actual_value = angle_max_gz
            elif criterion_name == 'gz_30':
                actual_value = gz_30
            elif criterion_name == 'gz_15':
                actual_value = gz_15
            elif criterion_name in areas:
                actual_value = areas[criterion_name]
            else:
                continue
            
            # 检查是否满足要求
            min_value = criterion.get('min_value', 0)
            passed = actual_value >= min_value
            all_passed = all_passed and passed
            
            results[criterion_name] = {
                'name': criterion['name'],
                'description': criterion['description'],
                'required': min_value,
                'actual': actual_value,
                'unit': criterion.get('unit', ''),
                'passed': passed,
            }
        
        results['all_passed'] = all_passed
        
        return results

