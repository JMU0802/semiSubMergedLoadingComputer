"""
主窗口 - 船舶装载工况计算系统
Semi-Submersible Loading Condition Calculator
"""

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTabWidget, QMenuBar, QMenu, QAction,
                             QStatusBar, QToolBar, QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QColor
import json
import os

from gui.form1_widget import Form1Widget
from gui.form2_widget import Form2Widget
from gui.report_widget import ReportWidget
from gui.ship_data_viewer import ShipDataViewer


class MainWindow(QMainWindow):
    """主窗口类"""
    
    def __init__(self):
        super().__init__()
        self.current_condition = None
        self.default_conditions = []  # 存储13个默认工况
        self.init_ui()
        self.load_default_conditions()  # 加载默认工况
        
    def init_ui(self):
        """初始化用户界面"""
        self.setWindowTitle("船舶装载工况计算系统 - Semi-Submersible Loading Condition Calculator")
        self.setGeometry(100, 100, 1400, 900)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Arial", 10))
        
        # Form 1: 装载数据输入
        self.form1_widget = Form1Widget()
        self.tab_widget.addTab(self.form1_widget, "FORM 1 - 装载数据")
        
        # Form 2: 稳性与强度计算
        self.form2_widget = Form2Widget()
        self.tab_widget.addTab(self.form2_widget, "FORM 2 - 稳性与强度")
        
        # 报表视图
        self.report_widget = ReportWidget()
        self.tab_widget.addTab(self.report_widget, "报表输出")

        # 船舶数据查看器
        self.ship_data_viewer = ShipDataViewer()
        self.tab_widget.addTab(self.ship_data_viewer, "船舶数据")

        main_layout.addWidget(self.tab_widget)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")
        
        # 连接信号
        self.connect_signals()
        
    def create_menu_bar(self):
        """创建菜单栏"""
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu("文件(&F)")
        
        new_action = QAction("新建工况(&N)", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_condition)
        file_menu.addAction(new_action)
        
        open_action = QAction("打开工况(&O)", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_condition)
        file_menu.addAction(open_action)
        
        save_action = QAction("保存工况(&S)", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_condition)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("导出报表(&E)", self)
        export_action.triggered.connect(self.export_report)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 工况菜单
        condition_menu = menubar.addMenu("工况(&L)")

        # 添加13个默认工况的子菜单
        self.condition_actions = []
        condition_names = [
            "LC00 - Lightship",
            "LC01 - Departure",
            "LC02 - Arrival",
            "LC03 - Ballast Departure",
            "LC04 - Ballast Arrival",
            "LC05 - Maximum Deadweight",
            "LC11 - Loading Condition 11",
            "LC12 - Loading Condition 12",
            "LC23 - Loading Condition 23",
            "LC24 - Loading Condition 24",
            "LC25 - Loading Condition 25",
            "LC26 - Loading Condition 26",
            "LC31 - Loading Condition 31",
        ]

        for i, name in enumerate(condition_names):
            action = QAction(name, self)
            action.triggered.connect(lambda checked, idx=i: self.load_condition_by_index(idx))
            condition_menu.addAction(action)
            self.condition_actions.append(action)

        # 计算菜单
        calc_menu = menubar.addMenu("计算(&C)")

        calc_action = QAction("执行计算(&C)", self)
        calc_action.setShortcut("F5")
        calc_action.triggered.connect(self.calculate)
        calc_menu.addAction(calc_action)

        calc_all_action = QAction("计算所有工况(&A)", self)
        calc_all_action.setShortcut("Ctrl+F5")
        calc_all_action.triggered.connect(self.calculate_all_conditions)
        calc_menu.addAction(calc_all_action)

        calc_menu.addSeparator()

        verify_action = QAction("验证稳性(&V)", self)
        verify_action.triggered.connect(self.verify_stability)
        calc_menu.addAction(verify_action)
        
        # 视图菜单
        view_menu = menubar.addMenu("视图(&V)")
        
        form1_action = QAction("FORM 1", self)
        form1_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
        view_menu.addAction(form1_action)
        
        form2_action = QAction("FORM 2", self)
        form2_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
        view_menu.addAction(form2_action)
        
        report_action = QAction("报表", self)
        report_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(2))
        view_menu.addAction(report_action)
        
        # 帮助菜单
        help_menu = menubar.addMenu("帮助(&H)")
        
        about_action = QAction("关于(&A)", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_tool_bar(self):
        """创建工具栏"""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(32, 32))
        self.addToolBar(toolbar)
        
        # 新建
        new_action = QAction("新建", self)
        new_action.triggered.connect(self.new_condition)
        toolbar.addAction(new_action)
        
        # 打开
        open_action = QAction("打开", self)
        open_action.triggered.connect(self.open_condition)
        toolbar.addAction(open_action)
        
        # 保存
        save_action = QAction("保存", self)
        save_action.triggered.connect(self.save_condition)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # 计算
        calc_action = QAction("计算", self)
        calc_action.triggered.connect(self.calculate)
        toolbar.addAction(calc_action)
        
        # 验证
        verify_action = QAction("验证", self)
        verify_action.triggered.connect(self.verify_stability)
        toolbar.addAction(verify_action)
        
    def connect_signals(self):
        """连接信号和槽"""
        # Form1的计算按钮连接到计算函数
        self.form1_widget.calculate_clicked.connect(self.calculate)
        
        # Form2的数据更新信号
        self.form2_widget.data_updated.connect(self.update_report)
        
    def new_condition(self):
        """新建工况"""
        self.form1_widget.clear_all()
        self.form2_widget.clear_all()
        self.status_bar.showMessage("新建工况")
        
    def open_condition(self):
        """打开工况"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "打开工况", "", "Loading Condition Files (*.lc.json);;All Files (*)"
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                # 加载数据到Form1
                self.load_condition_data(data)

                self.status_bar.showMessage(f"已打开: {filename}")
                QMessageBox.information(self, "成功", "工况数据已加载")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"打开文件失败：\n{str(e)}")
                self.status_bar.showMessage("打开失败")

    def save_condition(self):
        """保存工况"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "保存工况", "", "Loading Condition Files (*.lc.json);;All Files (*)"
        )
        if filename:
            # 确保文件扩展名
            if not filename.endswith('.lc.json'):
                filename += '.lc.json'

            try:
                # 获取Form1的数据
                data = self.form1_widget.get_loading_data()

                # 保存到文件
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                self.status_bar.showMessage(f"已保存: {filename}")
                QMessageBox.information(self, "成功", "工况数据已保存")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存文件失败：\n{str(e)}")
                self.status_bar.showMessage("保存失败")

    def load_condition_data(self, data):
        """加载工况数据到界面"""
        # Form1Widget使用condition_combo而不是condition_name
        # 我们不需要设置它，因为它已经通过load_default_condition设置了

        # 设置舱室装载
        items = data.get('items', [])

        # 先清空所有舱室
        self.form1_widget.table.blockSignals(True)
        for row in range(self.form1_widget.table.rowCount()):
            item_widget = self.form1_widget.table.item(row, 0)
            if item_widget and ':' in item_widget.text():  # 舱室行
                weight_item = self.form1_widget.table.item(row, 3)
                if weight_item:
                    weight_item.setText("0.0")

        # 设置工况中的装载
        for item in items:
            tank_id = item.get('tank_id')
            weight = item.get('weight', 0)

            # 在表格中找到对应的舱室
            for row in range(self.form1_widget.table.rowCount()):
                name_item = self.form1_widget.table.item(row, 0)
                if name_item and name_item.text().startswith(tank_id + ":"):
                    weight_item = self.form1_widget.table.item(row, 3)
                    if weight_item:
                        weight_item.setText(f"{weight:.1f}")
                    break

        self.form1_widget.table.blockSignals(False)

        # 重新计算
        self.form1_widget.update_summary()
        
    def calculate(self):
        """执行计算"""
        try:
            self.status_bar.showMessage("正在计算...")
            
            # 从Form1获取装载数据
            loading_data = self.form1_widget.get_loading_data()
            
            # 传递给Form2进行计算
            self.form2_widget.calculate(loading_data)
            
            # 切换到Form2显示结果
            self.tab_widget.setCurrentIndex(1)
            
            self.status_bar.showMessage("计算完成")
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"计算过程中发生错误：\n{str(e)}")
            self.status_bar.showMessage("计算失败")
            
    def verify_stability(self):
        """验证稳性"""
        try:
            # 获取Form2的计算结果
            results = self.form2_widget.get_results()
            
            if results is None:
                QMessageBox.warning(self, "警告", "请先执行计算！")
                return
            
            # 检查稳性衡准
            criteria_results = results.get('criteria', {})
            
            # 显示结果
            msg = "稳性衡准检查结果：\n\n"
            all_pass = True
            
            for name, data in criteria_results.items():
                status = "✓ 通过" if data.get('pass', False) else "✗ 不通过"
                msg += f"{name}: {status}\n"
                if not data.get('pass', False):
                    all_pass = False
            
            if all_pass:
                QMessageBox.information(self, "稳性验证", msg + "\n所有衡准通过！")
            else:
                QMessageBox.warning(self, "稳性验证", msg + "\n部分衡准不通过！")
                
        except Exception as e:
            QMessageBox.critical(self, "验证错误", f"验证过程中发生错误：\n{str(e)}")
            
    def update_report(self):
        """更新报表"""
        try:
            # 获取Form1和Form2的数据
            loading_data = self.form1_widget.get_loading_data()
            results = self.form2_widget.get_results()
            
            # 更新报表
            self.report_widget.update_report(loading_data, results)
            
        except Exception as e:
            print(f"更新报表错误: {e}")
            
    def export_report(self):
        """导出报表"""
        # TODO: 实现报表导出功能
        self.status_bar.showMessage("导出报表...")
        
    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于",
                         "船舶装载工况计算系统\n"
                         "Semi-Submersible Loading Condition Calculator\n\n"
                         "版本: 1.0\n"
                         "用于半潜船装载工况计算和稳性验证")

    def load_default_conditions(self):
        """加载13个默认工况"""
        condition_files = [
            'LC00.json', 'LC01.json', 'LC02.json', 'LC03.json',
            'LC04.json', 'LC05.json', 'LC11.json', 'LC12.json',
            'LC23.json', 'LC24.json', 'LC25.json', 'LC26.json',
            'LC31.json'
        ]

        self.default_conditions = []

        for filename in condition_files:
            filepath = os.path.join('default_conditions', filename)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    self.default_conditions.append(data)
                    print(f"已加载工况: {filename}")
                except Exception as e:
                    print(f"加载工况 {filename} 失败: {e}")
                    self.default_conditions.append(None)
            else:
                print(f"工况文件不存在: {filepath}")
                self.default_conditions.append(None)

        print(f"共加载 {len([c for c in self.default_conditions if c is not None])} 个默认工况")

    def load_condition_by_index(self, index):
        """根据索引加载工况"""
        if index < 0 or index >= len(self.default_conditions):
            QMessageBox.warning(self, "警告", "工况索引无效")
            return

        condition_data = self.default_conditions[index]
        if condition_data is None:
            QMessageBox.warning(self, "警告", "该工况数据未加载")
            return

        try:
            # 转换工况数据格式以适配GUI
            converted_data = self.convert_condition_data(condition_data)

            # 加载到Form1
            self.load_condition_data(converted_data)

            # 自动执行计算
            self.calculate()

            condition_name = condition_data.get('name', f'LC{index:02d}')
            self.status_bar.showMessage(f"已加载工况: {condition_name}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载工况失败：\n{str(e)}")
            import traceback
            traceback.print_exc()

    def convert_condition_data(self, condition_data):
        """转换工况数据格式"""
        from ship_data.tanks_details_data import get_tank_info

        # 获取工况名称
        condition_name = condition_data.get('name', 'Unknown')

        # 空船数据（固定值）
        lightweight = 20871.4
        lw_lcg = 113.44
        lw_vcg = 10.44

        # 处理舱室数据
        tanks_data = condition_data.get('tanks', {})
        items = []

        for tank_id, tank_info_dict in tanks_data.items():
            weight = tank_info_dict.get('weight', 0)

            if weight > 0:
                # 获取舱室详细信息
                tank_details = get_tank_info(tank_id)

                if tank_details:
                    # 使用舱室详细信息中的LCG/VCG
                    lcg = tank_details.get('lcg', 0)
                    vcg = tank_details.get('vcg', 0)
                else:
                    # 如果没有详细信息，使用默认值
                    lcg = 100.0
                    vcg = 5.0

                items.append({
                    'tank_id': tank_id,
                    'filling': 100,  # 假设100%填充
                    'weight': weight,
                    'lcg': lcg,
                    'vcg': vcg,
                    'tcg': 0.0,
                    'fsm': 0.0
                })

        # 计算总重量和重心
        total_weight = lightweight
        total_moment_lcg = lightweight * lw_lcg
        total_moment_vcg = lightweight * lw_vcg
        total_fsm = 0.0

        for item in items:
            total_weight += item['weight']
            total_moment_lcg += item['weight'] * item['lcg']
            total_moment_vcg += item['weight'] * item['vcg']
            total_fsm += item.get('fsm', 0)

        lcg = total_moment_lcg / total_weight if total_weight > 0 else 0
        vcg = total_moment_vcg / total_weight if total_weight > 0 else 0

        return {
            'condition_name': condition_name,
            'lightweight': lightweight,
            'lw_lcg': lw_lcg,
            'lw_vcg': lw_vcg,
            'items': items,
            'displacement': total_weight,
            'lcg': lcg,
            'vcg': vcg,
            'fsm': total_fsm
        }

    def calculate_all_conditions(self):
        """计算所有13个工况"""
        from PyQt5.QtWidgets import QProgressDialog

        # 创建进度对话框
        progress = QProgressDialog("正在计算所有工况...", "取消", 0, len(self.default_conditions), self)
        progress.setWindowTitle("批量计算")
        progress.setWindowModality(Qt.WindowModal)

        results_summary = []

        for i, condition_data in enumerate(self.default_conditions):
            if progress.wasCanceled():
                break

            if condition_data is None:
                continue

            progress.setValue(i)
            condition_name = condition_data.get('name', f'LC{i:02d}')
            progress.setLabelText(f"正在计算: {condition_name}")

            try:
                # 转换并计算
                converted_data = self.convert_condition_data(condition_data)

                # 执行计算（不更新界面）
                self.form2_widget.calculate(converted_data)
                results = self.form2_widget.get_results()

                if results:
                    # 收集关键结果
                    summary = {
                        'name': condition_name,
                        'displacement': results.get('displacement', 0),
                        'draught': results.get('draught', 0),
                        'gmf': results.get('gmf', 0),
                        'stability_ok': all(c.get('pass', False) for c in results.get('criteria', {}).values()),
                    }

                    # 添加强度结果
                    if 'strength' in results and results['strength']:
                        strength = results['strength']
                        summary['strength_ok'] = strength.get('all_ok', False)
                        summary['max_shear'] = strength.get('max_shear_force', 0)
                        summary['max_bending'] = strength.get('max_sagging_moment', 0)
                    else:
                        summary['strength_ok'] = None

                    results_summary.append(summary)

            except Exception as e:
                print(f"计算工况 {condition_name} 失败: {e}")

        progress.setValue(len(self.default_conditions))

        # 显示汇总结果
        self.show_results_summary(results_summary)

    def show_results_summary(self, results_summary):
        """显示计算结果汇总"""
        from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton

        dialog = QDialog(self)
        dialog.setWindowTitle("所有工况计算结果汇总")
        dialog.setGeometry(200, 200, 900, 600)

        layout = QVBoxLayout(dialog)

        # 创建表格
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "工况", "排水量(t)", "吃水(m)", "GMf(m)",
            "稳性", "强度", "最大剪力(kN)"
        ])
        table.setRowCount(len(results_summary))

        for i, result in enumerate(results_summary):
            table.setItem(i, 0, QTableWidgetItem(result['name']))
            table.setItem(i, 1, QTableWidgetItem(f"{result['displacement']:.1f}"))
            table.setItem(i, 2, QTableWidgetItem(f"{result['draught']:.2f}"))
            table.setItem(i, 3, QTableWidgetItem(f"{result['gmf']:.3f}"))

            # 稳性状态
            stability_item = QTableWidgetItem("✓ 通过" if result['stability_ok'] else "✗ 不通过")
            stability_item.setForeground(QColor(0, 128, 0) if result['stability_ok'] else QColor(255, 0, 0))
            table.setItem(i, 4, stability_item)

            # 强度状态
            if result['strength_ok'] is not None:
                strength_item = QTableWidgetItem("✓ 通过" if result['strength_ok'] else "✗ 不通过")
                strength_item.setForeground(QColor(0, 128, 0) if result['strength_ok'] else QColor(255, 0, 0))
            else:
                strength_item = QTableWidgetItem("未计算")
            table.setItem(i, 5, strength_item)

            # 最大剪力
            if 'max_shear' in result:
                table.setItem(i, 6, QTableWidgetItem(f"{result['max_shear']:.1f}"))
            else:
                table.setItem(i, 6, QTableWidgetItem("-"))

        table.resizeColumnsToContents()
        layout.addWidget(table)

        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)

        dialog.exec_()


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

