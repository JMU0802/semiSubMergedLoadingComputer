"""
浮态计算模块 (Flotation Calculation)
计算船舶的吃水、纵倾、排水量等浮态参数
"""

import numpy as np
from scipy import interpolate
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from ship_data.hydrostatic_data import get_hydrostatic_data
from ship_data.ship_particulars import SHIP_PARTICULARS, DENSITIES


class FlotationCalculator:
    """浮态计算器"""
    
    def __init__(self, condition='TRANSIT'):
        """
        初始化浮态计算器
        
        Args:
            condition: 工况类型 ('TRANSIT' 或 'SEMI_SUBMERGED')
        """
        self.condition = condition
        self.hydro_data = get_hydrostatic_data(condition)
        self._create_interpolators()
    
    def _create_interpolators(self):
        """创建插值函数"""
        draughts = self.hydro_data['draught']
        displacements = self.hydro_data['displacement']

        # 创建各参数的插值函数（吃水 -> 参数）
        self.interp_displacement = interpolate.interp1d(
            draughts, displacements,
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_lcb = interpolate.interp1d(
            draughts, self.hydro_data['lcb'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_vcb = interpolate.interp1d(
            draughts, self.hydro_data['vcb'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_lcf = interpolate.interp1d(
            draughts, self.hydro_data['lcf'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_tpc = interpolate.interp1d(
            draughts, self.hydro_data['tpc'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_mct = interpolate.interp1d(
            draughts, self.hydro_data['mct'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_gmt = interpolate.interp1d(
            draughts, self.hydro_data['gmt'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_bmt = interpolate.interp1d(
            draughts, self.hydro_data['bmt'],
            kind='cubic', fill_value='extrapolate'
        )
        
        # 创建反向插值（排水量->吃水）
        self.interp_draught = interpolate.interp1d(
            displacements, draughts,
            kind='cubic', fill_value='extrapolate'
        )

        # 创建排水量->其他参数的插值函数
        self.interp_lcb_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['lcb'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_vcb_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['vcb'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_lcf_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['lcf'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_tpc_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['tpc'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_mct_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['mct'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_gmt_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['gmt'],
            kind='cubic', fill_value='extrapolate'
        )
        self.interp_bmt_from_disp = interpolate.interp1d(
            displacements, self.hydro_data['bmt'],
            kind='cubic', fill_value='extrapolate'
        )
    
    def get_displacement(self, draught):
        """
        根据吃水计算排水量
        
        Args:
            draught: 吃水 (m)
        
        Returns:
            float: 排水量 (t)
        """
        return float(self.interp_displacement(draught))
    
    def get_draught(self, displacement):
        """
        根据排水量计算吃水
        
        Args:
            displacement: 排水量 (t)
        
        Returns:
            float: 吃水 (m)
        """
        return float(self.interp_draught(displacement))
    
    def get_hydrostatic_properties(self, draught):
        """
        获取指定吃水的所有静水力参数

        Args:
            draught: 吃水 (m)

        Returns:
            dict: 静水力参数字典
        """
        return {
            'draught': draught,
            'displacement': float(self.interp_displacement(draught)),
            'lcb': float(self.interp_lcb(draught)),
            'vcb': float(self.interp_vcb(draught)),
            'lcf': float(self.interp_lcf(draught)),
            'tpc': float(self.interp_tpc(draught)),
            'mct': float(self.interp_mct(draught)),
            'gmt': float(self.interp_gmt(draught)),
            'bmt': float(self.interp_bmt(draught)),
            'kmt': float(self.interp_vcb(draught)) + float(self.interp_bmt(draught)),  # KM = KB + BM
        }

    def get_hydrostatic_properties_by_displacement(self, displacement):
        """
        根据排水量获取所有静水力参数

        Args:
            displacement: 排水量 (t)

        Returns:
            dict: 静水力参数字典
        """
        draught = float(self.interp_draught(displacement))
        return {
            'draught': draught,
            'displacement': displacement,
            'lcb': float(self.interp_lcb_from_disp(displacement)),
            'vcb': float(self.interp_vcb_from_disp(displacement)),
            'lcf': float(self.interp_lcf_from_disp(displacement)),
            'tpc': float(self.interp_tpc_from_disp(displacement)),
            'mct': float(self.interp_mct_from_disp(displacement)),
            'gmt': float(self.interp_gmt_from_disp(displacement)),
            'bmt': float(self.interp_bmt_from_disp(displacement)),
            'kmt': float(self.interp_vcb_from_disp(displacement)) + float(self.interp_bmt_from_disp(displacement)),
        }
    
    def calculate_trim(self, total_weight, lcg_total):
        """
        计算纵倾
        
        Args:
            total_weight: 总重量 (t)
            lcg_total: 总重心纵向位置 (m from AP)
        
        Returns:
            dict: 包含平均吃水、首吃水、尾吃水、纵倾的字典
        """
        # 根据总重量计算平均吃水
        draught_mean = self.get_draught(total_weight)
        
        # 获取静水力参数
        hydro = self.get_hydrostatic_properties(draught_mean)
        lcb = hydro['lcb']
        lcf = hydro['lcf']
        mct = hydro['mct']
        
        # 计算纵倾力矩
        trim_moment = total_weight * (lcg_total - lcb)

        # 计算纵倾 (cm)
        # MCT单位是改变1cm纵倾所需力矩 (t·m)
        trim_cm = trim_moment / mct if mct > 0 else 0

        # 转换为米
        trim = trim_cm / 100.0

        # 计算首尾吃水
        # 纵倾正值表示尾倾（艉吃水大于首吃水）
        lpp = SHIP_PARTICULARS['lpp']
        ap = SHIP_PARTICULARS['ap_position']
        fp = SHIP_PARTICULARS['fp_position']

        # 使用漂心位置计算首尾吃水
        # 吃水变化 = 纵倾 × 距离漂心的距离 / 船长
        draught_aft = draught_mean + trim * (lcf - ap) / lpp
        draught_fwd = draught_mean - trim * (fp - lcf) / lpp
        
        return {
            'draught_mean': draught_mean,
            'draught_aft': draught_aft,
            'draught_fwd': draught_fwd,
            'trim': trim,
            'trim_angle': np.degrees(np.arctan(trim / lpp)),  # 纵倾角(度)
        }

