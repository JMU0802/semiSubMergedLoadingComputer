"""
报表输出界面
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
                             QPushButton, QLabel, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextDocument
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from datetime import datetime


class ReportWidget(QWidget):
    """报表输出界面"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """初始化界面"""
        layout = QVBoxLayout(self)
        
        # 标题
        title = QLabel("报表输出")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 报表文本框
        self.report_text = QTextEdit()
        self.report_text.setFont(QFont("Courier New", 9))
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text, 1)
        
        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.export_pdf_button = QPushButton("导出PDF")
        self.export_pdf_button.setMinimumSize(100, 40)
        self.export_pdf_button.clicked.connect(self.export_pdf)
        button_layout.addWidget(self.export_pdf_button)
        
        self.export_txt_button = QPushButton("导出TXT")
        self.export_txt_button.setMinimumSize(100, 40)
        self.export_txt_button.clicked.connect(self.export_txt)
        button_layout.addWidget(self.export_txt_button)
        
        self.print_button = QPushButton("打印")
        self.print_button.setMinimumSize(100, 40)
        self.print_button.clicked.connect(self.print_report)
        button_layout.addWidget(self.print_button)
        
        layout.addLayout(button_layout)
        
    def update_report(self, loading_data, results):
        """更新报表内容"""
        print(f"\n=== ReportWidget.update_report() ===")
        print(f"loading_data: {loading_data is not None}")
        print(f"results: {results is not None}")
        if results:
            print(f"results keys: {results.keys()}")
        report = self.generate_report(loading_data, results)
        self.report_text.setPlainText(report)
        print(f"报表已更新，长度: {len(report)} 字符")
        print("=== 报表更新完成 ===\n")
        
    def generate_report(self, loading_data, results):
        """生成报表文本 - 完整格式"""
        if results is None:
            return "请先执行计算"

        report = []
        report.append("=" * 120)
        report.append(f"LOADING CONDITION: {loading_data.get('condition_name', 'Unknown')}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 120)
        report.append("")

        # FLOATING POSITION
        report.append("FLOATING POSITION")
        report.append("-" * 120)
        draught = results.get('draught', 0)
        km = results.get('km', 0)
        vcg = results.get('vcg', 0)
        gm0 = results.get('gm0', 0)
        dgm = results.get('dgm', 0)
        gmf = results.get('gmf', 0)
        trim = results.get('trim', 0)

        report.append(f"Mean draught (moulded)      {draught:8.2f} m    KM above the moulded base  {km:8.2f} m")
        report.append(f"Draught at AP (moulded)     {draught:8.2f} m    KG above the moulded base  {vcg:8.2f} m")
        report.append(f"Draught at FP (moulded)     {draught:8.2f} m    GM0 (solid)                {gm0:8.2f} m")
        report.append(f"Trim                        {trim:8.2f} m    Free surface correction    {dgm:8.2f} m")
        report.append(f"Heeling                     {0.00:8.2f} deg")
        report.append(f"                                         GM  (fluid)                {gmf:8.2f} m")
        report.append(f"Mean draught (heel 0)       {draught:8.2f} m")
        report.append(f"Trim (heel 0)               {trim:8.2f} m")
        report.append("")

        # LOADS - 详细装载数据
        self._append_loads_section(report, loading_data)

        # GZ CURVE DATA
        self._append_gz_curve_section(report, results)

        # STABILITY CRITERIA
        self._append_stability_criteria_section(report, results)

        report.append("")
        report.append("=" * 120)

        return "\n".join(report)

    def _append_loads_section(self, report, loading_data):
        """添加装载数据部分"""
        from ship_data.tank_definitions import ALL_TANKS

        report.append("LOADS")
        report.append("-" * 120)
        report.append(f"{'Location':<12} {'Description':<30} {'Weight':>10} {'Filling':>8} {'L.C.G.':>8} {'T.C.G.':>8} {'V.C.G.':>8} {'Frs.mom.':>10}")
        report.append(f"{'':<12} {'':<30} {'(t)':>10} {'%':>8} {'(m)':>8} {'(m)':>8} {'(m)':>8} {'(tm)':>10}")
        report.append("-" * 120)

        # 按类别组织舱室数据
        items = loading_data.get('items', [])

        # 分类统计
        categories = {
            'HFO': {'name': 'Heavy Fuel Oil', 'density': 0.991, 'items': []},
            'MGO': {'name': 'Diesel Oil', 'density': 0.900, 'items': []},
            'LO': {'name': 'Lubricating Oil', 'density': 0.900, 'items': []},
            'TW': {'name': 'Technical Water', 'density': 1.000, 'items': []},
            'FW': {'name': 'Fresh Water', 'density': 1.000, 'items': []},
            'WB': {'name': 'Ballast Water', 'density': 1.025, 'items': []},
            'WB_FIXED': {'name': 'Fixed FW ballast', 'density': 1.000, 'items': []},
            'GW': {'name': 'Grey Water', 'density': 1.000, 'items': []},
            'BILGE': {'name': 'Bilge Water', 'density': 1.000, 'items': []},
            'SLUDGE': {'name': 'Sludge', 'density': 2.380, 'items': []},
        }

        # 分类装载项
        for item in items:
            tank_id = item.get('tank_id', '')
            if 'HFO' in tank_id or 'T09.03' in tank_id or 'T09.04' in tank_id or 'T09.05' in tank_id or 'T09.06' in tank_id:
                categories['HFO']['items'].append(item)
            elif 'MGO' in tank_id or 'T09.07' in tank_id or 'T09.08' in tank_id or 'T09.18' in tank_id or 'T09.19' in tank_id:
                categories['MGO']['items'].append(item)
            elif 'T09.09' in tank_id:
                categories['LO']['items'].append(item)
            elif 'T09.10' in tank_id:
                categories['TW']['items'].append(item)
            elif 'FW' in tank_id or 'T10.01' in tank_id:
                categories['FW']['items'].append(item)
            elif 'WB02' in tank_id:
                categories['WB_FIXED']['items'].append(item)
            elif 'WB' in tank_id:
                categories['WB']['items'].append(item)
            elif 'T09.11' in tank_id or 'T09.13' in tank_id:
                categories['GW']['items'].append(item)
            elif 'T09.20' in tank_id or 'T09.22' in tank_id:
                categories['BILGE']['items'].append(item)
            elif 'T09.21' in tank_id:
                categories['SLUDGE']['items'].append(item)

        # 输出各类别
        for cat_key, cat_data in categories.items():
            if cat_data['items']:
                # 类别标题
                report.append("")
                report.append(f"{cat_data['name']} density={cat_data['density']:.3f} t/m3")

                total_weight = 0
                total_l_mom = 0
                total_t_mom = 0
                total_v_mom = 0
                total_fsm = 0

                for item in cat_data['items']:
                    tank_id = item.get('tank_id', '')
                    name = item.get('name', '')
                    weight = item.get('weight', 0)
                    filling = item.get('filling', 0)
                    lcg = item.get('lcg', 0)
                    vcg = item.get('vcg', 0)
                    fsm = item.get('fsm', 0)

                    # 获取TCG
                    tank_info = ALL_TANKS.get(tank_id, {})
                    tcg = tank_info.get('tcg', 0)

                    l_mom = weight * lcg
                    t_mom = weight * tcg
                    v_mom = weight * vcg

                    report.append(f"{tank_id:<12} {name:<30} {weight:10.1f} {filling:8.1f} {lcg:8.2f} {tcg:8.2f} {vcg:8.2f} {fsm:10.1f}")

                    total_weight += weight
                    total_l_mom += l_mom
                    total_t_mom += t_mom
                    total_v_mom += v_mom
                    total_fsm += fsm

                # 类别小计
                avg_lcg = total_l_mom / total_weight if total_weight > 0 else 0
                avg_tcg = total_t_mom / total_weight if total_weight > 0 else 0
                avg_vcg = total_v_mom / total_weight if total_weight > 0 else 0
                report.append(f"{'Total of ' + cat_data['name']:<43} {total_weight:10.1f} {'':<8} {avg_lcg:8.2f} {avg_tcg:8.2f} {avg_vcg:8.2f} {total_fsm:10.1f}")

        # 其他项目（Stores, Crew, Miscellaneous）
        report.append("")
        report.append("Stores")
        report.append(f"{'(STO)':<43} {100.0:10.1f} {'':<8} {199.20:8.2f} {0.00:8.2f} {29.05:8.2f} {0.0:10.1f}")
        report.append("")
        report.append("Crew")
        report.append(f"{'(CREW)':<43} {6.0:10.1f} {'':<8} {199.20:8.2f} {0.00:8.2f} {35.70:8.2f} {0.0:10.1f}")
        report.append("")
        report.append("Miscellaneous density=1.000 t/m3")
        report.append(f"{'(MIS)':<43} {87.0:10.1f} {'':<8} {178.40:8.2f} {0.00:8.2f} {5.00:8.2f} {0.0:10.1f}")

        # 总计
        report.append("-" * 120)
        dw_weight = loading_data.get('deadweight', 0)
        dw_lcg = loading_data.get('lcg', 0)  # 这是总LCG，需要计算DW的LCG
        dw_vcg = loading_data.get('vcg', 0)  # 这是总VCG，需要计算DW的VCG
        total_fsm = loading_data.get('fsm', 0)

        # 计算载重的平均位置
        lw_weight = loading_data.get('lightweight', 0)
        lw_lcg = loading_data.get('lw_lcg', 0)
        lw_vcg = loading_data.get('lw_vcg', 0)
        total_disp = loading_data.get('displacement', 0)
        total_lcg = loading_data.get('lcg', 0)
        total_vcg = loading_data.get('vcg', 0)

        if dw_weight > 0:
            dw_lcg_calc = (total_disp * total_lcg - lw_weight * lw_lcg) / dw_weight
            dw_vcg_calc = (total_disp * total_vcg - lw_weight * lw_vcg) / dw_weight
        else:
            dw_lcg_calc = 0
            dw_vcg_calc = 0

        report.append(f"{'Deadweight':<43} {dw_weight:10.1f} {'':<8} {dw_lcg_calc:8.2f} {0.00:8.2f} {dw_vcg_calc:8.2f} {total_fsm:10.1f}")
        report.append("")
        report.append(f"{'Lightweight':<43} {lw_weight:10.1f} {'':<8} {lw_lcg:8.2f} {-0.01:8.2f} {lw_vcg:8.2f}")
        report.append(f"{'Displacement (1.025 t/m3)':<43} {total_disp:10.1f} {'':<8} {total_lcg:8.2f} {-0.00:8.2f} {total_vcg:8.2f} {total_fsm:10.1f}")
        report.append("-" * 120)
        report.append("")

    def _append_gz_curve_section(self, report, results):
        """添加GZ曲线数据部分"""
        import numpy as np

        report.append("GZ CURVE DATA")
        report.append("-" * 120)
        report.append(f"{'Heel Angle':>12} {'sin(θ)':>12} {'KN':>12} {'KGf×sin(θ)':>14} {'GZ_corr_FSM':>14} {'GZ':>12}")
        report.append(f"{'(deg)':>12} {'':>12} {'(m)':>12} {'(m)':>14} {'(m)':>14} {'(m)':>12}")
        report.append("-" * 120)

        gz_data = results.get('gz_curve', {})
        angles = gz_data.get('angles', [])
        kn_values = gz_data.get('kn', [])
        kgf_sin_values = gz_data.get('kgf_sin', [])
        gz_corr_values = gz_data.get('gz_corr_fsm', [])
        gz_values = gz_data.get('gz', [])

        for i, angle in enumerate(angles):
            if i < len(gz_values):
                sin_theta = np.sin(np.radians(angle))
                kn = kn_values[i] if i < len(kn_values) else 0
                kgf_sin = kgf_sin_values[i] if i < len(kgf_sin_values) else 0
                gz_corr = gz_corr_values[i] if i < len(gz_corr_values) else 0
                gz = gz_values[i]

                report.append(f"{angle:12.1f} {sin_theta:12.4f} {kn:12.3f} {kgf_sin:14.3f} {gz_corr:14.3f} {gz:12.3f}")

        report.append("")

    def _append_stability_criteria_section(self, report, results):
        """添加稳性衡准部分"""
        report.append("STABILITY CRITERIA")
        report.append("-" * 120)
        report.append(f"{'RCR':<15} {'TEXT':<50} {'REQ':>12} {'ATTV':>12} {'UNIT':<10} {'STAT':<6}")
        report.append("-" * 120)

        criteria = results.get('criteria', {})

        # 定义衡准的显示文本
        criteria_text = {
            'V.AREA15-30': 'Area depending on GZ curve top',
            'V.AREA3040': 'Area under GZ curve between 30 and 40 deg',
            'V.GZ0.2': 'Min. GZ > 0.2',
            'V.POSMAX15': 'Top of GZ curve at least 15 degrees',
            'V.GM0.15': 'GM > 0.15 m',
        }

        criteria_units = {
            'V.AREA15-30': 'mrad',
            'V.AREA3040': 'mrad',
            'V.GZ0.2': 'm',
            'V.POSMAX15': 'deg',
            'V.GM0.15': 'm',
        }

        for name, data in criteria.items():
            text = criteria_text.get(name, name)
            unit = criteria_units.get(name, '')
            req = data.get('required', 0)
            attv = data.get('actual', 0)
            status = "OK" if data.get('pass', False) else "FAIL"

            # 格式化数值
            if 'AREA' in name:
                req_str = f"{req:.3f}"
                attv_str = f"{attv:.3f}"
            elif 'GZ' in name or 'GM' in name:
                req_str = f"{req:.3f}"
                attv_str = f"{attv:.3f}"
            else:
                req_str = f"{req:.3f}"
                attv_str = f"{attv:.3f}"

            report.append(f"{name:<15} {text:<50} {attv_str:>12} {req_str:>12} {unit:<10} {status:<6}")

        report.append("-" * 120)
        report.append("")

    def export_pdf(self):
        """导出PDF"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出PDF", "", "PDF Files (*.pdf)"
        )
        if filename:
            try:
                # 确保文件扩展名
                if not filename.endswith('.pdf'):
                    filename += '.pdf'

                # 创建打印机对象
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(filename)
                printer.setPageSize(QPrinter.A4)

                # 打印文档
                self.report_text.document().print_(printer)

                QMessageBox.information(self, "成功", f"报表已导出到:\n{filename}")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出PDF失败:\n{str(e)}")

    def export_txt(self):
        """导出TXT"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "导出TXT", "", "Text Files (*.txt)"
        )
        if filename:
            try:
                # 确保文件扩展名
                if not filename.endswith('.txt'):
                    filename += '.txt'

                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.report_text.toPlainText())

                QMessageBox.information(self, "成功", f"报表已导出到:\n{filename}")

            except Exception as e:
                QMessageBox.critical(self, "错误", f"导出TXT失败:\n{str(e)}")

    def print_report(self):
        """打印报表"""
        try:
            # 创建打印对话框
            printer = QPrinter(QPrinter.HighResolution)
            dialog = QPrintDialog(printer, self)

            if dialog.exec_() == QPrintDialog.Accepted:
                # 打印文档
                self.report_text.document().print_(printer)
                QMessageBox.information(self, "成功", "报表已发送到打印机")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"打印失败:\n{str(e)}")

