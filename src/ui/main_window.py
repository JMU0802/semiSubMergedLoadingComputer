"""
主窗口 (Main Window)
装载计算软件的主界面
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTabWidget, QPushButton, QLabel, QStatusBar,
                             QMessageBox, QAction, QMenuBar, QToolBar)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.ui.loading_tab import LoadingTab
from src.ui.results_tab import ResultsTab
from src.core.calculation_engine import CalculationEngine
from ship_data.ship_particulars import SHIP_PARTICULARS


class MainWindow(QMainWindow):
    """主窗口"""
    
    def __init__(self):
        super().__init__()
        
        # 初始化计算引擎
        self.calc_engine = CalculationEngine()
        
        # 设置窗口
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        # 窗口基本设置
        self.setWindowTitle(f"半潜船装载计算软件 - {SHIP_PARTICULARS['ship_name']}")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 装载工况标签页
        self.loading_tab = LoadingTab(self.calc_engine)
        self.tab_widget.addTab(self.loading_tab, "装载工况")
        
        # 计算结果标签页
        self.results_tab = ResultsTab(self.calc_engine)
        self.tab_widget.addTab(self.results_tab, "计算结果")
        
        # 连接信号
        self.loading_tab.calculation_completed.connect(self.on_calculation_completed)
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
    
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件(&F)')
        
        new_action = QAction('新建工况(&N)', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_condition)
        file_menu.addAction(new_action)
        
        open_action = QAction('打开工况(&O)', self)
        open_action.setShortcut('Ctrl+O')
        file_menu.addAction(open_action)
        
        save_action = QAction('保存工况(&S)', self)
        save_action.setShortcut('Ctrl+S')
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('退出(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 计算菜单
        calc_menu = menubar.addMenu('计算(&C)')
        
        calc_action = QAction('执行计算(&R)', self)
        calc_action.setShortcut('F5')
        calc_action.triggered.connect(self.loading_tab.calculate)
        calc_menu.addAction(calc_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu('帮助(&H)')
        
        about_action = QAction('关于(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # 新建按钮
        new_btn = QPushButton("新建工况")
        new_btn.clicked.connect(self.new_condition)
        toolbar.addWidget(new_btn)
        
        toolbar.addSeparator()
        
        # 计算按钮
        calc_btn = QPushButton("执行计算")
        calc_btn.clicked.connect(self.loading_tab.calculate)
        toolbar.addWidget(calc_btn)
    
    def new_condition(self):
        """新建工况"""
        self.loading_tab.clear_all()
        self.status_bar.showMessage("已创建新工况")
    
    def on_calculation_completed(self, success):
        """计算完成回调"""
        if success:
            self.status_bar.showMessage("计算完成")
            self.results_tab.update_results()
            self.tab_widget.setCurrentWidget(self.results_tab)
        else:
            self.status_bar.showMessage("计算失败")
            QMessageBox.warning(self, "计算错误", "计算过程中出现错误，请检查输入数据")
    
    def show_about(self):
        """显示关于对话框"""
        about_text = """
        <h2>半潜船装载计算软件</h2>
        <p>版本: 1.0.0</p>
        <p>基于装载手册 G-8-1-装载手册(B3598.1174.102)</p>
        <br>
        <p><b>功能特性:</b></p>
        <ul>
        <li>浮态计算（吃水、纵倾、排水量）</li>
        <li>稳性计算（GZ曲线、稳性衡准）</li>
        <li>强度计算（剪力、弯矩）</li>
        <li>多工况支持（Transit、Semi-submerged等）</li>
        </ul>
        <br>
        <p>© 2026 Marine Engineering Software</p>
        """
        QMessageBox.about(self, "关于", about_text)

