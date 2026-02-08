"""
Form 1 Widget - FORM 0格式
显示所有舱室的完整装载表格
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QLabel, QGroupBox, QPushButton,
                             QHeaderView, QComboBox, QDoubleSpinBox, QLineEdit)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from ship_data.tank_definitions import ALL_TANKS
from ship_data.loading_conditions import LOADING_CONDITIONS


class Form1Widget(QWidget):
    """Form 1 - 装载数据输入（FORM 0格式）"""

    data_changed = pyqtSignal()
    calculate_clicked = pyqtSignal()  # 计算按钮信号

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.populate_all_tanks()
        # 加载默认工况（LC01）
        self.load_default_condition('LC01')
        self.condition_combo.setCurrentIndex(1)  # 设置下拉菜单为LC01（索引1）
        
    def init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # 顶部：标题和工况选择
        top_layout = QHBoxLayout()
        top_layout.setSpacing(15)

        # FORM 0标签
        form_label = QLabel("FORM 0 - Loading Condition")
        form_label.setFont(QFont("Arial", 18, QFont.Bold))
        top_layout.addWidget(form_label)

        top_layout.addStretch()

        # 工况选择
        top_layout.addWidget(QLabel("工况:"))
        self.condition_combo = QComboBox()
        self.condition_combo.setMinimumWidth(400)
        self.condition_combo.setFont(QFont("Arial", 10))

        # 从loading_conditions.py加载所有13个工况
        from ship_data.loading_conditions import LOADING_CONDITIONS
        self.condition_ids = sorted(LOADING_CONDITIONS.keys())
        condition_names = []
        for cid in self.condition_ids:
            name = LOADING_CONDITIONS[cid]['name']
            if name.startswith(cid):
                condition_names.append(name)
            else:
                condition_names.append(f"{cid}: {name}")

        self.condition_combo.addItems(condition_names)
        self.condition_combo.currentIndexChanged.connect(self.on_condition_changed)
        top_layout.addWidget(self.condition_combo)

        layout.addLayout(top_layout)

        # 空船参数
        layout.addWidget(self.create_lightweight_group())

        # 装载表格
        layout.addWidget(self.create_loading_table(), 1)  # 给表格更多空间

        # 货物输入
        layout.addWidget(self.create_cargo_group())

        # 汇总信息
        layout.addWidget(self.create_summary_group())

        # 按钮
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        button_layout.addStretch()

        self.calc_button = QPushButton("计算")
        self.calc_button.setMinimumSize(120, 45)
        self.calc_button.setFont(QFont("Arial", 11, QFont.Bold))
        self.calc_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; border-radius: 5px; }")
        self.calc_button.clicked.connect(self.on_calculate)
        button_layout.addWidget(self.calc_button)

        self.clear_button = QPushButton("清空")
        self.clear_button.setMinimumSize(120, 45)
        self.clear_button.setFont(QFont("Arial", 11))
        self.clear_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; border-radius: 5px; }")
        self.clear_button.clicked.connect(self.clear_all)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)
        
    def create_lightweight_group(self):
        """创建空船参数组"""
        from PyQt5.QtWidgets import QGridLayout

        group = QGroupBox("Lightweight (空船重量)")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # 第一行
        layout.addWidget(QLabel("Weight:"), 0, 0)
        self.lw_weight = QDoubleSpinBox()
        self.lw_weight.setRange(0, 50000)
        self.lw_weight.setValue(20871.4)
        self.lw_weight.setDecimals(1)
        self.lw_weight.setSuffix(" t")
        self.lw_weight.setMinimumWidth(120)
        layout.addWidget(self.lw_weight, 0, 1)

        layout.addWidget(QLabel("LCG:"), 0, 2)
        self.lw_lcg = QDoubleSpinBox()
        self.lw_lcg.setRange(0, 250)
        self.lw_lcg.setValue(113.44)
        self.lw_lcg.setDecimals(2)
        self.lw_lcg.setSuffix(" m")
        self.lw_lcg.setMinimumWidth(120)
        layout.addWidget(self.lw_lcg, 0, 3)

        layout.addWidget(QLabel("TCG:"), 0, 4)
        self.lw_tcg = QDoubleSpinBox()
        self.lw_tcg.setRange(-50, 50)
        self.lw_tcg.setValue(-0.01)
        self.lw_tcg.setDecimals(2)
        self.lw_tcg.setSuffix(" m")
        self.lw_tcg.setMinimumWidth(120)
        layout.addWidget(self.lw_tcg, 0, 5)

        layout.addWidget(QLabel("VCG:"), 0, 6)
        self.lw_vcg = QDoubleSpinBox()
        self.lw_vcg.setRange(0, 50)
        self.lw_vcg.setValue(10.44)
        self.lw_vcg.setDecimals(2)
        self.lw_vcg.setSuffix(" m")
        self.lw_vcg.setMinimumWidth(120)
        layout.addWidget(self.lw_vcg, 0, 7)

        layout.setColumnStretch(8, 1)  # 最后一列拉伸

        group.setLayout(layout)
        return group

    def create_cargo_group(self):
        """创建货物输入组"""
        group = QGroupBox("Cargo (货物)")
        layout = QVBoxLayout()

        # 货物表格
        self.cargo_table = QTableWidget()
        self.cargo_table.setColumnCount(7)
        self.cargo_table.setHorizontalHeaderLabels([
            "Description", "Weight\n[t]", "LCG\n[m]", "TCG\n[m]",
            "VCG\n[m]", "FSM\n[t·m]", "操作"
        ])
        self.cargo_table.setMaximumHeight(150)
        self.cargo_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 6):
            self.cargo_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.cargo_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.cargo_table.cellChanged.connect(self.on_cargo_table_changed)
        layout.addWidget(self.cargo_table)

        # 添加货物按钮
        button_layout = QHBoxLayout()
        add_cargo_btn = QPushButton("+ 添加货物")
        add_cargo_btn.clicked.connect(self.add_cargo_row)
        button_layout.addWidget(add_cargo_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        group.setLayout(layout)
        return group

    def create_loading_table(self):
        """创建装载表格 - FORM 0格式"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ITEMS", "Volume\n[m³]", "Density\n[t/m³]", 
            "Weight\n[t]", "LCG\n[m]", "L.mom\n[t*m]", 
            "VCG\n[m]", "V.mom\n[t*m]", "FSM\n[t*m]"
        ])
        
        # 设置列宽
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 9):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        # 设置字体
        self.table.setFont(QFont("Arial", 9))
        
        # 连接单元格变化信号
        self.table.cellChanged.connect(self.on_cell_changed)
        
        layout.addWidget(self.table)
        
        return widget
        
    def create_summary_group(self):
        """创建汇总信息组"""
        from PyQt5.QtWidgets import QGridLayout

        group = QGroupBox("Summary (汇总信息)")
        group.setFont(QFont("Arial", 10, QFont.Bold))
        layout = QGridLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Deadweight行
        dw_label = QLabel("Deadweight:")
        dw_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(dw_label, 0, 0)

        self.dw_summary = QLabel("0.0 t")
        self.dw_summary.setFont(QFont("Arial", 11, QFont.Bold))
        self.dw_summary.setStyleSheet("QLabel { color: #2196F3; }")
        layout.addWidget(self.dw_summary, 0, 1)

        layout.addWidget(QLabel("LCG:"), 0, 2)
        self.dw_lcg_summary = QLabel("0.00 m")
        self.dw_lcg_summary.setFont(QFont("Arial", 10))
        layout.addWidget(self.dw_lcg_summary, 0, 3)

        layout.addWidget(QLabel("VCG:"), 0, 4)
        self.dw_vcg_summary = QLabel("0.00 m")
        self.dw_vcg_summary.setFont(QFont("Arial", 10))
        layout.addWidget(self.dw_vcg_summary, 0, 5)

        # Displacement行
        disp_label = QLabel("Displacement:")
        disp_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(disp_label, 1, 0)

        self.disp_summary = QLabel("20871.4 t")
        self.disp_summary.setFont(QFont("Arial", 11, QFont.Bold))
        self.disp_summary.setStyleSheet("QLabel { color: #4CAF50; }")
        layout.addWidget(self.disp_summary, 1, 1)

        layout.addWidget(QLabel("LCG:"), 1, 2)
        self.disp_lcg_summary = QLabel("113.44 m")
        self.disp_lcg_summary.setFont(QFont("Arial", 10))
        layout.addWidget(self.disp_lcg_summary, 1, 3)

        layout.addWidget(QLabel("VCG:"), 1, 4)
        self.disp_vcg_summary = QLabel("10.44 m")
        self.disp_vcg_summary.setFont(QFont("Arial", 10))
        layout.addWidget(self.disp_vcg_summary, 1, 5)

        layout.addWidget(QLabel("FSM:"), 1, 6)
        self.fsm_summary = QLabel("0.0 t*m")
        self.fsm_summary.setFont(QFont("Arial", 10))
        layout.addWidget(self.fsm_summary, 1, 7)

        layout.setColumnStretch(8, 1)

        group.setLayout(layout)
        return group

    def populate_all_tanks(self):
        """填充所有舱室到表格 - 按类别分组"""
        self.table.blockSignals(True)

        # 从tank_definitions获取所有舱室并按类别分组
        from ship_data.tank_definitions import get_tanks_by_category, TANK_CATEGORIES

        # 定义每个类别的密度
        category_densities = {
            'Heavy Fuel Oil': 0.991,
            'Diesel Oil': 0.900,
            'Lubricating Oil': 0.900,
            'Technical Water': 1.000,
            'Fresh Water': 1.000,
            'Ballast Water': 1.025,
            'Fixed FW ballast': 1.000,
            'Gray Water': 1.000,
            'Bilge Water': 1.000,
            'Sludge': 2.380
        }

        row = 0

        # 遍历每个类别
        for category_name in TANK_CATEGORIES:
            # 获取该类别的所有舱室
            category_tanks = get_tanks_by_category(category_name)
            if not category_tanks:
                continue

            density = category_densities.get(category_name, 1.000)
            # 添加类别标题行
            self.table.insertRow(row)
            category_item = QTableWidgetItem(f"{category_name} density={density:.3f} t/m3")
            category_item.setFont(QFont("Arial", 10, QFont.Bold))
            category_item.setBackground(QColor(200, 200, 200))
            self.table.setItem(row, 0, category_item)

            # 合并类别标题行的所有列
            for col in range(1, 9):
                self.table.setItem(row, col, QTableWidgetItem(""))
                self.table.item(row, col).setBackground(QColor(200, 200, 200))

            row += 1

            # 添加该类别的所有舱室（按tank_id排序）
            for tank_id in sorted(category_tanks.keys()):
                tank_info = category_tanks[tank_id]
                self.table.insertRow(row)

                # ITEMS (舱室名称)
                name_item = QTableWidgetItem(f"{tank_id}: {tank_info['name']}")
                self.table.setItem(row, 0, name_item)

                # Volume
                volume = tank_info.get('max_volume', tank_info.get('volume', 0))
                vol_item = QTableWidgetItem(f"{volume:.1f}")
                vol_item.setFlags(vol_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 1, vol_item)

                # Density
                dens_item = QTableWidgetItem(f"{density:.3f}")
                dens_item.setFlags(dens_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 2, dens_item)

                # Weight (可编辑)
                weight_item = QTableWidgetItem("0.0")
                self.table.setItem(row, 3, weight_item)

                # LCG
                lcg_item = QTableWidgetItem(f"{tank_info['lcg']:.2f}")
                lcg_item.setFlags(lcg_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 4, lcg_item)

                # L.mom (计算)
                lmom_item = QTableWidgetItem("0.0")
                lmom_item.setFlags(lmom_item.flags() & ~Qt.ItemIsEditable)
                lmom_item.setForeground(QColor(0, 0, 255))
                self.table.setItem(row, 5, lmom_item)

                # VCG
                vcg_item = QTableWidgetItem(f"{tank_info['vcg']:.2f}")
                vcg_item.setFlags(vcg_item.flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 6, vcg_item)

                # V.mom (计算)
                vmom_item = QTableWidgetItem("0.0")
                vmom_item.setFlags(vmom_item.flags() & ~Qt.ItemIsEditable)
                vmom_item.setForeground(QColor(0, 0, 255))
                self.table.setItem(row, 7, vmom_item)

                # FSM (计算)
                fsm_item = QTableWidgetItem("0.0")
                fsm_item.setFlags(fsm_item.flags() & ~Qt.ItemIsEditable)
                fsm_item.setForeground(QColor(0, 0, 255))
                self.table.setItem(row, 8, fsm_item)

                row += 1

            # 添加类别小计行
            self.table.insertRow(row)
            total_item = QTableWidgetItem(f"Total of {category_name}")
            total_item.setFont(QFont("Arial", 9, QFont.Bold))
            total_item.setBackground(QColor(220, 220, 220))
            self.table.setItem(row, 0, total_item)

            for col in range(1, 9):
                item = QTableWidgetItem("0.0")
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                item.setFont(QFont("Arial", 9, QFont.Bold))
                item.setBackground(QColor(220, 220, 220))
                self.table.setItem(row, col, item)

            row += 1

        # 添加汇总行
        self.add_summary_rows(row)

        self.table.blockSignals(False)

    def add_summary_rows(self, start_row):
        """添加汇总行"""
        row = start_row

        # 添加Deadweight总计行
        self.table.insertRow(row)
        dw_item = QTableWidgetItem("Deadweight")
        dw_item.setFont(QFont("Arial", 10, QFont.Bold))
        dw_item.setBackground(QColor(255, 255, 200))
        self.table.setItem(row, 0, dw_item)
        for col in range(1, 9):
            item = QTableWidgetItem("0.0")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setFont(QFont("Arial", 10, QFont.Bold))
            item.setBackground(QColor(255, 255, 200))
            self.table.setItem(row, col, item)
        row += 1

        # Lightweight
        self.table.insertRow(row)
        lw_item = QTableWidgetItem("Lightweight")
        lw_item.setFont(QFont("Arial", 10, QFont.Bold))
        lw_item.setBackground(QColor(200, 255, 200))
        self.table.setItem(row, 0, lw_item)
        self.table.setItem(row, 1, QTableWidgetItem(""))
        self.table.setItem(row, 2, QTableWidgetItem(""))
        self.table.setItem(row, 3, QTableWidgetItem("20871.4"))
        self.table.setItem(row, 4, QTableWidgetItem("113.44"))
        self.table.setItem(row, 5, QTableWidgetItem("2367729.0"))
        self.table.setItem(row, 6, QTableWidgetItem("10.44"))
        self.table.setItem(row, 7, QTableWidgetItem("217897.4"))
        self.table.setItem(row, 8, QTableWidgetItem("0.0"))
        for col in range(1, 9):
            self.table.item(row, col).setFlags(self.table.item(row, col).flags() & ~Qt.ItemIsEditable)
            self.table.item(row, col).setBackground(QColor(200, 255, 200))
        row += 1

        # Displacement
        self.table.insertRow(row)
        disp_item = QTableWidgetItem("Displacement (1.025 t/m3)")
        disp_item.setFont(QFont("Arial", 10, QFont.Bold))
        disp_item.setBackground(QColor(255, 200, 200))
        self.table.setItem(row, 0, disp_item)
        for col in range(1, 9):
            item = QTableWidgetItem("0.0")
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item.setFont(QFont("Arial", 10, QFont.Bold))
            item.setBackground(QColor(255, 200, 200))
            self.table.setItem(row, col, item)

    def on_cell_changed(self, row, col):
        """单元格变化时重新计算"""
        if col == 3:  # Weight列变化
            self.calculate_row(row)
            self.update_category_totals()
            self.update_summary()

    def calculate_row(self, row):
        """计算单行的力矩和FSM"""
        try:
            weight_item = self.table.item(row, 3)
            if not weight_item:
                return

            weight = float(weight_item.text())

            # 获取LCG和VCG
            lcg_item = self.table.item(row, 4)
            vcg_item = self.table.item(row, 6)

            if lcg_item and vcg_item:
                lcg = float(lcg_item.text())
                vcg = float(vcg_item.text())

                # 计算力矩
                l_mom = weight * lcg
                v_mom = weight * vcg

                # 更新L.mom和V.mom
                self.table.item(row, 5).setText(f"{l_mom:.1f}")
                self.table.item(row, 7).setText(f"{v_mom:.1f}")

                # 计算FSM（如果有）
                # 这里需要根据舱室ID和装载百分比计算
                # 暂时设为0
                self.table.item(row, 8).setText("0.0")
        except:
            pass

    def update_category_totals(self):
        """更新各类别的小计"""
        # 遍历所有行，找到Total行并更新
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text().startswith("Total of"):
                # 向上查找该类别的所有舱室
                category_start = row - 1
                while category_start >= 0:
                    prev_item = self.table.item(category_start, 0)
                    if prev_item and (prev_item.font().bold() and not prev_item.text().startswith("Total")):
                        break
                    category_start -= 1

                # 计算该类别的总和
                total_weight = 0
                total_lmom = 0
                total_vmom = 0
                total_fsm = 0

                for r in range(category_start + 1, row):
                    try:
                        weight = float(self.table.item(r, 3).text())
                        lmom = float(self.table.item(r, 5).text())
                        vmom = float(self.table.item(r, 7).text())
                        fsm = float(self.table.item(r, 8).text())

                        total_weight += weight
                        total_lmom += lmom
                        total_vmom += vmom
                        total_fsm += fsm
                    except:
                        pass

                # 更新Total行
                self.table.item(row, 3).setText(f"{total_weight:.1f}")
                self.table.item(row, 5).setText(f"{total_lmom:.1f}")
                self.table.item(row, 7).setText(f"{total_vmom:.1f}")
                self.table.item(row, 8).setText(f"{total_fsm:.1f}")

                # 计算平均LCG和VCG
                if total_weight > 0:
                    avg_lcg = total_lmom / total_weight
                    avg_vcg = total_vmom / total_weight
                    self.table.item(row, 4).setText(f"{avg_lcg:.2f}")
                    self.table.item(row, 6).setText(f"{avg_vcg:.2f}")

    def update_summary(self):
        """更新汇总信息"""
        # 查找Deadweight行
        dw_row = -1
        lw_row = -1
        disp_row = -1

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item:
                if item.text() == "Deadweight":
                    dw_row = row
                elif item.text() == "Lightweight":
                    lw_row = row
                elif item.text() == "Displacement (1.025 t/m3)":
                    disp_row = row

        if dw_row < 0 or lw_row < 0 or disp_row < 0:
            return

        # 计算Deadweight（所有Total行的总和 + Stores + Crew + Miscellaneous）
        total_dw_weight = 0
        total_dw_lmom = 0
        total_dw_vmom = 0
        total_dw_fsm = 0

        for row in range(dw_row):
            item = self.table.item(row, 0)
            if item and item.text().startswith("Total of"):
                try:
                    weight = float(self.table.item(row, 3).text())
                    lmom = float(self.table.item(row, 5).text())
                    vmom = float(self.table.item(row, 7).text())
                    fsm = float(self.table.item(row, 8).text())

                    total_dw_weight += weight
                    total_dw_lmom += lmom
                    total_dw_vmom += vmom
                    total_dw_fsm += fsm
                except:
                    pass

        # 添加所有货物到Deadweight
        for row in range(self.cargo_table.rowCount()):
            try:
                weight = float(self.cargo_table.item(row, 1).text())
                if weight > 0:
                    lcg = float(self.cargo_table.item(row, 2).text())
                    vcg = float(self.cargo_table.item(row, 4).text())
                    fsm = float(self.cargo_table.item(row, 5).text())

                    total_dw_weight += weight
                    total_dw_lmom += weight * lcg
                    total_dw_vmom += weight * vcg
                    total_dw_fsm += fsm
            except:
                pass

        # 更新Deadweight行
        self.table.item(dw_row, 3).setText(f"{total_dw_weight:.1f}")
        self.table.item(dw_row, 5).setText(f"{total_dw_lmom:.1f}")
        self.table.item(dw_row, 7).setText(f"{total_dw_vmom:.1f}")
        self.table.item(dw_row, 8).setText(f"{total_dw_fsm:.1f}")

        if total_dw_weight > 0:
            dw_lcg = total_dw_lmom / total_dw_weight
            dw_vcg = total_dw_vmom / total_dw_weight
            self.table.item(dw_row, 4).setText(f"{dw_lcg:.2f}")
            self.table.item(dw_row, 6).setText(f"{dw_vcg:.2f}")

        # 获取Lightweight
        lw_weight = float(self.table.item(lw_row, 3).text())
        lw_lmom = float(self.table.item(lw_row, 5).text())
        lw_vmom = float(self.table.item(lw_row, 7).text())

        # 计算Displacement
        disp_weight = total_dw_weight + lw_weight
        disp_lmom = total_dw_lmom + lw_lmom
        disp_vmom = total_dw_vmom + lw_vmom
        disp_fsm = total_dw_fsm

        self.table.item(disp_row, 3).setText(f"{disp_weight:.1f}")
        self.table.item(disp_row, 5).setText(f"{disp_lmom:.1f}")
        self.table.item(disp_row, 7).setText(f"{disp_vmom:.1f}")
        self.table.item(disp_row, 8).setText(f"{disp_fsm:.1f}")

        if disp_weight > 0:
            disp_lcg = disp_lmom / disp_weight
            disp_vcg = disp_vmom / disp_weight
            self.table.item(disp_row, 4).setText(f"{disp_lcg:.2f}")
            self.table.item(disp_row, 6).setText(f"{disp_vcg:.2f}")

        # 更新顶部汇总标签
        self.dw_summary.setText(f"{total_dw_weight:.1f} t")
        if total_dw_weight > 0:
            self.dw_lcg_summary.setText(f"{dw_lcg:.2f} m")
            self.dw_vcg_summary.setText(f"{dw_vcg:.2f} m")

        self.disp_summary.setText(f"{disp_weight:.1f} t")
        if disp_weight > 0:
            self.disp_lcg_summary.setText(f"{disp_lcg:.2f} m")
            self.disp_vcg_summary.setText(f"{disp_vcg:.2f} m")
        self.fsm_summary.setText(f"{disp_fsm:.1f} t*m")

        # 发射数据变化信号
        self.data_changed.emit()

    def add_cargo_row(self):
        """添加货物行"""
        row = self.cargo_table.rowCount()
        self.cargo_table.insertRow(row)

        # Description (可编辑)
        self.cargo_table.setItem(row, 0, QTableWidgetItem("Cargo"))

        # Weight (可编辑)
        self.cargo_table.setItem(row, 1, QTableWidgetItem("0.0"))

        # LCG (可编辑)
        self.cargo_table.setItem(row, 2, QTableWidgetItem("0.0"))

        # TCG (可编辑)
        self.cargo_table.setItem(row, 3, QTableWidgetItem("0.0"))

        # VCG (可编辑)
        self.cargo_table.setItem(row, 4, QTableWidgetItem("0.0"))

        # FSM (可编辑)
        self.cargo_table.setItem(row, 5, QTableWidgetItem("0.0"))

        # 删除按钮
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(lambda: self.delete_cargo_row(row))
        self.cargo_table.setCellWidget(row, 6, delete_btn)

    def delete_cargo_row(self, row):
        """删除货物行"""
        self.cargo_table.blockSignals(True)
        self.cargo_table.removeRow(row)
        self.cargo_table.blockSignals(False)

        # 更新所有删除按钮的行号
        for r in range(self.cargo_table.rowCount()):
            delete_btn = QPushButton("删除")
            delete_btn.clicked.connect(lambda checked, row=r: self.delete_cargo_row(row))
            self.cargo_table.setCellWidget(r, 6, delete_btn)

        self.update_summary()

    def on_cargo_table_changed(self, row, col):
        """货物表格数据变化"""
        if col < 6:  # 不是操作列
            self.update_summary()

    def clear_cargo_table(self):
        """清空货物表格"""
        self.cargo_table.blockSignals(True)
        self.cargo_table.setRowCount(0)
        self.cargo_table.blockSignals(False)

    def on_condition_changed(self, index):
        """工况选择变化"""
        if 0 <= index < len(self.condition_ids):
            condition_id = self.condition_ids[index]
            self.load_default_condition(condition_id)

    def load_default_condition(self, condition_id):
        """加载默认工况"""
        if condition_id not in LOADING_CONDITIONS:
            return

        condition = LOADING_CONDITIONS[condition_id]

        # 清空所有舱室的装载
        self.table.blockSignals(True)

        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and ':' in item.text():  # 舱室行
                self.table.item(row, 3).setText("0.0")

        # 设置工况中的装载
        for tank_id, data in condition['tanks'].items():
            # 查找该舱室的行
            for row in range(self.table.rowCount()):
                item = self.table.item(row, 0)
                if item and item.text().startswith(tank_id + ":"):
                    weight = data.get('weight', 0)
                    self.table.item(row, 3).setText(f"{weight:.1f}")
                    break

        self.table.blockSignals(False)

        # 清空货物表格
        self.clear_cargo_table()

        # 加载货物数据（如果有）
        if 'cargo' in condition:
            cargo_list = condition['cargo']
            # 兼容旧格式（单个货物字典）和新格式（货物列表）
            if isinstance(cargo_list, dict):
                cargo_list = [cargo_list]

            self.cargo_table.blockSignals(True)
            for cargo in cargo_list:
                row = self.cargo_table.rowCount()
                self.cargo_table.insertRow(row)

                self.cargo_table.setItem(row, 0, QTableWidgetItem(cargo.get('description', '')))
                self.cargo_table.setItem(row, 1, QTableWidgetItem(str(cargo.get('weight', 0.0))))
                self.cargo_table.setItem(row, 2, QTableWidgetItem(str(cargo.get('lcg', 0.0))))
                self.cargo_table.setItem(row, 3, QTableWidgetItem(str(cargo.get('tcg', 0.0))))
                self.cargo_table.setItem(row, 4, QTableWidgetItem(str(cargo.get('vcg', 0.0))))
                self.cargo_table.setItem(row, 5, QTableWidgetItem(str(cargo.get('fsm', 0.0))))

                # 添加删除按钮
                delete_btn = QPushButton("删除")
                delete_btn.clicked.connect(lambda checked, r=row: self.delete_cargo_row(r))
                self.cargo_table.setCellWidget(row, 6, delete_btn)

            self.cargo_table.blockSignals(False)

        # 重新计算所有行
        for row in range(self.table.rowCount()):
            self.calculate_row(row)

        self.update_category_totals()
        self.update_summary()

    def get_loading_data(self):
        """获取装载数据"""
        # 查找Displacement行
        disp_row = -1
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and item.text() == "Displacement (1.025 t/m3)":
                disp_row = row
                break

        if disp_row < 0:
            return None

        # 获取总排水量数据
        displacement = float(self.table.item(disp_row, 3).text())
        lcg = float(self.table.item(disp_row, 4).text())
        vcg = float(self.table.item(disp_row, 6).text())
        fsm = float(self.table.item(disp_row, 8).text())

        # 获取所有装载的舱室
        items = []
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and ':' in item.text():  # 舱室行
                try:
                    weight = float(self.table.item(row, 3).text())
                    if weight > 0:
                        tank_id = item.text().split(':')[0].strip()
                        items.append({
                            'tank_id': tank_id,
                            'name': item.text(),
                            'weight': weight,
                            'lcg': float(self.table.item(row, 4).text()),
                            'vcg': float(self.table.item(row, 6).text()),
                            'fsm': float(self.table.item(row, 8).text())
                        })
                except:
                    pass

        # 添加所有货物
        for row in range(self.cargo_table.rowCount()):
            try:
                weight = float(self.cargo_table.item(row, 1).text())
                if weight > 0:
                    items.append({
                        'tank_id': 'CARGO',
                        'name': f'Cargo: {self.cargo_table.item(row, 0).text()}',
                        'weight': weight,
                        'lcg': float(self.cargo_table.item(row, 2).text()),
                        'tcg': float(self.cargo_table.item(row, 3).text()),
                        'vcg': float(self.cargo_table.item(row, 4).text()),
                        'fsm': float(self.cargo_table.item(row, 5).text())
                    })
            except:
                pass

        return {
            'condition_name': self.condition_combo.currentText(),
            'lightweight': self.lw_weight.value(),
            'lw_lcg': self.lw_lcg.value(),
            'lw_vcg': self.lw_vcg.value(),
            'deadweight': float(self.dw_summary.text().replace(' t', '')),
            'displacement': displacement,
            'lcg': lcg,
            'vcg': vcg,
            'fsm': fsm,
            'items': items
        }

    def on_calculate(self):
        """计算按钮点击"""
        self.calculate_clicked.emit()

    def clear_all(self):
        """清空所有装载数据"""
        self.table.blockSignals(True)

        # 清空所有舱室的重量
        for row in range(self.table.rowCount()):
            item = self.table.item(row, 0)
            if item and ':' in item.text():  # 舱室行
                self.table.item(row, 3).setText("0.0")

        self.table.blockSignals(False)

        # 重新计算
        for row in range(self.table.rowCount()):
            self.calculate_row(row)

        self.update_category_totals()
        self.update_summary()

