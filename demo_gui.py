"""
GUI Demonstration Script
演示GUI程序
"""
import sys
import os

# Set Qt backend for headless environment
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
from src.gui import MainWindow

def main():
    print("=" * 70)
    print("半潜船装载计算软件 GUI 演示")
    print("Semi-Submersible Ship Loading Computer GUI Demo")
    print("=" * 70)
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("Semi-Submersible Ship Loading Computer")
    
    print("\n✓ Creating main window...")
    window = MainWindow()
    
    print("✓ Main window created successfully")
    print(f"  Window title: {window.windowTitle()}")
    print(f"  Window size: {window.width()}x{window.height()}")
    print(f"  Number of tabs: {window.tab_widget.count()}")
    
    # List tabs
    print("\n✓ Available tabs:")
    for i in range(window.tab_widget.count()):
        tab_name = window.tab_widget.tabText(i)
        print(f"  {i+1}. {tab_name}")
    
    # Show initial loading condition
    print("\n✓ Initial loading condition:")
    print(f"  Ship LPP: {window.ship_params.lpp} m")
    print(f"  Ship Breadth: {window.ship_params.breadth} m")
    print(f"  Lightship: {window.ship_params.lightship_weight} t")
    print(f"  Compartments: {len(window.compartment_manager.compartments)}")
    print(f"  Cargos: {len(window.cargo_manager.cargos)}")
    
    # Perform calculation
    print("\n✓ Performing calculations...")
    window.calculate_all()
    
    # Display results
    print("\n✓ Calculation Results:")
    print("  " + "-" * 60)
    
    if window.flotation_results:
        print("  Flotation / 浮态:")
        print(f"    Displacement: {window.loading_condition.total_weight:.2f} t")
        print(f"    Mean Draft: {window.flotation_results['mean_draft']:.3f} m")
        print(f"    Forward Draft: {window.flotation_results['fwd_draft']:.3f} m")
        print(f"    Aft Draft: {window.flotation_results['aft_draft']:.3f} m")
        print(f"    Trim: {window.flotation_results['trim']:.3f} m")
        print(f"    Trim Angle: {window.flotation_results['trim_angle']:.4f}°")
    
    if window.stability_results:
        print("\n  Stability / 稳性:")
        print(f"    GMT (corrected): {window.stability_results['gmt_corrected']:.3f} m")
        criteria = window.stability_results['criteria']
        passed = sum(1 for k, v in criteria.items() if k != 'Overall' and v['passed'])
        total = len(criteria) - 1
        print(f"    Stability Criteria: {passed}/{total} PASSED")
        
        if criteria['Overall']['passed']:
            print("    ✓ All IMO stability criteria satisfied!")
        else:
            print("    ✗ Some criteria not satisfied")
    
    if window.strength_results:
        print("\n  Strength / 强度:")
        import numpy as np
        sf = window.strength_results['shear_force']
        bm = window.strength_results['bending_moment']
        print(f"    Max Shear Force: {np.max(sf):.2f} t")
        print(f"    Min Shear Force: {np.min(sf):.2f} t")
        print(f"    Max Bending Moment: {np.max(bm):.2f} t·m")
        print(f"    Min Bending Moment: {np.min(bm):.2f} t·m")
    
    print("\n" + "=" * 70)
    print("✓ GUI Application Demo Complete!")
    print("=" * 70)
    print("\nTo run the full GUI interface:")
    print("  python main.py")
    print("\nNote: In a graphical environment, the GUI will display with:")
    print("  - Interactive compartment and cargo management")
    print("  - Real-time calculation results")
    print("  - GZ curve visualization")
    print("  - Shear force and bending moment plots")
    print("  - Stability criteria check table")
    print("=" * 70)
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
