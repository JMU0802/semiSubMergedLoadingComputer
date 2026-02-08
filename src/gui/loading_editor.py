"""
Loading condition editor widget
装载工况编辑器
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QGroupBox, QFormLayout)
from PyQt5.QtCore import Qt

from ..models import ShipParameters


class LoadingEditorWidget(QWidget):
    """
    装载工况编辑器 / Loading Condition Editor
    """
    
    def __init__(self, ship_params: ShipParameters):
        super().__init__()
        self.ship_params = ship_params
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        
        # Loading condition info group
        info_group = QGroupBox("工况信息 / Loading Condition Info")
        info_layout = QFormLayout()
        
        self.name_edit = QLineEdit("Ballast Condition")
        self.desc_edit = QTextEdit()
        self.desc_edit.setMaximumHeight(60)
        self.desc_edit.setPlainText("Initial ballast loading condition")
        
        info_layout.addRow("工况名称 Name:", self.name_edit)
        info_layout.addRow("描述 Description:", self.desc_edit)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Ship parameters group
        ship_group = QGroupBox("船舶参数 / Ship Parameters")
        ship_layout = QFormLayout()
        
        ship_layout.addRow("总长 LOA (m):", QLabel(f"{self.ship_params.loa:.2f}"))
        ship_layout.addRow("垂线间长 LPP (m):", QLabel(f"{self.ship_params.lpp:.2f}"))
        ship_layout.addRow("型宽 Breadth (m):", QLabel(f"{self.ship_params.breadth:.2f}"))
        ship_layout.addRow("型深 Depth (m):", QLabel(f"{self.ship_params.depth:.2f}"))
        ship_layout.addRow("空船重量 Lightship (t):", QLabel(f"{self.ship_params.lightship_weight:.2f}"))
        ship_layout.addRow("空船LCG (m):", QLabel(f"{self.ship_params.lightship_lcg:.2f}"))
        ship_layout.addRow("空船VCG (m):", QLabel(f"{self.ship_params.lightship_vcg:.2f}"))
        
        ship_group.setLayout(ship_layout)
        layout.addWidget(ship_group)
