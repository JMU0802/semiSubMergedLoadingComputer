"""
Cargo manager widget
货物装载管理
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QDialog, QFormLayout, QLineEdit,
                             QDoubleSpinBox, QDialogButtonBox)
from PyQt5.QtCore import Qt

from ..models import Cargo


class CargoDialog(QDialog):
    """Dialog for adding/editing cargo"""
    
    def __init__(self, cargo: Cargo = None, parent=None):
        super().__init__(parent)
        self.cargo = cargo
        self.init_ui()
        
        if cargo:
            self.load_cargo()
    
    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("货物编辑 / Cargo Editor")
        layout = QFormLayout(self)
        
        self.name_edit = QLineEdit()
        
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(0, 100000)
        self.weight_spin.setDecimals(2)
        self.weight_spin.setSuffix(" t")
        
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
        
        layout.addRow("名称 Name:", self.name_edit)
        layout.addRow("重量 Weight:", self.weight_spin)
        layout.addRow("纵向重心 LCG:", self.lcg_spin)
        layout.addRow("横向重心 TCG:", self.tcg_spin)
        layout.addRow("垂向重心 VCG:", self.vcg_spin)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
    
    def load_cargo(self):
        """Load cargo data into form"""
        self.name_edit.setText(self.cargo.name)
        self.weight_spin.setValue(self.cargo.weight)
        self.lcg_spin.setValue(self.cargo.lcg)
        self.tcg_spin.setValue(self.cargo.tcg)
        self.vcg_spin.setValue(self.cargo.vcg)
    
    def get_cargo(self) -> Cargo:
        """Get cargo from form data"""
        return Cargo(
            name=self.name_edit.text(),
            weight=self.weight_spin.value(),
            lcg=self.lcg_spin.value(),
            tcg=self.tcg_spin.value(),
            vcg=self.vcg_spin.value()
        )


class CargoManagerWidget(QWidget):
    """
    货物装载管理 / Cargo Loading Manager
    """
    
    def __init__(self):
        super().__init__()
        self.cargos = []
        self.init_ui()
        self.add_sample_cargos()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        group = QGroupBox("货物装载 / Cargo Loading")
        group_layout = QVBoxLayout()
        
        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("添加 Add")
        add_btn.clicked.connect(self.add_cargo)
        edit_btn = QPushButton("编辑 Edit")
        edit_btn.clicked.connect(self.edit_cargo)
        delete_btn = QPushButton("删除 Delete")
        delete_btn.clicked.connect(self.delete_cargo)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        
        group_layout.addLayout(button_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "名称 Name", "重量 Weight(t)", "LCG(m)", "TCG(m)", "VCG(m)"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        group_layout.addWidget(self.table)
        
        group.setLayout(group_layout)
        layout.addWidget(group)
    
    def add_sample_cargos(self):
        """Add sample cargos"""
        samples = [
            Cargo("Heavy Equipment #1", 2000, 0, 0, 12),
            Cargo("Container Stack", 500, 40, 0, 10),
        ]
        
        for cargo in samples:
            self.cargos.append(cargo)
        
        self.update_table()
    
    def update_table(self):
        """Update table display"""
        self.table.setRowCount(len(self.cargos))
        
        for i, cargo in enumerate(self.cargos):
            self.table.setItem(i, 0, QTableWidgetItem(cargo.name))
            self.table.setItem(i, 1, QTableWidgetItem(f"{cargo.weight:.2f}"))
            self.table.setItem(i, 2, QTableWidgetItem(f"{cargo.lcg:.2f}"))
            self.table.setItem(i, 3, QTableWidgetItem(f"{cargo.tcg:.2f}"))
            self.table.setItem(i, 4, QTableWidgetItem(f"{cargo.vcg:.2f}"))
    
    def add_cargo(self):
        """Add new cargo"""
        dialog = CargoDialog(parent=self)
        if dialog.exec_() == QDialog.Accepted:
            self.cargos.append(dialog.get_cargo())
            self.update_table()
    
    def edit_cargo(self):
        """Edit selected cargo"""
        row = self.table.currentRow()
        if row >= 0:
            dialog = CargoDialog(self.cargos[row], parent=self)
            if dialog.exec_() == QDialog.Accepted:
                self.cargos[row] = dialog.get_cargo()
                self.update_table()
    
    def delete_cargo(self):
        """Delete selected cargo"""
        row = self.table.currentRow()
        if row >= 0:
            del self.cargos[row]
            self.update_table()
    
    def get_cargos(self):
        """Get all cargos"""
        return self.cargos.copy()
