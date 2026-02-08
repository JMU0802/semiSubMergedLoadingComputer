"""
Compartment manager widget
舱室装载管理
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QDialog, QFormLayout, QLineEdit,
                             QComboBox, QDoubleSpinBox, QDialogButtonBox)
from PyQt5.QtCore import Qt

from ..models import Compartment, CompartmentType


class CompartmentDialog(QDialog):
    """Dialog for adding/editing compartment"""
    
    def __init__(self, compartment: Compartment = None, parent=None):
        super().__init__(parent)
        self.compartment = compartment
        self.init_ui()
        
        if compartment:
            self.load_compartment()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("舱室编辑 / Compartment Editor")
        layout = QFormLayout(self)
        
        self.name_edit = QLineEdit()
        self.type_combo = QComboBox()
        for ctype in CompartmentType:
            self.type_combo.addItem(ctype.value, ctype)
        
        self.capacity_spin = QDoubleSpinBox()
        self.capacity_spin.setRange(0, 100000)
        self.capacity_spin.setDecimals(2)
        self.capacity_spin.setSuffix(" m³")
        
        self.lcg_spin = QDoubleSpinBox()
        self.lcg_spin.setRange(-200, 200)
        self.lcg_spin.setDecimals(2)
        self.lcg_spin.setSuffix(" m")
        
        self.tcg_spin = QDoubleSpinBox()
        self.tcg_spin.setRange(-50, 50)
        self.tcg_spin.setDecimals(2)
        self.tcg_spin.setSuffix(" m")
        
        self.vcg_spin = QDoubleSpinBox()
        self.vcg_spin.setRange(0, 50)
        self.vcg_spin.setDecimals(2)
        self.vcg_spin.setSuffix(" m")
        
        self.density_spin = QDoubleSpinBox()
        self.density_spin.setRange(0.5, 2.0)
        self.density_spin.setDecimals(3)
        self.density_spin.setValue(1.025)
        self.density_spin.setSuffix(" t/m³")
        
        self.fill_spin = QDoubleSpinBox()
        self.fill_spin.setRange(0, 100)
        self.fill_spin.setDecimals(1)
        self.fill_spin.setSuffix(" %")
        
        self.fsm_spin = QDoubleSpinBox()
        self.fsm_spin.setRange(0, 100000)
        self.fsm_spin.setDecimals(2)
        self.fsm_spin.setSuffix(" t·m")
        
        layout.addRow("名称 Name:", self.name_edit)
        layout.addRow("类型 Type:", self.type_combo)
        layout.addRow("容积 Capacity:", self.capacity_spin)
        layout.addRow("纵向重心 LCG:", self.lcg_spin)
        layout.addRow("横向重心 TCG:", self.tcg_spin)
        layout.addRow("垂向重心 VCG:", self.vcg_spin)
        layout.addRow("密度 Density:", self.density_spin)
        layout.addRow("装载率 Fill %:", self.fill_spin)
        layout.addRow("自由液面 FSM:", self.fsm_spin)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def load_compartment(self):
        """Load compartment data into form"""
        self.name_edit.setText(self.compartment.name)
        index = self.type_combo.findData(self.compartment.type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        self.capacity_spin.setValue(self.compartment.capacity)
        self.lcg_spin.setValue(self.compartment.lcg)
        self.tcg_spin.setValue(self.compartment.tcg)
        self.vcg_spin.setValue(self.compartment.vcg)
        self.density_spin.setValue(self.compartment.density)
        self.fill_spin.setValue(self.compartment.fill_percentage)
        self.fsm_spin.setValue(self.compartment.fsm)
    
    def get_compartment(self) -> Compartment:
        """Get compartment from form data"""
        return Compartment(
            name=self.name_edit.text(),
            type=self.type_combo.currentData(),
            capacity=self.capacity_spin.value(),
            lcg=self.lcg_spin.value(),
            tcg=self.tcg_spin.value(),
            vcg=self.vcg_spin.value(),
            density=self.density_spin.value(),
            fill_percentage=self.fill_spin.value(),
            fsm=self.fsm_spin.value()
        )


class CompartmentManagerWidget(QWidget):
    """
    舱室装载管理 / Compartment Loading Manager
    """
    
    def __init__(self):
        super().__init__()
        self.compartments = []
        self.init_ui()
        self.add_sample_compartments()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        group = QGroupBox("舱室装载 / Compartment Loading")
        group_layout = QVBoxLayout()
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("添加 Add")
        add_btn.clicked.connect(self.add_compartment)
        edit_btn = QPushButton("编辑 Edit")
        edit_btn.clicked.connect(self.edit_compartment)
        delete_btn = QPushButton("删除 Delete")
        delete_btn.clicked.connect(self.delete_compartment)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        
        group_layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "名称 Name", "类型 Type", "容积 Cap.(m³)", 
            "装载率 Fill%", "重量 Wt.(t)", "LCG(m)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        group_layout.addWidget(self.table)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def add_sample_compartments(self):
        """Add sample compartments"""
        samples = [
            Compartment("Ballast Tank #1", CompartmentType.BALLAST, 500, -60, 0, 5, 1.025, 80, 150),
            Compartment("Ballast Tank #2", CompartmentType.BALLAST, 500, 60, 0, 5, 1.025, 75, 145),
            Compartment("Fuel Oil Tank", CompartmentType.FUEL, 300, -30, 5, 8, 0.95, 50, 100),
        ]
        
        for comp in samples:
            self.compartments.append(comp)
        
        self.update_table()
    
    def update_table(self):
        """Update table display"""
        self.table.setRowCount(len(self.compartments))
        
        for i, comp in enumerate(self.compartments):
            self.table.setItem(i, 0, QTableWidgetItem(comp.name))
            self.table.setItem(i, 1, QTableWidgetItem(comp.type.value))
            self.table.setItem(i, 2, QTableWidgetItem(f"{comp.capacity:.1f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{comp.fill_percentage:.1f}"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{comp.weight:.2f}"))
            self.table.setItem(i, 5, QTableWidgetItem(f"{comp.lcg:.2f}"))
    
    def add_compartment(self):
        """Add new compartment"""
        dialog = CompartmentDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.compartments.append(dialog.get_compartment())
            self.update_table()
    
    def edit_compartment(self):
        """Edit selected compartment"""
        row = self.table.currentRow()
        if row >= 0:
            dialog = CompartmentDialog(self.compartments[row], parent=self)
            if dialog.exec_() == QDialog.Accepted:
                self.compartments[row] = dialog.get_compartment()
                self.update_table()
    
    def delete_compartment(self):
        """Delete selected compartment"""
        row = self.table.currentRow()
        if row >= 0:
            del self.compartments[row]
            self.update_table()
    
    def get_compartments(self):
        """Get all compartments"""
        return self.compartments.copy()
