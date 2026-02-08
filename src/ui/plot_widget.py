"""
绘图部件 (Plot Widget)
使用Matplotlib绘制GZ曲线、剪力弯矩曲线等
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class PlotWidget(QWidget):
    """绘图部件"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 创建Figure和Canvas
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        # 创建工具栏
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # 创建坐标轴
        self.ax = self.figure.add_subplot(111)
    
    def clear(self):
        """清空图表"""
        self.ax.clear()
        self.canvas.draw()
    
    def plot_gz_curve(self, heel_angles, gz_values):
        """
        绘制GZ曲线
        
        Args:
            heel_angles: 横倾角数组 (degrees)
            gz_values: GZ值数组 (m)
        """
        self.ax.clear()
        
        # 绘制GZ曲线
        self.ax.plot(heel_angles, gz_values, 'b-', linewidth=2, label='GZ曲线')
        self.ax.plot(heel_angles, gz_values, 'bo', markersize=6)
        
        # 绘制零线
        self.ax.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
        
        # 标注最大GZ点
        max_idx = np.argmax(gz_values)
        max_gz = gz_values[max_idx]
        max_angle = heel_angles[max_idx]
        self.ax.plot(max_angle, max_gz, 'ro', markersize=10, label=f'最大GZ: {max_gz:.3f}m @ {max_angle}°')
        self.ax.annotate(f'Max: {max_gz:.3f}m\n@ {max_angle}°',
                        xy=(max_angle, max_gz),
                        xytext=(max_angle + 5, max_gz + 0.1),
                        arrowprops=dict(arrowstyle='->', color='red'),
                        fontsize=10)
        
        # 设置标签和标题
        self.ax.set_xlabel('横倾角 (度)', fontsize=12)
        self.ax.set_ylabel('复原力臂 GZ (m)', fontsize=12)
        self.ax.set_title('静稳性曲线 (GZ Curve)', fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='best')
        
        # 设置坐标轴范围
        self.ax.set_xlim(0, max(heel_angles) + 5)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_shear_force(self, stations, shear_force, max_allowable):
        """
        绘制剪力曲线
        
        Args:
            stations: 站位数组 (m)
            shear_force: 剪力数组 (kN)
            max_allowable: 许用剪力 (kN)
        """
        self.ax.clear()
        
        # 绘制剪力曲线
        self.ax.plot(stations, shear_force, 'b-', linewidth=2, label='剪力')
        self.ax.fill_between(stations, 0, shear_force, alpha=0.3)
        
        # 绘制许用值线
        if max_allowable > 0:
            self.ax.axhline(y=max_allowable, color='r', linestyle='--', 
                          linewidth=1.5, label=f'许用剪力: ±{max_allowable:.0f} kN')
            self.ax.axhline(y=-max_allowable, color='r', linestyle='--', linewidth=1.5)
        
        # 绘制零线
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        
        # 标注最大值
        max_sf = np.max(np.abs(shear_force))
        max_idx = np.argmax(np.abs(shear_force))
        max_station = stations[max_idx]
        max_value = shear_force[max_idx]
        self.ax.plot(max_station, max_value, 'ro', markersize=8)
        
        # 设置标签和标题
        self.ax.set_xlabel('船长位置 (m from AP)', fontsize=12)
        self.ax.set_ylabel('剪力 (kN)', fontsize=12)
        self.ax.set_title('剪力曲线 (Shear Force)', fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='best')
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def plot_bending_moment(self, stations, bending_moment, max_sagging, max_hogging):
        """
        绘制弯矩曲线
        
        Args:
            stations: 站位数组 (m)
            bending_moment: 弯矩数组 (kN·m)
            max_sagging: 许用中拱弯矩 (kN·m)
            max_hogging: 许用中垂弯矩 (kN·m)
        """
        self.ax.clear()
        
        # 绘制弯矩曲线
        self.ax.plot(stations, bending_moment / 1000, 'b-', linewidth=2, label='弯矩')
        self.ax.fill_between(stations, 0, bending_moment / 1000, alpha=0.3)
        
        # 绘制许用值线
        if max_sagging > 0:
            self.ax.axhline(y=max_sagging / 1000, color='r', linestyle='--',
                          linewidth=1.5, label=f'许用中拱: {max_sagging/1000:.0f} MN·m')
        if max_hogging > 0:
            self.ax.axhline(y=-max_hogging / 1000, color='r', linestyle='--',
                          linewidth=1.5, label=f'许用中垂: {max_hogging/1000:.0f} MN·m')
        
        # 绘制零线
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        
        # 标注最大值
        max_bm = np.max(np.abs(bending_moment))
        max_idx = np.argmax(np.abs(bending_moment))
        max_station = stations[max_idx]
        max_value = bending_moment[max_idx] / 1000
        self.ax.plot(max_station, max_value, 'ro', markersize=8)
        
        # 设置标签和标题
        self.ax.set_xlabel('船长位置 (m from AP)', fontsize=12)
        self.ax.set_ylabel('弯矩 (MN·m)', fontsize=12)
        self.ax.set_title('弯矩曲线 (Bending Moment)', fontsize=14, fontweight='bold')
        self.ax.grid(True, alpha=0.3)
        self.ax.legend(loc='best')
        
        self.figure.tight_layout()
        self.canvas.draw()

