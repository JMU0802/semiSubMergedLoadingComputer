"""
Main entry point for semi-submersible ship loading computer
半潜船装载计算软件主入口
"""

import sys
from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow


def main():
    """Main function"""
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("Semi-Submersible Ship Loading Computer")
    app.setOrganizationName("Maritime Engineering")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
