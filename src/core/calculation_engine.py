"""
计算引擎 (Calculation Engine)
整合浮态、稳性、强度计算，提供统一的计算接口
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.flotation import FlotationCalculator
from src.core.stability import StabilityCalculator
from src.core.strength import StrengthCalculator
from src.core.loading_condition import LoadingCondition


class CalculationEngine:
    """计算引擎"""
    
    def __init__(self):
        """初始化计算引擎"""
        self.loading_condition = None
        self.results = {}
    
    def set_loading_condition(self, loading_condition):
        """
        设置装载工况
        
        Args:
            loading_condition: LoadingCondition对象
        """
        self.loading_condition = loading_condition
        self.results = {}
    
    def calculate_all(self, standard='IMO'):
        """
        执行完整计算
        
        Args:
            standard: 稳性规范标准 ('IMO', 'DNV', 'CCS')
        
        Returns:
            dict: 完整计算结果
        """
        if not self.loading_condition:
            raise ValueError("Loading condition not set")
        
        condition_type = self.loading_condition.condition_type
        
        # 1. 计算重量和重心
        totals = self.loading_condition.calculate_totals()
        total_weight = totals['total_weight']
        lcg = totals['lcg']
        vcg = totals['vcg']
        tcg = totals['tcg']
        total_fsm = totals['total_fsm']
        
        # 2. 浮态计算
        flotation_calc = FlotationCalculator(condition_type)
        trim_results = flotation_calc.calculate_trim(total_weight, lcg)
        draught_mean = trim_results['draught_mean']
        trim = trim_results.get('trim', 0.0)
        hydro_props = flotation_calc.get_hydrostatic_properties(draught_mean)

        # 3. 稳性计算
        stability_calc = StabilityCalculator(condition_type, standard)

        # 计算KG（考虑自由液面修正）
        kg_results = stability_calc.calculate_kg(total_weight, vcg, total_fsm)
        kg_corrected = kg_results['kg_corrected']

        # 计算GM
        gm_results = stability_calc.calculate_gm(draught_mean, kg_corrected)

        # 准备tank FSM数据（用于GZ修正）
        tank_fsm_data = []
        for item in totals.get('weight_items', []):
            if item.get('fsm', 0) > 0:
                tank_fsm_data.append({
                    'name': item.get('name', ''),
                    'fsm': item.get('fsm', 0),
                })

        # 计算GZ曲线（使用吃水和trim）
        gz_curve = stability_calc.calculate_gz_curve(
            total_weight,
            kg_corrected,
            draught=draught_mean,
            trim=trim,
            tank_fsm_data=tank_fsm_data if tank_fsm_data else None
        )
        
        # 计算GZ曲线面积
        areas = stability_calc.calculate_gz_areas(
            gz_curve['heel_angles'],
            gz_curve['gz_values']
        )
        
        # 检查稳性衡准
        criteria_check = stability_calc.check_stability_criteria(
            gm_results['gm'],
            gz_curve,
            areas
        )
        
        # 4. 强度计算
        strength_calc = StrengthCalculator(condition_type)
        weight_items = self.loading_condition.get_weight_items_list()
        strength_results = strength_calc.calculate_shear_force_and_bending_moment(
            weight_items,
            draught_mean,
            total_weight
        )
        
        # 整合所有结果
        self.results = {
            'condition_name': self.loading_condition.name,
            'condition_type': condition_type,
            'standard': standard,
            
            # 重量和重心
            'weight_summary': totals,
            
            # 浮态结果
            'flotation': {
                **trim_results,
                **hydro_props,
            },
            
            # 稳性结果
            'stability': {
                **kg_results,
                **gm_results,
                'gz_curve': gz_curve,
                'areas': areas,
                'criteria_check': criteria_check,
            },
            
            # 强度结果
            'strength': strength_results,
            
            # 总体评估
            'overall_status': {
                'stability_ok': criteria_check.get('all_passed', False),
                'strength_ok': strength_results.get('all_ok', False),
                'all_ok': (criteria_check.get('all_passed', False) and 
                          strength_results.get('all_ok', False)),
            }
        }
        
        return self.results
    
    def get_results(self):
        """获取计算结果"""
        return self.results
    
    def get_summary(self):
        """
        获取计算结果摘要
        
        Returns:
            dict: 结果摘要
        """
        if not self.results:
            return None
        
        return {
            'condition_name': self.results['condition_name'],
            'displacement': self.results['flotation']['displacement'],
            'draught_mean': self.results['flotation']['draught_mean'],
            'draught_fwd': self.results['flotation']['draught_fwd'],
            'draught_aft': self.results['flotation']['draught_aft'],
            'trim': self.results['flotation']['trim'],
            'gm': self.results['stability']['gm'],
            'max_gz': max(self.results['stability']['gz_curve']['gz_values']),
            'stability_ok': self.results['overall_status']['stability_ok'],
            'strength_ok': self.results['overall_status']['strength_ok'],
            'all_ok': self.results['overall_status']['all_ok'],
        }

