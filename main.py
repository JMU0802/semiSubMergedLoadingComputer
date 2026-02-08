"""
半潜船装载计算软件 - 主程序入口
Semi-Submersible Ship Loading Computer - Main Entry Point
"""

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from src.ui.main_window import MainWindow


def main():
    """主函数"""
    # 创建应用
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("半潜船装载计算软件")
    app.setOrganizationName("Marine Engineering Software")
    app.setApplicationVersion("1.0.0")
    
    # 设置默认字体
    font = QFont("Microsoft YaHei UI", 10)
    app.setFont(font)
    
    # 设置样式
    app.setStyle("Fusion")
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 运行应用
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

