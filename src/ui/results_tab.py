"""
计算结果显示标签页 (Results Tab)
显示浮态、稳性、强度计算结果
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QTableWidget, QTableWidgetItem, QHeaderView,
                             QTextEdit, QTabWidget, QPushButton, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.ui.plot_widget import PlotWidget


class ResultsTab(QWidget):
    """计算结果显示标签页"""
    
    def __init__(self, calc_engine):
        super().__init__()
        self.calc_engine = calc_engine
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 创建子标签页
        self.sub_tabs = QTabWidget()
        layout.addWidget(self.sub_tabs)
        
        # 摘要标签页
        self.summary_widget = self.create_summary_widget()
        self.sub_tabs.addTab(self.summary_widget, "计算摘要")
        
        # 浮态结果标签页
        self.flotation_widget = self.create_flotation_widget()
        self.sub_tabs.addTab(self.flotation_widget, "浮态计算")
        
        # 稳性结果标签页
        self.stability_widget = self.create_stability_widget()
        self.sub_tabs.addTab(self.stability_widget, "稳性计算")
        
        # 强度结果标签页
        self.strength_widget = self.create_strength_widget()
        self.sub_tabs.addTab(self.strength_widget, "强度计算")
    
    def create_summary_widget(self):
        """创建摘要部件"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # 总体状态
        status_group = QGroupBox("总体状态")
        status_layout = QVBoxLayout()
        self.status_label = QLabel("未计算")
        self.status_label.setFont(QFont("Arial", 16, QFont.Bold))
        status_layout.addWidget(self.status_label)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        # 关键参数
        params_group = QGroupBox("关键参数")
        params_layout = QVBoxLayout()
        self.params_text = QTextEdit()
        self.params_text.setReadOnly(True)
        params_layout.addWidget(self.params_text)
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        layout.addStretch()
        
        return widget
    
    def create_flotation_widget(self):
        """创建浮态结果部件"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # 浮态参数表格
        self.flotation_table = QTableWidget()
        self.flotation_table.setColumnCount(2)
        self.flotation_table.setHorizontalHeaderLabels(["参数", "数值"])
        self.flotation_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.flotation_table)
        
        return widget
    
    def create_stability_widget(self):
        """创建稳性结果部件"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)
        
        # 稳性参数
        params_group = QGroupBox("稳性参数")
        params_layout = QVBoxLayout()
        self.stability_table = QTableWidget()
        self.stability_table.setColumnCount(2)
        self.stability_table.setHorizontalHeaderLabels(["参数", "数值"])
        self.stability_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        params_layout.addWidget(self.stability_table)
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)
        
        # GZ曲线
        gz_group = QGroupBox("GZ曲线")
        gz_layout = QVBoxLayout()
        self.gz_plot = PlotWidget()
        gz_layout.addWidget(self.gz_plot)
        gz_group.setLayout(gz_layout)
        layout.addWidget(gz_group)
        
        # 稳性衡准检查
        criteria_group = QGroupBox("稳性衡准检查")
        criteria_layout = QVBoxLayout()
        self.criteria_table = QTableWidget()
        self.criteria_table.setColumnCount(5)
        self.criteria_table.setHorizontalHeaderLabels(
            ["衡准项", "要求值", "实际值", "单位", "状态"]
        )
        self.criteria_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        criteria_layout.addWidget(self.criteria_table)
        criteria_group.setLayout(criteria_layout)
        layout.addWidget(criteria_group)
        
        return widget
    
    def create_strength_widget(self):
        """创建强度结果部件"""
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        # 强度参数表格
        params_group = QGroupBox("强度参数")
        params_layout = QVBoxLayout()
        self.strength_table = QTableWidget()
        self.strength_table.setColumnCount(2)
        self.strength_table.setHorizontalHeaderLabels(["参数", "数值"])
        self.strength_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        params_layout.addWidget(self.strength_table)
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # 剪力曲线
        sf_group = QGroupBox("剪力曲线")
        sf_layout = QVBoxLayout()
        self.sf_plot = PlotWidget()
        sf_layout.addWidget(self.sf_plot)
        sf_group.setLayout(sf_layout)
        layout.addWidget(sf_group)

        # 弯矩曲线
        bm_group = QGroupBox("弯矩曲线")
        bm_layout = QVBoxLayout()
        self.bm_plot = PlotWidget()
        bm_layout.addWidget(self.bm_plot)
        bm_group.setLayout(bm_layout)
        layout.addWidget(bm_group)

        return widget
    
    def update_results(self):
        """更新显示结果"""
        results = self.calc_engine.get_results()
        if not results:
            return
        
        # 更新摘要
        self.update_summary(results)
        
        # 更新浮态结果
        self.update_flotation(results)
        
        # 更新稳性结果
        self.update_stability(results)
        
        # 更新强度结果
        self.update_strength(results)

    def update_summary(self, results):
        """更新摘要"""
        overall = results['overall_status']

        # 更新状态标签
        if overall['all_ok']:
            self.status_label.setText("✓ 计算通过 - 所有衡准满足")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("✗ 计算未通过 - 部分衡准不满足")
            self.status_label.setStyleSheet("color: red;")

        # 更新关键参数
        summary = self.calc_engine.get_summary()
        params_text = f"""
工况名称: {summary['condition_name']}
排水量: {summary['displacement']:.2f} t
平均吃水: {summary['draught_mean']:.3f} m
首吃水: {summary['draught_fwd']:.3f} m
尾吃水: {summary['draught_aft']:.3f} m
纵倾: {summary['trim']:.3f} m
初稳性高GM: {summary['gm']:.3f} m
最大GZ: {summary['max_gz']:.3f} m

稳性检查: {'通过' if summary['stability_ok'] else '不通过'}
强度检查: {'通过' if summary['strength_ok'] else '不通过'}
        """
        self.params_text.setText(params_text)

    def update_flotation(self, results):
        """更新浮态结果"""
        flotation = results['flotation']

        data = [
            ("排水量", f"{flotation['displacement']:.2f} t"),
            ("平均吃水", f"{flotation['draught_mean']:.3f} m"),
            ("首吃水", f"{flotation['draught_fwd']:.3f} m"),
            ("尾吃水", f"{flotation['draught_aft']:.3f} m"),
            ("纵倾", f"{flotation['trim']:.3f} m"),
            ("纵倾角", f"{flotation['trim_angle']:.3f} °"),
            ("浮心纵向位置LCB", f"{flotation['lcb']:.2f} m"),
            ("浮心垂向位置VCB", f"{flotation['vcb']:.2f} m"),
            ("漂心位置LCF", f"{flotation['lcf']:.2f} m"),
            ("每厘米吃水吨数TPC", f"{flotation['tpc']:.2f} t/cm"),
            ("纵稳性高MCT", f"{flotation['mct']:.2f} t·m"),
        ]

        self.flotation_table.setRowCount(len(data))
        for i, (param, value) in enumerate(data):
            self.flotation_table.setItem(i, 0, QTableWidgetItem(param))
            self.flotation_table.setItem(i, 1, QTableWidgetItem(value))

    def update_stability(self, results):
        """更新稳性结果"""
        stability = results['stability']

        # 更新稳性参数表格
        data = [
            ("重心高度KG", f"{stability['kg']:.3f} m"),
            ("自由液面修正ΔKG", f"{stability['delta_kg']:.3f} m"),
            ("修正重心高度KG'", f"{stability['kg_corrected']:.3f} m"),
            ("浮心高度KB", f"{stability['kb']:.3f} m"),
            ("横稳心半径BM", f"{stability['bm']:.3f} m"),
            ("横稳心高度KM", f"{stability['km']:.3f} m"),
            ("初稳性高GM", f"{stability['gm']:.3f} m"),
        ]

        self.stability_table.setRowCount(len(data))
        for i, (param, value) in enumerate(data):
            self.stability_table.setItem(i, 0, QTableWidgetItem(param))
            self.stability_table.setItem(i, 1, QTableWidgetItem(value))

        # 绘制GZ曲线
        gz_curve = stability['gz_curve']
        self.gz_plot.plot_gz_curve(
            gz_curve['heel_angles'],
            gz_curve['gz_values']
        )

        # 更新稳性衡准表格
        criteria = stability['criteria_check']
        self.criteria_table.setRowCount(0)

        for key, value in criteria.items():
            if key == 'all_passed':
                continue

            row = self.criteria_table.rowCount()
            self.criteria_table.insertRow(row)

            self.criteria_table.setItem(row, 0, QTableWidgetItem(value['name']))
            self.criteria_table.setItem(row, 1, QTableWidgetItem(f"{value['required']:.3f}"))
            self.criteria_table.setItem(row, 2, QTableWidgetItem(f"{value['actual']:.3f}"))
            self.criteria_table.setItem(row, 3, QTableWidgetItem(value['unit']))

            status_item = QTableWidgetItem("通过" if value['passed'] else "不通过")
            if value['passed']:
                status_item.setBackground(QColor(144, 238, 144))  # 浅绿色
            else:
                status_item.setBackground(QColor(255, 182, 193))  # 浅红色
            self.criteria_table.setItem(row, 4, status_item)

    def update_strength(self, results):
        """更新强度结果"""
        strength = results['strength']

        # 更新强度参数表格
        params = [
            ("最大剪力", f"{strength['max_shear_force']:.2f} kN @ Frame {self._position_to_frame(strength['position_max_shear']):.0f}"),
            ("最大中拱弯矩", f"{strength['max_sagging_moment']:.2f} kN·m @ Frame {self._position_to_frame(strength['position_max_sagging']):.0f}"),
            ("最大中垂弯矩", f"{strength['max_hogging_moment']:.2f} kN·m @ Frame {self._position_to_frame(strength['position_max_hogging']):.0f}"),
            ("许用剪力", f"{strength['allowable_shear_force']:.2f} kN"),
            ("许用中拱弯矩", f"{strength['allowable_sagging_moment']:.2f} kN·m"),
            ("许用中垂弯矩", f"{strength['allowable_hogging_moment']:.2f} kN·m"),
            ("", ""),  # 空行
            ("边界条件检查", ""),
            ("V(0)", f"{strength['boundary_check']['V(0)']:.6f} t"),
            ("V(L)", f"{strength['boundary_check']['V(L)']:.6f} t"),
            ("M(0)", f"{strength['boundary_check']['M(0)']:.6f} t·m"),
            ("M(L)", f"{strength['boundary_check']['M(L)']:.6f} t·m"),
        ]

        self.strength_table.setRowCount(len(params))
        for i, (param, value) in enumerate(params):
            param_item = QTableWidgetItem(param)
            value_item = QTableWidgetItem(value)

            # 加粗边界条件检查标题
            if param == "边界条件检查":
                font = QFont()
                font.setBold(True)
                param_item.setFont(font)

            self.strength_table.setItem(i, 0, param_item)
            self.strength_table.setItem(i, 1, value_item)

        # 绘制剪力曲线
        self.sf_plot.plot_shear_force(
            strength['stations'],
            strength['shear_force'],
            strength.get('max_shear_force', 0)
        )

        # 绘制弯矩曲线
        self.bm_plot.plot_bending_moment(
            strength['stations'],
            strength['bending_moment'],
            strength.get('max_sagging_moment', 0),
            strength.get('max_hogging_moment', 0)
        )

    def _position_to_frame(self, position):
        """将位置转换为肋骨号"""
        # Frame 0 在 -4.24m, 间距 0.8m
        return (position + 4.24) / 0.8

