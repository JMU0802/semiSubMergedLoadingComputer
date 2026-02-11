"""
计算引擎 - 用于GUI的稳性计算
"""

import numpy as np
from ship_data.crosscurves_data import get_crosscurves_data
from ship_data.hydrostatic_tables_2d import get_draught_from_displacement, get_km_at_draught
from ship_data.hydrostatic_tables_complete import get_lcb_at_draught, get_mct_at_draught


class StabilityCalculator:
    """稳性计算器"""
    
    def __init__(self):
        """初始化计算器"""
        self.crosscurves_data = get_crosscurves_data()
        
    def calculate_floating_position(self, displacement):
        """
        计算浮态参数

        Args:
            displacement: 排水量 (t)

        Returns:
            dict: 浮态参数
        """
        # 检查排水量是否有效
        if displacement <= 0:
            raise ValueError(f"排水量无效: {displacement:.1f} t (必须大于0)")

        # 查询吃水
        draught = get_draught_from_displacement(displacement)

        # 检查吃水是否有效
        if draught < 0:
            raise ValueError(f"计算得到的吃水无效: {draught:.2f} m (排水量: {displacement:.1f} t)")

        # 查询KM
        km = get_km_at_draught(draught)

        # 查询LCB
        lcb = get_lcb_at_draught(draught)

        # 查询MCT
        mct = get_mct_at_draught(draught)

        return {
            'draught': draught,
            'km': km,
            'lcb': lcb,
            'mct': mct,
        }
    
    def calculate_stability_parameters(self, displacement, vcg, fsm):
        """
        计算稳性参数

        Args:
            displacement: 排水量 (t)
            vcg: 重心垂向位置 (m)
            fsm: 自由液面力矩 (t·m)

        Returns:
            dict: 稳性参数
        """
        # 检查排水量是否有效
        if displacement <= 0:
            raise ValueError(f"排水量无效: {displacement:.1f} t (必须大于0)")

        # 获取浮态参数
        floating = self.calculate_floating_position(displacement)
        km = floating['km']

        # 计算GM0
        gm0 = km - vcg

        # 计算dGM（避免除零）
        if displacement > 0:
            dgm = fsm / displacement
        else:
            dgm = 0.0

        # 计算GMf
        gmf = gm0 - dgm

        # 计算KGf
        kgf = vcg + dgm

        return {
            'km': km,
            'vcg': vcg,
            'kg': vcg,
            'gm0': gm0,
            'dgm': dgm,
            'gmf': gmf,
            'kgf': kgf,
        }
    
    def calculate_gz_curve(self, displacement, vcg, fsm, draught, trim=0.0):
        """
        计算GZ曲线
        
        Args:
            displacement: 排水量 (t)
            vcg: 重心垂向位置 (m)
            fsm: 自由液面力矩 (t·m)
            draught: 吃水 (m)
            trim: 纵倾 (m)
            
        Returns:
            dict: GZ曲线数据
        """
        # 计算KGf
        dgm = fsm / displacement
        kgf = vcg + dgm
        
        # 横倾角度
        angles = np.array([0, 10, 20, 30, 40, 50, 60, 70])
        
        # GZ修正值（来自GZ Corrections Table）
        # 这里使用LC01的修正值作为示例
        gz_corrections = {
            0: 0.000,
            10: 0.039,
            20: 0.080,
            30: 0.121,
            40: 0.154,
            50: 0.181,
            60: 0.201,
            70: 0.215,
        }
        
        # 计算每个角度的GZ值
        kn_values = []
        kgf_sin_values = []
        gz_corr_values = []
        gz_values = []
        
        for angle in angles:
            # 查询KN值
            kn = self.get_kn_value(draught, trim, angle)
            kn_values.append(kn)
            
            # 计算KGf * sin(θ)
            kgf_sin = kgf * np.sin(np.radians(angle))
            kgf_sin_values.append(kgf_sin)
            
            # 获取GZ修正值
            gz_corr = gz_corrections.get(angle, 0.0)
            gz_corr_values.append(gz_corr)
            
            # 计算GZ
            gz = kn - kgf_sin - gz_corr
            gz_values.append(gz)
        
        return {
            'angles': angles.tolist(),
            'kn': kn_values,
            'kgf_sin': kgf_sin_values,
            'gz_corr': gz_corr_values,
            'gz': gz_values,
            'kgf': kgf,
        }
    
    def get_kn_value(self, draught, trim, heel_angle):
        """
        从Cross Curves查询KN值

        Args:
            draught: 吃水 (m)
            trim: 纵倾 (m)
            heel_angle: 横倾角 (度)

        Returns:
            float: KN值 (m)
        """
        # 使用CrossCurvesData的get_kn方法（支持双线性插值）
        kn = self.crosscurves_data.get_kn(draught, trim, heel_angle)

        return kn
    
    def check_stability_criteria(self, gz_curve_data, gmf):
        """
        检查稳性衡准
        
        Args:
            gz_curve_data: GZ曲线数据
            gmf: 流体GM (m)
            
        Returns:
            dict: 稳性衡准检查结果
        """
        angles = np.array(gz_curve_data['angles'])
        gz_values = np.array(gz_curve_data['gz'])
        
        # 计算GZ曲线面积
        area_0_30 = self.calculate_area(angles, gz_values, 0, 30)
        area_30_40 = self.calculate_area(angles, gz_values, 30, 40)
        area_15_30 = self.calculate_area(angles, gz_values, 15, 30)
        
        # 最大GZ
        max_gz = np.max(gz_values)
        max_gz_angle = angles[np.argmax(gz_values)]
        
        # IMO稳性衡准
        criteria = {
            'V.AREA15-30': {
                'name': 'Area 15-30°',
                'required': 0.055,  # m·rad
                'actual': area_15_30,
                'unit': 'm·rad',
                'pass': area_15_30 >= 0.055
            },
            'V.AREA3040': {
                'name': 'Area 30-40°',
                'required': 0.030,  # m·rad
                'actual': area_30_40,
                'unit': 'm·rad',
                'pass': area_30_40 >= 0.030
            },
            'V.GZ0.2': {
                'name': 'Max GZ',
                'required': 0.200,  # m
                'actual': max_gz,
                'unit': 'm',
                'pass': max_gz >= 0.200
            },
            'V.POSMAX15': {
                'name': 'Angle of Max GZ',
                'required': 15.0,  # deg
                'actual': max_gz_angle,
                'unit': 'deg',
                'pass': max_gz_angle >= 15.0
            },
            'V.GM0.15': {
                'name': 'GM',
                'required': 0.150,  # m
                'actual': gmf,
                'unit': 'm',
                'pass': gmf >= 0.150
            },
        }
        
        return criteria
    
    def calculate_area(self, angles, gz_values, angle_start, angle_end):
        """
        计算GZ曲线在指定角度范围内的面积
        
        Args:
            angles: 角度数组 (度)
            gz_values: GZ值数组 (m)
            angle_start: 起始角度 (度)
            angle_end: 结束角度 (度)
            
        Returns:
            float: 面积 (m·rad)
        """
        # 转换为弧度
        angles_rad = np.radians(angles)
        
        # 找到范围内的点
        mask = (angles >= angle_start) & (angles <= angle_end)
        angles_range = angles_rad[mask]
        gz_range = gz_values[mask]
        
        if len(angles_range) < 2:
            return 0.0

        # 使用梯形法则计算面积
        # NumPy 2.0+使用trapezoid代替trapz
        try:
            area = np.trapezoid(gz_range, angles_range)
        except AttributeError:
            # 兼容旧版本NumPy
            area = np.trapz(gz_range, angles_range)

        return area

    def calculate_strength(self, loading_data, draught, trim=0.0):
        """
        计算船舶强度

        Args:
            loading_data: 装载数据
            draught: 吃水 (m)
            trim: 纵倾 (m)

        Returns:
            dict: 强度计算结果
        """
        from src.core.strength import StrengthCalculator
        from src.core.loading_condition import WeightItem

        # 创建强度计算器
        strength_calc = StrengthCalculator(condition='TRANSIT')

        # 准备重量项列表
        weight_items = []

        # 添加舱室装载
        items = loading_data.get('items', [])
        for item in items:
            if item.get('weight', 0) > 0:
                weight_item = WeightItem(
                    name=item.get('tank_id', ''),
                    weight=item['weight'],
                    lcg=item['lcg'],
                    vcg=item['vcg'],
                    tcg=item.get('tcg', 0),
                    fsm=item.get('fsm', 0)
                )
                weight_items.append(weight_item)

        # 计算总排水量
        displacement = loading_data.get('displacement', 0)

        # 执行强度计算
        strength_results = strength_calc.calculate_shear_force_and_bending_moment(
            weight_items,
            draught,
            displacement,
            trim=trim
        )

        return strength_results

