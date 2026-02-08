"""
装载工况编辑标签页 (Loading Condition Tab)
用于编辑装载工况、添加重量项、舱室装载等
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QPushButton, QLabel, QLineEdit, QComboBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QDoubleSpinBox, QMessageBox, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.loading_condition import LoadingCondition, WeightItem
from ship_data.ship_particulars import LOADING_CONDITIONS
from ship_data.tank_data import ALL_TANKS


class LoadingTab(QWidget):
    """装载工况编辑标签页"""
    
    calculation_completed = pyqtSignal(bool)  # 计算完成信号
    
    def __init__(self, calc_engine):
        super().__init__()
        self.calc_engine = calc_engine
        self.loading_condition = None
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # 工况基本信息
        info_group = self.create_info_group()
        layout.addWidget(info_group)
        
        # 舱室装载
        tank_group = self.create_tank_group()
        layout.addWidget(tank_group)
        
        # 货物装载
        cargo_group = self.create_cargo_group()
        layout.addWidget(cargo_group)
        
        # 重量项列表
        weight_list_group = self.create_weight_list_group()
        layout.addWidget(weight_list_group)
        
        # 计算按钮
        calc_layout = QHBoxLayout()
        self.calc_button = QPushButton("执行计算")
        self.calc_button.clicked.connect(self.calculate)
        self.calc_button.setMinimumHeight(40)
        calc_layout.addStretch()
        calc_layout.addWidget(self.calc_button)
        layout.addLayout(calc_layout)
        
        # 初始化工况
        self.create_new_condition()
    
    def create_info_group(self):
        """创建工况信息组"""
        group = QGroupBox("工况信息")
        layout = QFormLayout()
        
        self.condition_name_edit = QLineEdit("新建工况")
        layout.addRow("工况名称:", self.condition_name_edit)
        
        self.condition_type_combo = QComboBox()
        for key, value in LOADING_CONDITIONS.items():
            self.condition_type_combo.addItem(value, key)
        layout.addRow("工况类型:", self.condition_type_combo)
        
        self.standard_combo = QComboBox()
        self.standard_combo.addItems(["IMO", "DNV", "CCS"])
        layout.addRow("稳性规范:", self.standard_combo)
        
        group.setLayout(layout)
        return group
    
    def create_tank_group(self):
        """创建舱室装载组"""
        group = QGroupBox("舱室装载")
        layout = QHBoxLayout()
        
        # 左侧：舱室选择和装载百分比
        form_layout = QFormLayout()
        
        self.tank_combo = QComboBox()
        for tank_id, tank_info in ALL_TANKS.items():
            self.tank_combo.addItem(f"{tank_id} - {tank_info['name']}", tank_id)
        form_layout.addRow("舱室:", self.tank_combo)
        
        self.fill_spin = QDoubleSpinBox()
        self.fill_spin.setRange(0, 100)
        self.fill_spin.setValue(95)
        self.fill_spin.setSuffix(" %")
        form_layout.addRow("装载率:", self.fill_spin)
        
        add_tank_btn = QPushButton("添加舱室")
        add_tank_btn.clicked.connect(self.add_tank)
        form_layout.addRow("", add_tank_btn)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        
        group.setLayout(layout)
        return group
    
    def create_cargo_group(self):
        """创建货物装载组"""
        group = QGroupBox("货物装载")
        layout = QFormLayout()
        
        self.cargo_name_edit = QLineEdit()
        layout.addRow("货物名称:", self.cargo_name_edit)
        
        self.cargo_weight_spin = QDoubleSpinBox()
        self.cargo_weight_spin.setRange(0, 100000)
        self.cargo_weight_spin.setSuffix(" t")
        layout.addRow("重量:", self.cargo_weight_spin)
        
        self.cargo_lcg_spin = QDoubleSpinBox()
        self.cargo_lcg_spin.setRange(0, 200)
        self.cargo_lcg_spin.setSuffix(" m")
        layout.addRow("LCG:", self.cargo_lcg_spin)
        
        self.cargo_vcg_spin = QDoubleSpinBox()
        self.cargo_vcg_spin.setRange(0, 50)
        self.cargo_vcg_spin.setSuffix(" m")
        layout.addRow("VCG:", self.cargo_vcg_spin)
        
        add_cargo_btn = QPushButton("添加货物")
        add_cargo_btn.clicked.connect(self.add_cargo)
        layout.addRow("", add_cargo_btn)
        
        group.setLayout(layout)
        return group
    
    def create_weight_list_group(self):
        """创建重量项列表组"""
        group = QGroupBox("重量项列表")
        layout = QVBoxLayout()
        
        self.weight_table = QTableWidget()
        self.weight_table.setColumnCount(6)
        self.weight_table.setHorizontalHeaderLabels(
            ["名称", "重量(t)", "LCG(m)", "VCG(m)", "TCG(m)", "FSM(t·m)"]
        )
        self.weight_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.weight_table)
        
        # 删除按钮
        delete_btn = QPushButton("删除选中项")
        delete_btn.clicked.connect(self.delete_selected_item)
        layout.addWidget(delete_btn)
        
        group.setLayout(layout)
        return group
    
    def create_new_condition(self):
        """创建新工况"""
        condition_type = self.condition_type_combo.currentData()
        self.loading_condition = LoadingCondition("新建工况", condition_type)
        self.update_weight_table()
    
    def add_tank(self):
        """添加舱室装载"""
        tank_id = self.tank_combo.currentData()
        fill_percentage = self.fill_spin.value()
        
        try:
            self.loading_condition.add_tank_loading(tank_id, fill_percentage)
            self.update_weight_table()
        except Exception as e:
            QMessageBox.warning(self, "错误", f"添加舱室失败: {str(e)}")
    
    def add_cargo(self):
        """添加货物"""
        name = self.cargo_name_edit.text()
        if not name:
            QMessageBox.warning(self, "错误", "请输入货物名称")
            return
        
        weight = self.cargo_weight_spin.value()
        lcg = self.cargo_lcg_spin.value()
        vcg = self.cargo_vcg_spin.value()
        
        self.loading_condition.add_cargo(name, weight, lcg, vcg)
        self.update_weight_table()
        
        # 清空输入
        self.cargo_name_edit.clear()
        self.cargo_weight_spin.setValue(0)

    def delete_selected_item(self):
        """删除选中的重量项"""
        current_row = self.weight_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "错误", "请选择要删除的项")
            return

        # 不能删除空船重量（第一项）
        if current_row == 0:
            QMessageBox.warning(self, "错误", "不能删除空船重量")
            return

        # 删除重量项
        del self.loading_condition.weight_items[current_row]
        self.update_weight_table()

    def update_weight_table(self):
        """更新重量项表格"""
        self.weight_table.setRowCount(0)

        for item in self.loading_condition.weight_items:
            row = self.weight_table.rowCount()
            self.weight_table.insertRow(row)

            self.weight_table.setItem(row, 0, QTableWidgetItem(item.name))
            self.weight_table.setItem(row, 1, QTableWidgetItem(f"{item.weight:.2f}"))
            self.weight_table.setItem(row, 2, QTableWidgetItem(f"{item.lcg:.2f}"))
            self.weight_table.setItem(row, 3, QTableWidgetItem(f"{item.vcg:.2f}"))
            self.weight_table.setItem(row, 4, QTableWidgetItem(f"{item.tcg:.2f}"))
            self.weight_table.setItem(row, 5, QTableWidgetItem(f"{item.fsm:.2f}"))

    def calculate(self):
        """执行计算"""
        try:
            # 更新工况名称和类型
            self.loading_condition.name = self.condition_name_edit.text()
            condition_type = self.condition_type_combo.currentData()
            self.loading_condition.condition_type = condition_type

            # 设置装载工况
            self.calc_engine.set_loading_condition(self.loading_condition)

            # 执行计算
            standard = self.standard_combo.currentText()
            results = self.calc_engine.calculate_all(standard)

            # 发送计算完成信号
            self.calculation_completed.emit(True)

        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"计算过程中出现错误:\n{str(e)}")
            self.calculation_completed.emit(False)

    def clear_all(self):
        """清空所有数据"""
        self.create_new_condition()
        self.condition_name_edit.setText("新建工况")

