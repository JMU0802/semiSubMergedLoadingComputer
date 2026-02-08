"""
启动船舶装载工况计算系统GUI
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow


def main():
    """主函数"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # 使用Fusion风格
    
    # 设置应用程序信息
    app.setApplicationName("船舶装载工况计算系统")
    app.setOrganizationName("Semi-Submersible")
    app.setApplicationVersion("1.0")
    
    # 创建并显示主窗口
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

