"""
吃水测量计算模块 (Draught Survey Calculation)
根据实际吃水读数计算排水量

基于装载手册 3.7 Displacement calculation from the draught readings
"""

import numpy as np
from typing import Dict, Tuple
from ship_data.ship_particulars import SHIP_PARTICULARS


class DraughtSurvey:
    """吃水测量计算类"""

    def __init__(self):
        """初始化吃水测量计算器"""
        self.lpp = SHIP_PARTICULARS['lpp']  # 垂线间长 168.0m
        
        # 吃水标尺位置 (从frame 0开始，单位：米)
        # Frame spacing = 0.8m, Frame 0 at AP
        self.aft_mark_position = 5 * 0.8 + 0.240  # Frame 5 + 0.240m = 4.240m from AP
        self.mid_mark_position = 135 * 0.8  # Frame 135 = 108.0m from AP
        self.fwd_mark_position = 260 * 0.8  # Frame 260 = 208.0m from AP
        
    def calculate_displacement_from_draughts(
        self,
        d_aft_port: float,
        d_aft_stbd: float,
        d_mid_port: float,
        d_mid_stbd: float,
        d_fwd_port: float,
        d_fwd_stbd: float,
        specific_gravity: float = 1.025,
        hydrostatic_calculator=None
    ) -> Dict:
        """
        根据吃水读数计算排水量
        
        Args:
            d_aft_port: 尾部左舷吃水读数 (m)
            d_aft_stbd: 尾部右舷吃水读数 (m)
            d_mid_port: 中部左舷吃水读数 (m)
            d_mid_stbd: 中部右舷吃水读数 (m)
            d_fwd_port: 首部左舷吃水读数 (m)
            d_fwd_stbd: 首部右舷吃水读数 (m)
            specific_gravity: 海水比重 (默认1.025)
            hydrostatic_calculator: 静水力计算器实例
            
        Returns:
            包含计算结果的字典
        """
        # Step 1: 计算平均吃水读数
        d_ao = (d_aft_port + d_aft_stbd) / 2  # 尾部吃水标尺读数
        d_mo = (d_mid_port + d_mid_stbd) / 2  # 中部吃水标尺读数
        d_fo = (d_fwd_port + d_fwd_stbd) / 2  # 首部吃水标尺读数
        
        # Step 2: 计算垂线处的吃水
        # dF = dFo - 8.37 * (dAo - dFo) / 203.76
        d_f = d_fo - 8.37 * (d_ao - d_fo) / 203.76  # 首垂线吃水
        d_a = d_ao  # 尾垂线吃水
        d_m = d_mo - 2.305 * (d_ao - d_fo) / 203.76  # 中部吃水
        
        # Step 3: 计算纵倾、平均吃水和挠度
        trim = d_a - d_f  # 纵倾 (m)
        d_ma = (d_a + d_f) / 2  # 平均吃水 (m)
        deflection = d_m - d_ma  # 挠度 (m)
        
        # 判断纵倾和挠度状态
        trim_status = "trim by stern" if trim > 0 else "trim by bow" if trim < 0 else "even keel"
        deflection_status = "sagging" if deflection > 0 else "hogging" if deflection < 0 else "no deflection"
        
        # Step 4: 从静水力表读取数据
        if hydrostatic_calculator is None:
            from src.core.flotation import FlotationCalculator
            hydrostatic_calculator = FlotationCalculator()
        
        # 根据平均吃水获取静水力参数
        hydro_params = hydrostatic_calculator.get_hydrostatic_properties(d_m)
        
        displacement_1 = hydro_params['displacement']  # D1
        tpc = hydro_params['tpc']  # TPC
        mct = hydro_params['mct']  # MCT
        lca = hydro_params['lcf']  # LCA (从AP起算)
        
        # Step 5: 排水量修正
        # a. 纵倾修正
        # D2 = (LCA - 106.065) * t * TPC * 100 / Lpp
        displacement_2 = (lca - 106.065) * trim * tpc * 100 / self.lpp

        # b. 挠度修正
        # D3 = (TPC / (dA + dF)/2 / MCT) * Gd * 100
        # 修正公式：D3 = (TPC / draught / MCT) * Gd * 100
        if mct > 0 and d_ma > 0:
            displacement_3 = (tpc / d_ma / mct) * deflection * 100
        else:
            displacement_3 = 0.0
        
        # Step 6: 比重修正
        # D4 = (D1 + D2 + D3) * (S.G. - 1.025) / 1.025
        displacement_4 = (displacement_1 + displacement_2 + displacement_3) * \
                        (specific_gravity - 1.025) / 1.025
        
        # Step 7: 最终排水量
        final_displacement = displacement_1 + displacement_2 + displacement_3 + displacement_4
        
        # 计算横倾
        heel_aft = d_aft_stbd - d_aft_port
        heel_mid = d_mid_stbd - d_mid_port
        heel_fwd = d_fwd_stbd - d_fwd_port
        heel_avg = (heel_aft + heel_mid + heel_fwd) / 3
        
        return {
            # 原始读数
            'draught_readings': {
                'aft_port': d_aft_port,
                'aft_stbd': d_aft_stbd,
                'aft_avg': d_ao,
                'mid_port': d_mid_port,
                'mid_stbd': d_mid_stbd,
                'mid_avg': d_mo,
                'fwd_port': d_fwd_port,
                'fwd_stbd': d_fwd_stbd,
                'fwd_avg': d_fo,
            },
            # 垂线处吃水
            'perpendicular_draughts': {
                'aft': d_a,
                'mid': d_m,
                'fwd': d_f,
                'mean': d_ma,
            },
            # 纵倾和挠度
            'trim': trim,
            'trim_status': trim_status,
            'deflection': deflection,
            'deflection_status': deflection_status,
            'heel': heel_avg,
            # 静水力参数
            'hydrostatic_params': {
                'tpc': tpc,
                'mct': mct,
                'lca': lca,
            },
            # 排水量计算
            'displacement_calculation': {
                'D1_from_hydrostatic': displacement_1,
                'D2_trim_correction': displacement_2,
                'D3_deflection_correction': displacement_3,
                'D4_density_correction': displacement_4,
                'final_displacement': final_displacement,
            },
            'specific_gravity': specific_gravity,
        }

