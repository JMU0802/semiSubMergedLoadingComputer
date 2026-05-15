"""
Run GUI and take screenshot
"""
import sys
import os

# Set Qt backend for headless environment
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap
from src.gui import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Semi-Submersible Ship Loading Computer")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Process events to ensure window is fully rendered
    app.processEvents()
    
    # Take screenshot of the main window
    pixmap = window.grab()
    pixmap.save('gui_screenshot_main.png')
    print("✓ Screenshot saved: gui_screenshot_main.png")
    print(f"  Window size: {window.width()}x{window.height()}")
    
    # Perform a calculation to show results
    print("\n✓ Performing sample calculation...")
    window.calculate_all()
    app.processEvents()
    
    # Take screenshot after calculation
    pixmap = window.grab()
    pixmap.save('gui_screenshot_results.png')
    print("✓ Screenshot saved: gui_screenshot_results.png")
    
    # Switch to stability tab and take screenshot
    window.tab_widget.setCurrentIndex(2)  # Stability tab
    app.processEvents()
    pixmap = window.grab()
    pixmap.save('gui_screenshot_stability.png')
    print("✓ Screenshot saved: gui_screenshot_stability.png")
    
    # Switch to strength tab and take screenshot
    window.tab_widget.setCurrentIndex(3)  # Strength tab
    app.processEvents()
    pixmap = window.grab()
    pixmap.save('gui_screenshot_strength.png')
    print("✓ Screenshot saved: gui_screenshot_strength.png")
    
    print("\n✓ GUI application ran successfully!")
    print("✓ All screenshots captured!")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
