"""
船舶数据查看器
Ship Data Viewer Widget

显示邦金曲线、肋骨位置和空船重量分布
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
                             QLabel, QComboBox, QGroupBox, QPushButton, QCheckBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# 配置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

from ship_data.bonjean_curve_data import BONJEAN_CURVE_DATA
from ship_data.frame_data import LIGHTSHIP_WEIGHT_DATA, FRAME_POSITION_DATA


class ShipDataViewer(QWidget):
    """船舶数据查看器"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题
        title = QLabel("船舶数据查看器 (Ship Data Viewer)")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 创建标签页
        self.tabs = QTabWidget()
        
        # 邦金曲线标签页
        self.bonjean_tab = self.create_bonjean_tab()
        self.tabs.addTab(self.bonjean_tab, "邦金曲线 (Bonjean Curve)")
        
        # 空船重量分布标签页
        self.lightship_tab = self.create_lightship_tab()
        self.tabs.addTab(self.lightship_tab, "空船重量分布 (Lightship Weight)")
        
        # 综合视图标签页
        self.combined_tab = self.create_combined_tab()
        self.tabs.addTab(self.combined_tab, "综合视图 (Combined View)")
        
        layout.addWidget(self.tabs)
        
    def create_bonjean_tab(self):
        """创建邦金曲线标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 控制面板
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)

        # 说明标签
        info_label = QLabel("邦金曲线 Bonjean Curves - 横截面积分布")
        info_label.setFont(QFont("Arial", 11, QFont.Bold))
        control_layout.addWidget(info_label)

        control_layout.addStretch()

        # 吃水选择
        draught_label = QLabel("选择吃水 (Draught):")
        control_layout.addWidget(draught_label)

        self.draught_combo = QComboBox()

        # 添加默认选项（显示典型吃水）
        self.draught_combo.addItem("显示典型吃水 (8, 12, 16, 20, 24, 28 m)", None)
        self.draught_combo.addItem("---")

        # 添加典型吃水选项
        typical_draughts = [8, 12, 16, 20, 24, 28]
        for td in typical_draughts:
            self.draught_combo.addItem(f"吃水 {td} m", td)

        self.draught_combo.addItem("---")

        # 添加所有吃水
        draughts = BONJEAN_CURVE_DATA['draughts']
        for d in draughts:
            self.draught_combo.addItem(f"吃水 {d:.2f} m", d)

        self.draught_combo.currentIndexChanged.connect(self.update_bonjean_plot)
        control_layout.addWidget(self.draught_combo)

        # 显示所有站点复选框
        self.show_all_stations_check = QCheckBox("显示所有21个站点")
        self.show_all_stations_check.setChecked(True)
        self.show_all_stations_check.stateChanged.connect(self.update_bonjean_plot)
        control_layout.addWidget(self.show_all_stations_check)

        layout.addWidget(control_panel)

        # 绘图区域
        self.bonjean_figure = Figure(figsize=(16, 10))
        self.bonjean_canvas = FigureCanvas(self.bonjean_figure)
        layout.addWidget(self.bonjean_canvas)

        # 初始绘图
        self.update_bonjean_plot()

        return widget
        
    def create_lightship_tab(self):
        """创建空船重量分布标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 统计信息
        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout()

        from ship_data.frame_data import calculate_total_lightship_weight

        lw_data = LIGHTSHIP_WEIGHT_DATA
        total_weight = calculate_total_lightship_weight()
        avg_weight = lw_data['weights'].mean()
        max_weight = lw_data['weights'].max()
        min_weight = lw_data['weights'].min()

        error = abs(total_weight - 20871.4)
        error_pct = error / 20871.4 * 100

        stats_layout.addWidget(QLabel(f"<b>Total Lightship Weight: {total_weight:.2f} t</b>"))
        stats_layout.addWidget(QLabel(f"Manual Reference: 20871.4 t"))

        if error < 0.1:
            stats_layout.addWidget(QLabel(f"<font color='green'>[OK] Exact Match!</font>"))
        else:
            stats_layout.addWidget(QLabel(f"Error: {error:.2f} t ({error_pct:.2f}%)"))

        stats_layout.addWidget(QLabel(""))  # 空行
        stats_layout.addWidget(QLabel(f"Average Density: {avg_weight:.2f} t/m"))
        stats_layout.addWidget(QLabel(f"Maximum Density: {max_weight:.2f} t/m"))
        stats_layout.addWidget(QLabel(f"Minimum Density: {min_weight:.2f} t/m"))

        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)

        # 绘图区域
        self.lightship_figure = Figure(figsize=(14, 7))
        self.lightship_canvas = FigureCanvas(self.lightship_figure)
        layout.addWidget(self.lightship_canvas)

        # 初始绘图
        self.update_lightship_plot()

        return widget
        
    def create_combined_tab(self):
        """创建综合视图标签页"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 绘图区域
        self.combined_figure = Figure(figsize=(14, 12))
        self.combined_canvas = FigureCanvas(self.combined_figure)
        layout.addWidget(self.combined_canvas)

        # 初始绘图
        self.update_combined_plot()

        return widget

    def update_bonjean_plot(self):
        """更新邦金曲线图 - 根据选择显示典型吃水或特定吃水"""
        self.bonjean_figure.clear()

        x_positions = BONJEAN_CURVE_DATA['x_positions']
        draughts = BONJEAN_CURVE_DATA['draughts']

        # 获取选择的吃水
        selected_draught = self.draught_combo.currentData()

        # 创建两个子图
        ax1 = self.bonjean_figure.add_subplot(2, 1, 1)
        ax2 = self.bonjean_figure.add_subplot(2, 1, 2)

        # 使用颜色映射
        import matplotlib.cm as cm

        # 确定要绘制的吃水
        if selected_draught is None:
            # 显示典型吃水（默认）
            typical_draughts = [8.0, 12.0, 16.0, 20.0, 24.0, 28.0]
            draught_indices = []
            for td in typical_draughts:
                idx = np.argmin(np.abs(draughts - td))
                draught_indices.append(idx)
            colors = cm.tab10(np.linspace(0, 1, len(draught_indices)))
            title_suffix = "Typical Draughts (8, 12, 16, 20, 24, 28 m)"
        else:
            # 显示选定的单个吃水
            idx = np.argmin(np.abs(draughts - selected_draught))
            draught_indices = [idx]
            colors = ['red']
            title_suffix = f"Draught = {draughts[idx]:.2f} m"

        # 绘制面积曲线
        for i, idx in enumerate(draught_indices):
            draught = draughts[idx]
            areas = BONJEAN_CURVE_DATA['areas'][idx, :]
            ax1.plot(x_positions, areas, color=colors[i], linewidth=2.0,
                    label=f'T={draught:.1f}m', alpha=0.9, marker='o', markersize=4)

        ax1.set_xlabel('X-COORD (Distance from AP, m)', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Sectional Area (m^2)', fontsize=12, fontweight='bold')
        ax1.set_title(f'Bonjean Curve - Sectional Area\n{title_suffix}',
                     fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
        ax1.grid(True, which='minor', alpha=0.2, linestyle=':', linewidth=0.5)
        ax1.minorticks_on()
        ax1.legend(loc='upper right', fontsize=10, framealpha=0.9)

        # 绘制力矩曲线
        for i, idx in enumerate(draught_indices):
            draught = draughts[idx]
            moments = BONJEAN_CURVE_DATA['moments'][idx, :]
            ax2.plot(x_positions, moments, color=colors[i], linewidth=2.0,
                    label=f'T={draught:.1f}m', alpha=0.9, marker='s', markersize=4)

        ax2.set_xlabel('X-COORD (Distance from AP, m)', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Moment about Baseline (m^3)', fontsize=12, fontweight='bold')
        ax2.set_title(f'Bonjean Curve - Moment about Baseline\n{title_suffix}',
                     fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.4, linestyle='--', linewidth=0.8)
        ax2.grid(True, which='minor', alpha=0.2, linestyle=':', linewidth=0.5)
        ax2.minorticks_on()
        ax2.legend(loc='upper right', fontsize=10, framealpha=0.9)

        # 添加站点信息
        info_text = f'Stations: {len(x_positions)} (X: {x_positions.min():.2f} - {x_positions.max():.2f} m)'
        ax1.text(0.02, 0.98, info_text, transform=ax1.transAxes,
                fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))

        self.bonjean_figure.tight_layout(pad=2.0)
        self.bonjean_canvas.draw()

    def update_lightship_plot(self):
        """更新空船重量分布图"""
        self.lightship_figure.clear()

        from ship_data.frame_data import calculate_total_lightship_weight

        lw_data = LIGHTSHIP_WEIGHT_DATA
        fp_data = FRAME_POSITION_DATA

        # 创建子图
        ax = self.lightship_figure.add_subplot(1, 1, 1)

        # 绘制重量密度分布 - 使用填充区域
        ax.fill_between(fp_data['positions'], 0, lw_data['weights'],
                       color='red', alpha=0.6, edgecolor='darkred', linewidth=0.8)
        ax.plot(fp_data['positions'], lw_data['weights'], 'r-', linewidth=1.8)

        ax.set_xlabel('FRAME (Distance from AP, m)', fontsize=12)
        ax.set_ylabel('Weight Distribution (t/m)', fontsize=12)
        ax.set_title('Lightship Weight Distribution', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_xlim([fp_data['positions'].min(), fp_data['positions'].max()])
        ax.set_ylim([0, lw_data['weights'].max() * 1.1])

        # 添加统计信息
        total_weight = calculate_total_lightship_weight()
        avg_weight = lw_data['weights'].mean()
        max_weight = lw_data['weights'].max()
        error = abs(total_weight - 20871.4)
        error_pct = error / 20871.4 * 100

        info_text = f'Total Lightship Weight: {total_weight:.2f} t\n'
        info_text += f'Manual Reference: 20871.4 t\n'

        if error < 0.1:
            info_text += f'[OK] Exact Match!\n'
        else:
            info_text += f'Error: {error:.2f} t ({error_pct:.2f}%)\n'

        info_text += f'\nAverage Density: {avg_weight:.2f} t/m\n'
        info_text += f'Maximum Density: {max_weight:.2f} t/m'

        ax.text(0.02, 0.98, info_text,
                transform=ax.transAxes, fontsize=9, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

        self.lightship_figure.tight_layout(pad=1.5)
        self.lightship_canvas.draw()

    def update_combined_plot(self):
        """更新综合视图"""
        self.combined_figure.clear()

        # 创建4个子图
        ax1 = self.combined_figure.add_subplot(4, 1, 1)
        ax2 = self.combined_figure.add_subplot(4, 1, 2)
        ax3 = self.combined_figure.add_subplot(4, 1, 3)
        ax4 = self.combined_figure.add_subplot(4, 1, 4)

        # 1. 邦金曲线 - 多条吃水线
        x_positions = BONJEAN_CURVE_DATA['x_positions']
        draughts = BONJEAN_CURVE_DATA['draughts']

        # 选择几条代表性吃水线
        selected_draughts = [0, len(draughts)//4, len(draughts)//2, 3*len(draughts)//4, len(draughts)-1]
        colors = ['blue', 'green', 'orange', 'red', 'purple']

        for idx, d_idx in enumerate(selected_draughts):
            draught = draughts[d_idx]
            areas = BONJEAN_CURVE_DATA['areas'][d_idx, :]
            ax1.plot(x_positions, areas, color=colors[idx], linewidth=1.5,
                    label=f'T={draught:.1f}m', alpha=0.7)

        ax1.set_xlabel('Distance from AP (m)', fontsize=9)
        ax1.set_ylabel('Area (m^2)', fontsize=9)
        ax1.set_title('Bonjean Curve - Sectional Area at Different Draughts', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc='upper right', fontsize=7)

        # 2. 空船重量分布
        lw_data = LIGHTSHIP_WEIGHT_DATA
        fp_data = FRAME_POSITION_DATA

        ax2.fill_between(fp_data['positions'], 0, lw_data['weights'],
                        color='red', alpha=0.6, edgecolor='darkred', linewidth=0.5)
        ax2.plot(fp_data['positions'], lw_data['weights'], 'r-', linewidth=1.5)
        ax2.set_xlabel('Distance from AP (m)', fontsize=9)
        ax2.set_ylabel('Weight (t/m)', fontsize=9)
        ax2.set_title('Lightship Weight Distribution', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y')
        ax2.set_xlim([fp_data['positions'].min(), fp_data['positions'].max()])

        # 3. 肋骨位置曲线
        ax3.plot(fp_data['frames'], fp_data['positions'], 'b-', linewidth=2, marker='o',
                markersize=2, markerfacecolor='blue', markeredgecolor='darkblue')
        ax3.set_xlabel('Frame Number', fontsize=9)
        ax3.set_ylabel('Distance from AP (m)', fontsize=9)
        ax3.set_title('Frame Position Curve', fontsize=11, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim([0, 270])

        # 4. 肋骨位置散点图
        ax4.scatter(fp_data['positions'], fp_data['frames'], s=15, c='black', alpha=0.6, marker='.')
        ax4.set_xlabel('Distance from AP (m)', fontsize=9)
        ax4.set_ylabel('Frame Number', fontsize=9)
        ax4.set_title('Frame Distribution along Ship Length', fontsize=11, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.set_xlim([fp_data['positions'].min(), fp_data['positions'].max()])
        ax4.set_ylim([0, 270])

        self.combined_figure.tight_layout(pad=1.5)
        self.combined_canvas.draw()

