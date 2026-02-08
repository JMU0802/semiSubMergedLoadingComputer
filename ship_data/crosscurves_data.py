"""
Cross Curves数据解析和查询模块
用于从Crosscurves.txt读取KN值，支持吃水和trim的双线性插值
"""

import numpy as np
from scipy import interpolate
import os


class CrossCurvesData:
    """Cross Curves数据类"""
    
    def __init__(self, filepath=None):
        """
        初始化Cross Curves数据
        
        Args:
            filepath: Crosscurves.txt文件路径，默认为ship_data/Crosscurves.txt
        """
        if filepath is None:
            current_dir = os.path.dirname(__file__)
            filepath = os.path.join(current_dir, 'Crosscurves.txt')
        
        self.filepath = filepath
        self.data = {}  # {trim: {draught: {angle: kn_value}}}
        self.trim_values = []
        self.draught_values = []
        self.heel_angles = []
        
        self._load_data()
    
    def _load_data(self):
        """从文件加载数据"""
        with open(self.filepath, 'r') as f:
            lines = f.readlines()
        
        current_trim = None
        reading_data = False
        
        for line in lines:
            line = line.strip()
            
            # 检测trim标题行
            if 'INITIAL TRIM:' in line:
                # 提取trim值
                parts = line.split('INITIAL TRIM:')[1].split('M')[0].strip()
                current_trim = float(parts)
                if current_trim not in self.trim_values:
                    self.trim_values.append(current_trim)
                self.data[current_trim] = {}
                reading_data = False
                continue
            
            # 检测表头行（包含HEELING ANGLE）
            if 'HEELING ANGLE' in line:
                reading_data = True
                continue
            
            # 检测角度行（包含DRAUGHT）
            if 'DRAUGHT' in line and reading_data:
                # 下一行开始是数据
                continue
            
            # 读取数据行
            if reading_data and current_trim is not None and line:
                # 跳过分隔线
                if '=' in line or line.startswith('KN AS'):
                    reading_data = False
                    continue
                
                # 解析数据行
                parts = line.split()
                if len(parts) >= 10:  # draught + 9个角度的KN值
                    try:
                        draught = float(parts[0])
                        kn_values = [float(parts[i]) for i in range(1, 10)]
                        
                        # 存储数据
                        if draught not in self.data[current_trim]:
                            self.data[current_trim][draught] = {}
                            if draught not in self.draught_values:
                                self.draught_values.append(draught)
                        
                        # 角度：0, 5, 10, 15, 20, 30, 40, 50, 60
                        angles = [0.0, 5.0, 10.0, 15.0, 20.0, 30.0, 40.0, 50.0, 60.0]
                        if not self.heel_angles:
                            self.heel_angles = angles
                        
                        for angle, kn in zip(angles, kn_values):
                            self.data[current_trim][draught][angle] = kn
                    except (ValueError, IndexError):
                        continue
        
        # 排序
        self.trim_values.sort()
        self.draught_values.sort()
        
        print(f"✓ 已加载Cross Curves数据:")
        print(f"  - Trim范围: {min(self.trim_values):.2f} ~ {max(self.trim_values):.2f} m ({len(self.trim_values)}个点)")
        print(f"  - 吃水范围: {min(self.draught_values):.2f} ~ {max(self.draught_values):.2f} m ({len(self.draught_values)}个点)")
        print(f"  - 横倾角: {self.heel_angles}")
    
    def get_kn(self, draught, trim, heel_angle):
        """
        获取指定吃水、trim和横倾角的KN值（使用双线性插值）
        
        Args:
            draught: 吃水 (m)
            trim: 纵倾 (m)
            heel_angle: 横倾角 (degrees)
        
        Returns:
            float: KN值 (m)
        """
        # 限制trim范围
        trim = np.clip(trim, min(self.trim_values), max(self.trim_values))
        
        # 找到trim的两个邻近值
        trim_idx = np.searchsorted(self.trim_values, trim)
        if trim_idx == 0:
            trim_lower = trim_upper = self.trim_values[0]
            trim_ratio = 0.0
        elif trim_idx >= len(self.trim_values):
            trim_lower = trim_upper = self.trim_values[-1]
            trim_ratio = 0.0
        else:
            trim_lower = self.trim_values[trim_idx - 1]
            trim_upper = self.trim_values[trim_idx]
            if trim_upper != trim_lower:
                trim_ratio = (trim - trim_lower) / (trim_upper - trim_lower)
            else:
                trim_ratio = 0.0
        
        # 对两个trim值分别插值
        kn_lower = self._get_kn_at_trim(draught, trim_lower, heel_angle)
        kn_upper = self._get_kn_at_trim(draught, trim_upper, heel_angle)
        
        # trim方向线性插值
        kn = kn_lower + (kn_upper - kn_lower) * trim_ratio
        
        return kn
    
    def _get_kn_at_trim(self, draught, trim, heel_angle):
        """
        获取指定trim下，给定吃水和横倾角的KN值（吃水和角度方向插值）
        
        Args:
            draught: 吃水 (m)
            trim: 纵倾 (m，必须是self.trim_values中的值)
            heel_angle: 横倾角 (degrees)
        
        Returns:
            float: KN值 (m)
        """
        if trim not in self.data:
            raise ValueError(f"Trim {trim} not found in data")
        
        trim_data = self.data[trim]
        draughts = sorted(trim_data.keys())
        
        # 限制吃水范围
        draught = np.clip(draught, min(draughts), max(draughts))
        
        # 对每个横倾角，在吃水方向插值
        kn_at_draughts = []
        for d in draughts:
            if heel_angle in trim_data[d]:
                kn_at_draughts.append(trim_data[d][heel_angle])
            else:
                # 横倾角方向插值
                angles = sorted(trim_data[d].keys())
                kn_values = [trim_data[d][a] for a in angles]
                kn_interp = np.interp(heel_angle, angles, kn_values)
                kn_at_draughts.append(kn_interp)
        
        # 吃水方向插值
        kn = np.interp(draught, draughts, kn_at_draughts)
        
        return float(kn)


# 全局实例
_crosscurves_instance = None


def get_crosscurves_data():
    """获取Cross Curves数据实例（单例模式）"""
    global _crosscurves_instance
    if _crosscurves_instance is None:
        _crosscurves_instance = CrossCurvesData()
    return _crosscurves_instance

