"""
GUI validation test for semi-submersible ship loading computer
GUI验证测试
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Qt backend for testing
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
from unittest.mock import patch
from src.gui import MainWindow


def test_gui_initialization():
    """Test GUI initialization"""
    print("=" * 60)
    print("Testing GUI Initialization")
    print("=" * 60)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Test Application")
    
    # Create main window
    window = MainWindow()
    
    # Check components exist
    assert window.tab_widget is not None, "Tab widget not created"
    assert window.loading_editor is not None, "Loading editor not created"
    assert window.compartment_manager is not None, "Compartment manager not created"
    assert window.cargo_manager is not None, "Cargo manager not created"
    
    assert window.flotation_calc is not None, "Flotation calculator not created"
    assert window.stability_calc is not None, "Stability calculator not created"
    assert window.strength_calc is not None, "Strength calculator not created"
    
    print("✓ Main window created successfully")
    print("✓ All tabs initialized")
    print("✓ All calculators initialized")
    
    # Check tab count
    tab_count = window.tab_widget.count()
    print(f"✓ Number of tabs: {tab_count}")
    assert tab_count == 4, f"Expected 4 tabs, got {tab_count}"
    
    # Get tab names
    tab_names = [window.tab_widget.tabText(i) for i in range(tab_count)]
    print(f"✓ Tab names: {tab_names}")
    
    # Test calculation functionality (mock the message box)
    print("\nTesting calculation functionality...")
    try:
        # Mock QMessageBox to avoid dialog
        with patch('src.gui.main_window.QMessageBox.information'):
            window.calculate_all()
        
        print("✓ Calculation completed successfully")
        
        # Verify results were set
        assert window.flotation_results is not None, "Flotation results not set"
        assert window.stability_results is not None, "Stability results not set"
        assert window.strength_results is not None, "Strength results not set"
        
        print("✓ All calculation results generated")
        
        # Print some results
        print("\nCalculation Results:")
        print(f"  Displacement: {window.loading_condition.total_weight:.2f} t")
        print(f"  Mean Draft: {window.flotation_results['mean_draft']:.3f} m")
        print(f"  GMT (corrected): {window.stability_results['gmt_corrected']:.3f} m")
        
    except Exception as e:
        print(f"✗ Calculation failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✓ GUI initialization test passed!")
    return True


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("Semi-Submersible Ship Loading Computer - GUI Test")
    print("半潜船装载计算软件 - GUI测试")
    print("=" * 60)
    
    try:
        success = test_gui_initialization()
        
        if success:
            print("\n" + "=" * 60)
            print("✓ ALL GUI TESTS PASSED!")
            print("所有GUI测试通过！")
            print("=" * 60)
            return 0
        else:
            print("\n" + "=" * 60)
            print("✗ GUI TESTS FAILED!")
            print("GUI测试失败！")
            print("=" * 60)
            return 1
            
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ TEST FAILED: {e}")
        print("测试失败！")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
