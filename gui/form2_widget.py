"""
FORM 2 - 稳性计算界面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QLabel, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from gui.calculation_engine import StabilityCalculator


class Form2Widget(QWidget):
    """FORM 2 - 稳性计算"""
    
    data_updated = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.results = None
        self.calculator = StabilityCalculator()
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        from PyQt5.QtWidgets import QTabWidget

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(15, 15, 15, 15)

        # 标题
        title = QLabel("FORM 2 - 稳性与强度计算结果")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("QLabel { color: #1976D2; padding: 10px; }")
        layout.addWidget(title)

        # 创建子标签页
        self.sub_tabs = QTabWidget()
        layout.addWidget(self.sub_tabs)

        # 稳性计算标签页
        stability_widget = QWidget()
        stability_layout = QVBoxLayout(stability_widget)
        stability_layout.setSpacing(12)
        stability_layout.setContentsMargins(10, 10, 10, 10)

        # 浮态参数
        floating_group = self.create_floating_group()
        stability_layout.addWidget(floating_group)

        # 稳性参数
        stability_group = self.create_stability_group()
        stability_layout.addWidget(stability_group)

        # GZ曲线表格和图表
        hz_layout = QHBoxLayout()
        hz_layout.setSpacing(15)

        # GZ表格
        gz_table_group = self.create_gz_table_group()
        hz_layout.addWidget(gz_table_group, 1)

        # GZ曲线图
        gz_plot_group = self.create_gz_plot_group()
        hz_layout.addWidget(gz_plot_group, 2)

        stability_layout.addLayout(hz_layout, 1)

        # 稳性衡准
        criteria_group = self.create_criteria_group()
        stability_layout.addWidget(criteria_group)

        self.sub_tabs.addTab(stability_widget, "稳性计算")

        # 强度计算标签页
        strength_widget = self.create_strength_widget()
        self.sub_tabs.addTab(strength_widget, "强度计算")
        
    def create_floating_group(self):
        """创建浮态参数组"""
        group = QGroupBox("浮态参数 (Floating Parameters)")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        row = 0
        # 排水量
        label = QLabel("排水量 (Displacement):")
        label.setMinimumWidth(150)
        layout.addWidget(label, row, 0)
        self.displacement_label = QLabel("0.0 t")
        self.displacement_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.displacement_label.setStyleSheet("QLabel { color: #4CAF50; }")
        self.displacement_label.setMinimumWidth(100)
        layout.addWidget(self.displacement_label, row, 1)

        # 吃水
        layout.addWidget(QLabel("吃水 (Draught):"), row, 2)
        self.draught_label = QLabel("0.00 m")
        self.draught_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.draught_label.setStyleSheet("QLabel { color: #2196F3; }")
        self.draught_label.setMinimumWidth(100)
        layout.addWidget(self.draught_label, row, 3)

        # LCG
        layout.addWidget(QLabel("LCG:"), row, 4)
        self.lcg_label = QLabel("0.00 m")
        self.lcg_label.setFont(QFont("Arial", 10))
        self.lcg_label.setMinimumWidth(80)
        layout.addWidget(self.lcg_label, row, 5)

        row += 1
        # Trim
        layout.addWidget(QLabel("纵倾 (Trim):"), row, 0)
        self.trim_label = QLabel("0.00 m")
        self.trim_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.trim_label, row, 1)

        # LCB
        layout.addWidget(QLabel("LCB:"), row, 2)
        self.lcb_label = QLabel("0.00 m")
        self.lcb_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.lcb_label, row, 3)

        # MCT
        layout.addWidget(QLabel("MCT:"), row, 4)
        self.mct_label = QLabel("0.00 t·m/cm")
        self.mct_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.mct_label, row, 5)

        layout.setColumnStretch(6, 1)

        group.setLayout(layout)
        return group
        
    def create_stability_group(self):
        """创建稳性参数组"""
        group = QGroupBox("稳性参数 (Stability Parameters)")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        row = 0
        # KM
        label = QLabel("KM:")
        label.setMinimumWidth(150)
        layout.addWidget(label, row, 0)
        self.km_label = QLabel("0.00 m")
        self.km_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.km_label.setStyleSheet("QLabel { color: #FF9800; }")
        self.km_label.setMinimumWidth(100)
        layout.addWidget(self.km_label, row, 1)

        # VCG (KG)
        layout.addWidget(QLabel("VCG (KG):"), row, 2)
        self.vcg_label = QLabel("0.00 m")
        self.vcg_label.setFont(QFont("Arial", 10))
        self.vcg_label.setMinimumWidth(80)
        layout.addWidget(self.vcg_label, row, 3)

        # GM0
        layout.addWidget(QLabel("GM₀ (solid):"), row, 4)
        self.gm0_label = QLabel("0.00 m")
        self.gm0_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.gm0_label.setStyleSheet("QLabel { color: #9C27B0; }")
        self.gm0_label.setMinimumWidth(80)
        layout.addWidget(self.gm0_label, row, 5)

        row += 1
        # dGM
        layout.addWidget(QLabel("dGM (FS corr):"), row, 0)
        self.dgm_label = QLabel("0.00 m")
        self.dgm_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.dgm_label, row, 1)

        # GMf
        layout.addWidget(QLabel("GMf (fluid):"), row, 2)
        self.gmf_label = QLabel("0.00 m")
        self.gmf_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.gmf_label.setStyleSheet("QLabel { color: #E91E63; }")
        layout.addWidget(self.gmf_label, row, 3)

        # KGf
        layout.addWidget(QLabel("KGf:"), row, 4)
        self.kgf_label = QLabel("0.00 m")
        self.kgf_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.kgf_label, row, 5)

        layout.setColumnStretch(6, 1)

        group.setLayout(layout)
        return group
        
    def create_gz_table_group(self):
        """创建GZ表格组"""
        group = QGroupBox("GZ曲线数据")
        layout = QVBoxLayout()
        
        self.gz_table = QTableWidget()
        self.gz_table.setColumnCount(5)
        self.gz_table.setHorizontalHeaderLabels([
            "横倾角\n[deg]", "sin(θ)", "KN\n[m]", "KGf×sin(θ)\n[m]", "GZ\n[m]"
        ])
        self.gz_table.setFont(QFont("Arial", 9))
        
        layout.addWidget(self.gz_table)
        group.setLayout(layout)
        return group
        
    def create_gz_plot_group(self):
        """创建GZ曲线图组"""
        group = QGroupBox("GZ曲线图")
        layout = QVBoxLayout()
        
        # 创建matplotlib图表
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        group.setLayout(layout)
        return group
        
    def create_criteria_group(self):
        """创建稳性衡准组"""
        group = QGroupBox("稳性衡准")
        layout = QVBoxLayout()
        
        self.criteria_table = QTableWidget()
        self.criteria_table.setColumnCount(5)
        self.criteria_table.setHorizontalHeaderLabels([
            "衡准代码", "衡准说明", "要求值", "实际值", "状态"
        ])
        self.criteria_table.setFont(QFont("Arial", 9))
        
        layout.addWidget(self.criteria_table)
        group.setLayout(layout)
        return group
        
    def calculate(self, loading_data):
        """执行稳性计算"""
        try:
            print(f"\n=== Form2.calculate() ===")
            print(f"接收到的数据: {loading_data.keys()}")

            # 提取装载数据
            displacement = loading_data.get('displacement', 0)
            lcg = loading_data.get('lcg', 0)
            vcg = loading_data.get('vcg', 0)
            fsm = loading_data.get('fsm', 0)

            print(f"排水量: {displacement:.1f} t")
            print(f"LCG: {lcg:.2f} m")
            print(f"VCG: {vcg:.2f} m")
            print(f"FSM: {fsm:.1f} t·m")

            # 计算浮态参数
            print("正在计算浮态参数...")
            floating = self.calculator.calculate_floating_position(displacement)
            draught = floating['draught']
            km = floating['km']
            lcb = floating['lcb']
            mct = floating['mct']
            print(f"吃水: {draught:.2f} m, KM: {km:.2f} m")

            # 计算稳性参数
            print("正在计算稳性参数...")
            stability = self.calculator.calculate_stability_parameters(displacement, vcg, fsm)
            gm0 = stability['gm0']
            dgm = stability['dgm']
            gmf = stability['gmf']
            kgf = stability['kgf']
            print(f"GM0: {gm0:.2f} m, GMf: {gmf:.2f} m")

            # 计算GZ曲线
            print("正在计算GZ曲线...")
            gz_curve = self.calculator.calculate_gz_curve(displacement, vcg, fsm, draught, trim=0.0)
            print(f"GZ曲线点数: {len(gz_curve['angles'])}")

            # 检查稳性衡准
            print("正在检查稳性衡准...")
            criteria = self.calculator.check_stability_criteria(gz_curve, gmf)
            print(f"稳性衡准: {len(criteria)} 项")

            # 计算强度
            print("正在计算强度...")
            print(f"  装载数据项数: {len(loading_data.get('items', []))}")
            print(f"  吃水: {draught:.2f} m")
            try:
                strength = self.calculator.calculate_strength(loading_data, draught, trim=0.0)
                if strength:
                    print(f"✓ 强度计算完成:")
                    print(f"  最大剪力: {strength.get('max_shear_force', 0):.2f} kN")
                    print(f"  数据点数: {len(strength.get('stations', []))}")
                else:
                    print("✗ 强度计算返回None")
            except Exception as e:
                print(f"✗ 强度计算错误: {e}")
                import traceback
                traceback.print_exc()
                strength = None

            # 保存结果
            self.results = {
                'displacement': displacement,
                'lcg': lcg,
                'vcg': vcg,
                'kg': vcg,
                'fsm': fsm,
                'draught': draught,
                'trim': 0.0,
                'lcb': lcb,
                'mct': mct,
                'km': km,
                'gm0': gm0,
                'dgm': dgm,
                'gmf': gmf,
                'kgf': kgf,
                'gz_curve': gz_curve,
                'criteria': criteria,
                'strength': strength,
            }

            print("结果已保存")

            # 更新界面
            print("正在更新界面...")
            self.update_display()
            print("界面更新完成")

            # 发射信号
            self.data_updated.emit()
            print("信号已发射")
            print("=== 计算完成 ===\n")

        except Exception as e:
            print(f"计算错误: {e}")
            import traceback
            traceback.print_exc()
        
    def update_display(self):
        """更新界面显示"""
        if not self.results:
            return

        # 更新浮态参数
        self.displacement_label.setText(f"{self.results['displacement']:.1f} t")
        self.draught_label.setText(f"{self.results['draught']:.2f} m")
        self.lcg_label.setText(f"{self.results['lcg']:.2f} m")
        self.trim_label.setText(f"{self.results['trim']:.2f} m")
        self.lcb_label.setText(f"{self.results['lcb']:.2f} m")
        self.mct_label.setText(f"{self.results['mct']:.2f} t·m/cm")

        # 更新稳性参数
        self.km_label.setText(f"{self.results['km']:.2f} m")
        self.vcg_label.setText(f"{self.results['vcg']:.2f} m")
        self.gm0_label.setText(f"{self.results['gm0']:.2f} m")
        self.dgm_label.setText(f"{self.results['dgm']:.2f} m")
        self.gmf_label.setText(f"{self.results['gmf']:.2f} m")
        self.kgf_label.setText(f"{self.results['kgf']:.2f} m")

        # 更新GZ表格
        self.update_gz_table()

        # 更新GZ曲线图
        self.update_gz_plot()

        # 更新稳性衡准表格
        self.update_criteria_table()

        # 更新强度计算显示
        self.update_strength_display()

    def update_gz_table(self):
        """更新GZ表格"""
        if not self.results or 'gz_curve' not in self.results:
            return

        gz_data = self.results['gz_curve']
        angles = gz_data['angles']
        kn = gz_data['kn']
        kgf_sin = gz_data['kgf_sin']
        gz = gz_data['gz']

        self.gz_table.setRowCount(len(angles))

        for i, angle in enumerate(angles):
            # 横倾角
            self.gz_table.setItem(i, 0, QTableWidgetItem(f"{angle:.0f}"))
            # sin(θ)
            self.gz_table.setItem(i, 1, QTableWidgetItem(f"{np.sin(np.radians(angle)):.3f}"))
            # KN
            self.gz_table.setItem(i, 2, QTableWidgetItem(f"{kn[i]:.3f}"))
            # KGf×sin(θ)
            self.gz_table.setItem(i, 3, QTableWidgetItem(f"{kgf_sin[i]:.3f}"))
            # GZ
            item = QTableWidgetItem(f"{gz[i]:.3f}")
            item.setFont(QFont("Arial", 9, QFont.Bold))
            self.gz_table.setItem(i, 4, item)

    def update_gz_plot(self):
        """更新GZ曲线图"""
        if not self.results or 'gz_curve' not in self.results:
            return

        gz_data = self.results['gz_curve']
        angles = gz_data['angles']
        gz = gz_data['gz']

        # 清除之前的图
        self.figure.clear()

        # 创建子图
        ax = self.figure.add_subplot(111)

        # 绘制GZ曲线
        ax.plot(angles, gz, 'b-o', linewidth=2, markersize=6, label='GZ (Righting Lever)')
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.grid(True, alpha=0.3)

        ax.set_xlabel('Heeling Angle (deg)', fontsize=10)
        ax.set_ylabel('GZ (m)', fontsize=10)
        ax.set_title('GZ Curve', fontsize=12, fontweight='bold')
        ax.legend()

        # 刷新画布
        self.canvas.draw()

    def update_criteria_table(self):
        """更新稳性衡准表格"""
        if not self.results or 'criteria' not in self.results:
            return

        criteria = self.results['criteria']

        self.criteria_table.setRowCount(len(criteria))

        row = 0
        for code, data in criteria.items():
            # 衡准代码
            self.criteria_table.setItem(row, 0, QTableWidgetItem(code))
            # 衡准说明
            self.criteria_table.setItem(row, 1, QTableWidgetItem(data['name']))
            # 要求值
            self.criteria_table.setItem(row, 2, QTableWidgetItem(f"{data['required']:.3f} {data['unit']}"))
            # 实际值
            self.criteria_table.setItem(row, 3, QTableWidgetItem(f"{data['actual']:.3f} {data['unit']}"))
            # 状态
            status = "✓ 通过" if data['pass'] else "✗ 不通过"
            status_item = QTableWidgetItem(status)
            if data['pass']:
                status_item.setForeground(QColor(0, 128, 0))  # 绿色
            else:
                status_item.setForeground(QColor(255, 0, 0))  # 红色
            status_item.setFont(QFont("Arial", 9, QFont.Bold))
            self.criteria_table.setItem(row, 4, status_item)

            row += 1

    def clear_all(self):
        """清空所有数据"""
        self.results = None
        self.gz_table.setRowCount(0)
        self.criteria_table.setRowCount(0)

        # 清空标签
        self.displacement_label.setText("0.0 t")
        self.draught_label.setText("0.00 m")
        self.lcg_label.setText("0.00 m")
        self.trim_label.setText("0.00 m")
        self.lcb_label.setText("0.00 m")
        self.mct_label.setText("0.00 t·m/cm")

        self.km_label.setText("0.00 m")
        self.vcg_label.setText("0.00 m")
        self.gm0_label.setText("0.00 m")
        self.dgm_label.setText("0.00 m")
        self.gmf_label.setText("0.00 m")
        self.kgf_label.setText("0.00 m")

        # 清空图表
        self.figure.clear()
        self.canvas.draw()

    def get_results(self):
        """获取计算结果"""
        return self.results

    def create_strength_widget(self):
        """创建强度计算部件"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)

        # 强度参数表格
        params_group = QGroupBox("强度参数 (Strength Parameters)")
        params_group.setFont(QFont("Arial", 10, QFont.Bold))
        params_layout = QVBoxLayout()
        params_layout.setContentsMargins(20, 20, 20, 20)

        self.strength_table = QTableWidget()
        self.strength_table.setColumnCount(2)
        self.strength_table.setHorizontalHeaderLabels(["参数", "数值"])
        self.strength_table.horizontalHeader().setStretchLastSection(True)
        self.strength_table.setAlternatingRowColors(True)
        params_layout.addWidget(self.strength_table)
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # 强度曲线图 - 综合显示
        curves_group = QGroupBox("船舶强度曲线 (Ship Strength Curves)")
        curves_group.setFont(QFont("Arial", 10, QFont.Bold))
        curves_layout = QVBoxLayout()
        curves_layout.setContentsMargins(10, 10, 10, 10)

        # 创建一个大的图形，包含4个子图
        self.strength_figure = Figure(figsize=(14, 10))
        self.strength_canvas = FigureCanvas(self.strength_figure)
        curves_layout.addWidget(self.strength_canvas)
        curves_group.setLayout(curves_layout)

        layout.addWidget(curves_group, 1)

        return widget

    def update_strength_display(self):
        """更新强度计算显示"""
        if not self.results:
            print("update_strength_display: 没有计算结果")
            return

        if 'strength' not in self.results:
            print("update_strength_display: 结果中没有强度数据")
            return

        strength = self.results['strength']

        if strength is None:
            print("update_strength_display: 强度数据为None")
            return

        print(f"update_strength_display: 开始更新强度显示，数据点数={len(strength.get('stations', []))}")

        # 更新强度参数表格
        params = [
            ("最大剪力 (Max Shear Force)",
             f"{strength['max_shear_force']:.2f} kN @ Frame {self._position_to_frame(strength['position_max_shear']):.0f}"),
            ("最大中拱弯矩 (Max Sagging Moment)",
             f"{strength['max_sagging_moment']/1000:.2f} MN·m @ Frame {self._position_to_frame(strength['position_max_sagging']):.0f}"),
            ("最大中垂弯矩 (Max Hogging Moment)",
             f"{strength['max_hogging_moment']/1000:.2f} MN·m @ Frame {self._position_to_frame(strength['position_max_hogging']):.0f}"),
            ("", ""),
            ("许用剪力 (Allowable Shear Force)", f"{strength['allowable_shear_force']:.2f} kN"),
            ("许用中拱弯矩 (Allowable Sagging)", f"{strength['allowable_sagging_moment']/1000:.2f} MN·m"),
            ("许用中垂弯矩 (Allowable Hogging)", f"{strength['allowable_hogging_moment']/1000:.2f} MN·m"),
            ("", ""),
            ("剪力检查 (Shear Force Check)", "✓ 通过" if strength['shear_force_ok'] else "✗ 不通过"),
            ("中拱弯矩检查 (Sagging Check)", "✓ 通过" if strength['sagging_moment_ok'] else "✗ 不通过"),
            ("中垂弯矩检查 (Hogging Check)", "✓ 通过" if strength['hogging_moment_ok'] else "✗ 不通过"),
            ("", ""),
            ("边界条件 (Boundary Conditions)", ""),
            ("V(0)", f"{strength['boundary_check']['V(0)']:.6f} t"),
            ("V(L)", f"{strength['boundary_check']['V(L)']:.6f} t"),
            ("M(0)", f"{strength['boundary_check']['M(0)']:.6f} t·m"),
            ("M(L)", f"{strength['boundary_check']['M(L)']:.6f} t·m"),
        ]

        self.strength_table.setRowCount(len(params))
        for i, (param, value) in enumerate(params):
            param_item = QTableWidgetItem(param)
            value_item = QTableWidgetItem(value)

            # 加粗特定行
            if "边界条件" in param or "检查" in param:
                font = QFont("Arial", 9, QFont.Bold)
                param_item.setFont(font)
                value_item.setFont(font)

            # 设置颜色
            if "✓ 通过" in value:
                value_item.setForeground(QColor(0, 128, 0))
            elif "✗ 不通过" in value:
                value_item.setForeground(QColor(255, 0, 0))

            self.strength_table.setItem(i, 0, param_item)
            self.strength_table.setItem(i, 1, value_item)

        # 更新综合强度曲线图
        self.update_strength_plots(strength)

    def _position_to_frame(self, position):
        """将位置转换为肋骨号"""
        # Frame 0 在 -4.24m, 间距 0.8m
        return (position + 4.24) / 0.8

    def update_strength_plots(self, strength):
        """更新综合强度曲线图 - 在一张图中显示重力、浮力、剪力、弯矩"""
        self.strength_figure.clear()

        # 转换位置为Frame号
        frames = [(pos + 4.24) / 0.8 for pos in strength['stations']]

        # 创建2x2子图布局
        # 子图1: 重力分布
        ax1 = self.strength_figure.add_subplot(2, 2, 1)
        weight_density = strength['weight_density']  # t/m
        ax1.plot(frames, weight_density, 'r-', linewidth=1.5, label='Weight Density')
        ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax1.set_xlabel('Frame Number', fontsize=9)
        ax1.set_ylabel('Weight Density (t/m)', fontsize=9)
        ax1.set_title('Weight Distribution', fontsize=10, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend(fontsize=8)

        # 子图2: 浮力分布
        ax2 = self.strength_figure.add_subplot(2, 2, 2)
        buoyancy_density = strength['buoyancy_density']  # t/m
        ax2.plot(frames, buoyancy_density, 'b-', linewidth=1.5, label='Buoyancy Density')
        ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax2.set_xlabel('Frame Number', fontsize=9)
        ax2.set_ylabel('Buoyancy Density (t/m)', fontsize=9)
        ax2.set_title('Buoyancy Distribution', fontsize=10, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend(fontsize=8)

        # 子图3: 剪力曲线
        ax3 = self.strength_figure.add_subplot(2, 2, 3)
        shear_force = strength['shear_force']  # kN
        ax3.plot(frames, shear_force, 'g-', linewidth=1.5, label='Shear Force')
        ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # 绘制许用值线
        if strength['allowable_shear_force'] > 0:
            ax3.axhline(y=strength['allowable_shear_force'], color='r', linestyle='--',
                       linewidth=1, label=f'Allowable: ±{strength["allowable_shear_force"]:.0f} kN')
            ax3.axhline(y=-strength['allowable_shear_force'], color='r', linestyle='--', linewidth=1)

        # 标注最大值
        max_idx = np.argmax(np.abs(shear_force))
        ax3.plot(frames[max_idx], shear_force[max_idx], 'ro', markersize=6)

        ax3.set_xlabel('Frame Number', fontsize=9)
        ax3.set_ylabel('Shear Force (kN)', fontsize=9)
        ax3.set_title('Shear Force Curve', fontsize=10, fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.legend(fontsize=8)

        # 子图4: 弯矩曲线
        ax4 = self.strength_figure.add_subplot(2, 2, 4)
        bending_moment = [bm / 1000 for bm in strength['bending_moment']]  # 转换为MN·m
        ax4.plot(frames, bending_moment, 'm-', linewidth=1.5, label='Bending Moment')
        ax4.axhline(y=0, color='k', linestyle='-', linewidth=0.5)

        # 绘制许用值线
        if strength['allowable_sagging_moment'] > 0:
            ax4.axhline(y=strength['allowable_sagging_moment']/1000, color='r', linestyle='--',
                       linewidth=1, label=f'Allow. Sag: {strength["allowable_sagging_moment"]/1000:.0f} MN·m')
        if strength['allowable_hogging_moment'] > 0:
            ax4.axhline(y=-strength['allowable_hogging_moment']/1000, color='r', linestyle='--',
                       linewidth=1, label=f'Allow. Hog: {strength["allowable_hogging_moment"]/1000:.0f} MN·m')

        # 标注最大值
        max_idx = np.argmax(np.abs(bending_moment))
        ax4.plot(frames[max_idx], bending_moment[max_idx], 'ro', markersize=6)

        ax4.set_xlabel('Frame Number', fontsize=9)
        ax4.set_ylabel('Bending Moment (MN·m)', fontsize=9)
        ax4.set_title('Bending Moment Curve', fontsize=10, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        ax4.legend(fontsize=8)

        self.strength_figure.tight_layout(pad=2.0)
        self.strength_canvas.draw()

