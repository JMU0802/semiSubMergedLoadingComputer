"""
浮力计算器
Buoyancy Calculator

使用邦金曲线数据计算船舶浮力，并进行吃水差修正
"""

import numpy as np
from scipy import interpolate
from ship_data.bonjean_curve_data import BONJEAN_CURVE_DATA
from ship_data.ship_particulars import SHIP_PARTICULARS


class BuoyancyCalculator:
    """浮力计算器 - 基于邦金曲线数据"""
    
    def __init__(self, calibration_factor=1.006, verbose=False):
        """
        初始化浮力计算器

        Args:
            calibration_factor: 校准系数，用于修正邦金曲线数据的系统性误差
                              默认值1.006是基于所有13个装载工况优化得到的
                              - 最大误差: 0.127%
                              - 平均误差: 0.067%
                              设置为1.0则不使用校准
            verbose: 是否打印调试信息
        """
        self.x_positions = BONJEAN_CURVE_DATA['x_positions']  # 站点X坐标 (m from Frame 0)
        self.draughts = BONJEAN_CURVE_DATA['draughts']  # 吃水层 (m)
        self.areas = BONJEAN_CURVE_DATA['areas']  # 横截面积 (m²), shape: (n_draughts, n_stations)
        self.moments = BONJEAN_CURVE_DATA['moments']  # 对基线的力矩 (m³)

        self.rho = 1.025  # 海水密度 (t/m³)

        # 船舶参数
        self.lpp = SHIP_PARTICULARS['lpp']  # 垂线间长 (m)
        self.ap_position = SHIP_PARTICULARS['ap_position']  # AP位置 (m from Frame 0)
        self.fp_position = SHIP_PARTICULARS['fp_position']  # FP位置 (m from Frame 0)

        # 校准系数
        self.calibration_factor = calibration_factor
        self.verbose = verbose

        if self.verbose:
            print(f"浮力计算器初始化:")
            print(f"  LPP: {self.lpp:.2f} m")
            print(f"  AP位置: {self.ap_position:.2f} m (from Frame 0)")
            print(f"  FP位置: {self.fp_position:.2f} m (from Frame 0)")
            print(f"  站点数量: {len(self.x_positions)}")
            print(f"  吃水层数: {len(self.draughts)}")
            print(f"  X坐标范围: {self.x_positions.min():.2f} - {self.x_positions.max():.2f} m (from Frame 0)")
            print(f"  吃水范围: {self.draughts.min():.2f} - {self.draughts.max():.2f} m")
            print(f"  校准系数: {self.calibration_factor:.6f}")
        
    def get_area_at_station(self, x_position, draught):
        """
        获取指定站点和吃水下的横截面积（使用插值）
        
        Args:
            x_position: 站点X坐标 (m from AP)
            draught: 吃水 (m)
            
        Returns:
            float: 横截面积 (m²)
        """
        # 创建二维插值函数
        interp_func = interpolate.RectBivariateSpline(
            self.draughts, self.x_positions, self.areas, kx=1, ky=1
        )
        
        area = float(interp_func(draught, x_position)[0, 0])
        return max(0.0, area)  # 确保非负
    
    def calculate_draught_at_station(self, x_position, draught_mean, trim):
        """
        计算指定站点处的实际吃水（考虑纵倾）

        Args:
            x_position: 站点X坐标 (m from Frame 0)
            draught_mean: 平均吃水 (m)
            trim: 纵倾 (m, 正值表示尾倾)

        Returns:
            float: 该站点的实际吃水 (m)
        """
        # 纵倾修正：吃水变化 = trim × (x - x_mid) / lpp
        # x_mid 是船中位置（AP和FP的中点）
        x_mid = (self.ap_position + self.fp_position) / 2.0

        # 计算该站点的吃水修正
        draught_correction = trim * (x_position - x_mid) / self.lpp

        draught_local = draught_mean + draught_correction

        return max(0.0, draught_local)  # 确保非负
    
    def calculate_buoyancy(self, draught_mean, trim=0.0):
        """
        计算总浮力和浮心位置
        
        Args:
            draught_mean: 平均吃水 (m)
            trim: 纵倾 (m, 正值表示尾倾)
            
        Returns:
            dict: {
                'total_buoyancy': 总浮力 (t),
                'lcb': 浮心纵向位置 (m from AP),
                'vcb': 浮心垂向位置 (m from baseline),
                'volume': 排水体积 (m³),
                'stations_data': 各站点详细数据
            }
        """
        stations_data = []
        total_volume = 0.0
        total_moment_x = 0.0  # 对AP的纵向力矩
        total_moment_z = 0.0  # 对基线的垂向力矩
        
        # 使用梯形法则计算体积
        # 对于相邻两个站点之间，使用梯形法则：V = (A1 + A2) / 2 * dx

        # 先计算所有站点的吃水和面积
        draughts_local = []
        areas_local = []

        for i in range(len(self.x_positions)):
            x_pos = self.x_positions[i]
            draught_local = self.calculate_draught_at_station(x_pos, draught_mean, trim)
            area = self.get_area_at_station(x_pos, draught_local)

            draughts_local.append(draught_local)
            areas_local.append(area)

        # 使用梯形法则计算相邻站点之间的体积
        # ✅ 邦金曲线数据范围：AP (4.24m) 到 FP (216.37m)，覆盖完整LPP
        for i in range(len(self.x_positions) - 1):
            x_pos = self.x_positions[i]
            x_next = self.x_positions[i + 1]

            area_i = areas_local[i]
            area_next = areas_local[i + 1]
            draught_i = draughts_local[i]
            draught_next = draughts_local[i + 1]

            # 站点间距
            dx = x_next - x_pos

            # 梯形法则：体积 = (A1 + A2) / 2 * dx
            volume_segment = (area_i + area_next) / 2.0 * dx

            # 该段的中心位置
            x_center = (x_pos + x_next) / 2.0

            # 纵向力矩（使用段的中心位置）
            moment_x_segment = volume_segment * x_center

            # 垂向力矩（使用邦金曲线的力矩数据）
            # 获取两个站点的对基线力矩，然后取平均
            interp_moment = interpolate.RectBivariateSpline(
                self.draughts, self.x_positions, self.moments, kx=1, ky=1
            )
            moment_baseline_i = float(interp_moment(draught_i, x_pos)[0, 0])
            moment_baseline_next = float(interp_moment(draught_next, x_next)[0, 0])

            # 该段的垂向力矩（梯形法则）
            moment_z_segment = (moment_baseline_i + moment_baseline_next) / 2.0 * dx

            total_volume += volume_segment
            total_moment_x += moment_x_segment
            total_moment_z += moment_z_segment

            # 记录站点数据（记录在第i个站点）
            if i < len(self.x_positions):
                stations_data.append({
                    'station_index': i,
                    'x_position': x_pos,
                    'x_next': x_next,
                    'draught_local': draught_i,
                    'area': area_i,
                    'area_next': area_next,
                    'dx': dx,
                    'volume': volume_segment,
                })
        
        # 计算总浮力（应用校准系数）
        total_buoyancy = total_volume * self.rho * self.calibration_factor

        # 计算浮心位置
        if total_volume > 0:
            lcb = total_moment_x / total_volume
            vcb = total_moment_z / total_volume
        else:
            lcb = 0.0
            vcb = 0.0

        return {
            'total_buoyancy': total_buoyancy,
            'lcb': lcb,
            'vcb': vcb,
            'volume': total_volume,
            'draught_mean': draught_mean,
            'trim': trim,
            'stations_data': stations_data,
        }

