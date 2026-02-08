"""
Main window for semi-submersible ship loading computer
半潜船装载计算软件主窗口
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QLabel, QPushButton, QTableWidget,
                             QTableWidgetItem, QHeaderView, QGroupBox, QFormLayout,
                             QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from ..models import LoadingCondition, ShipParameters, CompartmentType
from ..calculations import FlotationCalculator, StabilityCalculator, StrengthCalculator
from ..data import get_sample_hydrostatic_table
from .loading_editor import LoadingEditorWidget
from .compartment_manager import CompartmentManagerWidget
from .cargo_manager import CargoManagerWidget


class MainWindow(QMainWindow):
    """
    主窗口 / Main Window
    """
    
    def __init__(self):
        super().__init__()
        self.init_data()
        self.init_ui()
    
    def init_data(self):
        """Initialize data and calculators"""
        # Ship parameters for sample semi-submersible
        self.ship_params = ShipParameters(
            loa=190.0,
            lpp=180.0,
            breadth=40.0,
            depth=18.0,
            lightship_weight=12000.0,
            lightship_lcg=0.0,
            lightship_tcg=0.0,
            lightship_vcg=9.5,
            design_draft=10.0
        )
        
        # Loading condition
        self.loading_condition = LoadingCondition(
            name="Ballast Condition",
            description="Initial ballast loading condition",
            ship_params=self.ship_params
        )
        
        # Initialize calculators
        hydrostatic_table = get_sample_hydrostatic_table()
        self.flotation_calc = FlotationCalculator(hydrostatic_table)
        self.stability_calc = StabilityCalculator()
        self.strength_calc = StrengthCalculator(lpp=self.ship_params.lpp)
        
        # Results
        self.flotation_results = None
        self.stability_results = None
        self.strength_results = None
    
    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("半潜船装载计算软件 / Semi-Submersible Ship Loading Computer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("半潜船装载计算软件\nSemi-Submersible Ship Loading Computer")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_input_tab()
        self.create_results_tab()
        self.create_stability_tab()
        self.create_strength_tab()
        
        # Calculate button
        calc_button = QPushButton("计算 / Calculate")
        calc_button.setMinimumHeight(40)
        calc_button.clicked.connect(self.calculate_all)
        main_layout.addWidget(calc_button)
    
    def create_input_tab(self):
        """Create input tab with loading condition editor"""
        input_widget = QWidget()
        layout = QVBoxLayout(input_widget)
        
        # Loading condition editor
        self.loading_editor = LoadingEditorWidget(self.ship_params)
        layout.addWidget(self.loading_editor)
        
        # Compartment manager
        self.compartment_manager = CompartmentManagerWidget()
        layout.addWidget(self.compartment_manager)
        
        # Cargo manager
        self.cargo_manager = CargoManagerWidget()
        layout.addWidget(self.cargo_manager)
        
        self.tab_widget.addTab(input_widget, "装载输入 / Loading Input")
    
    def create_results_tab(self):
        """Create results tab with flotation results"""
        results_widget = QWidget()
        layout = QVBoxLayout(results_widget)
        
        # Results group
        results_group = QGroupBox("浮态计算结果 / Flotation Calculation Results")
        results_layout = QFormLayout()
        
        self.disp_label = QLabel("--")
        self.mean_draft_label = QLabel("--")
        self.fwd_draft_label = QLabel("--")
        self.aft_draft_label = QLabel("--")
        self.trim_label = QLabel("--")
        self.trim_angle_label = QLabel("--")
        self.lcg_label = QLabel("--")
        self.vcg_label = QLabel("--")
        self.gmt_label = QLabel("--")
        
        results_layout.addRow("排水量 Displacement (t):", self.disp_label)
        results_layout.addRow("平均吃水 Mean Draft (m):", self.mean_draft_label)
        results_layout.addRow("首吃水 Forward Draft (m):", self.fwd_draft_label)
        results_layout.addRow("尾吃水 Aft Draft (m):", self.aft_draft_label)
        results_layout.addRow("纵倾值 Trim (m):", self.trim_label)
        results_layout.addRow("纵倾角 Trim Angle (deg):", self.trim_angle_label)
        results_layout.addRow("纵向重心 LCG (m):", self.lcg_label)
        results_layout.addRow("垂向重心 VCG (m):", self.vcg_label)
        results_layout.addRow("初稳性高 GMT (m):", self.gmt_label)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(results_widget, "浮态结果 / Flotation Results")
    
    def create_stability_tab(self):
        """Create stability tab with GZ curve and criteria"""
        stability_widget = QWidget()
        layout = QVBoxLayout(stability_widget)
        
        # GZ curve plot
        self.gz_figure = Figure(figsize=(10, 5))
        self.gz_canvas = FigureCanvas(self.gz_figure)
        layout.addWidget(self.gz_canvas)
        
        # Stability criteria table
        criteria_group = QGroupBox("稳性衡准检查 / Stability Criteria Check")
        criteria_layout = QVBoxLayout()
        
        self.criteria_table = QTableWidget()
        self.criteria_table.setColumnCount(4)
        self.criteria_table.setHorizontalHeaderLabels([
            "项目 Item", "实际值 Actual", "要求值 Required", "状态 Status"
        ])
        self.criteria_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        criteria_layout.addWidget(self.criteria_table)
        criteria_group.setLayout(criteria_layout)
        layout.addWidget(criteria_group)
        
        self.tab_widget.addTab(stability_widget, "稳性 / Stability")
    
    def create_strength_tab(self):
        """Create strength tab with shear force and bending moment curves"""
        strength_widget = QWidget()
        layout = QVBoxLayout(strength_widget)
        
        # Shear force plot
        self.sf_figure = Figure(figsize=(10, 4))
        self.sf_canvas = FigureCanvas(self.sf_figure)
        layout.addWidget(self.sf_canvas)
        
        # Bending moment plot
        self.bm_figure = Figure(figsize=(10, 4))
        self.bm_canvas = FigureCanvas(self.bm_figure)
        layout.addWidget(self.bm_canvas)
        
        self.tab_widget.addTab(strength_widget, "强度 / Strength")
    
    def calculate_all(self):
        """Perform all calculations"""
        try:
            # Get loading condition from editors
            self.loading_condition.compartments = self.compartment_manager.get_compartments()
            self.loading_condition.cargos = self.cargo_manager.get_cargos()
            
            # Flotation calculation
            mean_draft, trim, fwd_draft, aft_draft, hydro = self.flotation_calc.calculate_flotation(
                self.loading_condition,
                self.ship_params.lpp
            )
            
            trim_angle = self.flotation_calc.calculate_trim_angle(trim, self.ship_params.lpp)
            
            self.flotation_results = {
                'mean_draft': mean_draft,
                'trim': trim,
                'fwd_draft': fwd_draft,
                'aft_draft': aft_draft,
                'trim_angle': trim_angle,
                'hydro': hydro
            }
            
            # Update results display
            self.update_flotation_results()
            
            # Stability calculation
            heel_angles, gz_values, gmt_corrected, criteria = \
                self.stability_calc.calculate_stability_with_correction(
                    self.loading_condition,
                    hydro
                )
            
            self.stability_results = {
                'heel_angles': heel_angles,
                'gz_values': gz_values,
                'gmt_corrected': gmt_corrected,
                'criteria': criteria
            }
            
            # Update stability display
            self.update_stability_results()
            
            # Strength calculation
            stations, shear_force, bending_moment = \
                self.strength_calc.calculate_strength(self.loading_condition)
            
            self.strength_results = {
                'stations': stations,
                'shear_force': shear_force,
                'bending_moment': bending_moment
            }
            
            # Update strength display
            self.update_strength_results()
            
            QMessageBox.information(self, "计算完成 / Calculation Complete",
                                  "所有计算已完成！\nAll calculations completed!")
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误 / Calculation Error",
                               f"计算过程中发生错误：\nError during calculation:\n{str(e)}")
    
    def update_flotation_results(self):
        """Update flotation results display"""
        if not self.flotation_results:
            return
        
        r = self.flotation_results
        
        self.disp_label.setText(f"{self.loading_condition.total_weight:.2f}")
        self.mean_draft_label.setText(f"{r['mean_draft']:.3f}")
        self.fwd_draft_label.setText(f"{r['fwd_draft']:.3f}")
        self.aft_draft_label.setText(f"{r['aft_draft']:.3f}")
        self.trim_label.setText(f"{r['trim']:.3f}")
        self.trim_angle_label.setText(f"{r['trim_angle']:.4f}")
        self.lcg_label.setText(f"{self.loading_condition.lcg:.3f}")
        self.vcg_label.setText(f"{self.loading_condition.vcg:.3f}")
        self.gmt_label.setText(f"{r['hydro'].gmt:.3f}")
    
    def update_stability_results(self):
        """Update stability results display"""
        if not self.stability_results:
            return
        
        r = self.stability_results
        
        # Plot GZ curve
        self.gz_figure.clear()
        ax = self.gz_figure.add_subplot(111)
        ax.plot(r['heel_angles'], r['gz_values'], 'b-', linewidth=2)
        ax.grid(True)
        ax.set_xlabel('横倾角 Heel Angle (deg)')
        ax.set_ylabel('复原力臂 GZ (m)')
        ax.set_title('GZ曲线 / GZ Curve')
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        self.gz_canvas.draw()
        
        # Update criteria table
        criteria = r['criteria']
        self.criteria_table.setRowCount(len(criteria) - 1)  # Exclude 'Overall'
        
        row = 0
        for key, value in criteria.items():
            if key == 'Overall':
                continue
            
            self.criteria_table.setItem(row, 0, QTableWidgetItem(value['description']))
            
            if 'value' in value:
                if 'angle' in value:
                    val_text = f"{value['value']:.3f} @ {value['angle']:.1f}°"
                else:
                    val_text = f"{value['value']:.4f}"
                self.criteria_table.setItem(row, 1, QTableWidgetItem(val_text))
            else:
                self.criteria_table.setItem(row, 1, QTableWidgetItem("--"))
            
            if 'requirement' in value:
                self.criteria_table.setItem(row, 2, QTableWidgetItem(f"{value['requirement']:.3f}"))
            else:
                self.criteria_table.setItem(row, 2, QTableWidgetItem("--"))
            
            status = "✓ 满足 Pass" if value['passed'] else "✗ 不满足 Fail"
            status_item = QTableWidgetItem(status)
            if value['passed']:
                status_item.setForeground(Qt.darkGreen)
            else:
                status_item.setForeground(Qt.red)
            self.criteria_table.setItem(row, 3, status_item)
            
            row += 1
    
    def update_strength_results(self):
        """Update strength results display"""
        if not self.strength_results:
            return
        
        r = self.strength_results
        
        # Plot shear force
        self.sf_figure.clear()
        ax1 = self.sf_figure.add_subplot(111)
        ax1.plot(r['stations'], r['shear_force'], 'b-', linewidth=2)
        ax1.grid(True)
        ax1.set_xlabel('位置 Position (m from midship)')
        ax1.set_ylabel('剪力 Shear Force (t)')
        ax1.set_title('剪力曲线 / Shear Force Curve')
        ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax1.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
        self.sf_canvas.draw()
        
        # Plot bending moment
        self.bm_figure.clear()
        ax2 = self.bm_figure.add_subplot(111)
        ax2.plot(r['stations'], r['bending_moment'], 'r-', linewidth=2)
        ax2.grid(True)
        ax2.set_xlabel('位置 Position (m from midship)')
        ax2.set_ylabel('弯矩 Bending Moment (t·m)')
        ax2.set_title('弯矩曲线 / Bending Moment Curve')
        ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax2.axvline(x=0, color='k', linestyle='--', linewidth=0.5)
        self.bm_canvas.draw()
