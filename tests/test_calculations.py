"""
Test script for semi-submersible ship loading computer
测试脚本
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models import ShipParameters, LoadingCondition, Compartment, Cargo, CompartmentType
from src.calculations import FlotationCalculator, StabilityCalculator, StrengthCalculator
from src.data import get_sample_hydrostatic_table


def test_flotation_calculation():
    """Test flotation calculation"""
    print("=" * 60)
    print("Testing Flotation Calculation")
    print("=" * 60)
    
    # Create ship parameters
    ship_params = ShipParameters(
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
    
    # Create loading condition
    loading_condition = LoadingCondition(
        name="Test Condition",
        description="Test loading condition",
        ship_params=ship_params
    )
    
    # Add compartments
    loading_condition.compartments.append(
        Compartment("Ballast #1", CompartmentType.BALLAST, 500, -60, 0, 5, 1.025, 80, 150)
    )
    loading_condition.compartments.append(
        Compartment("Ballast #2", CompartmentType.BALLAST, 500, 60, 0, 5, 1.025, 75, 145)
    )
    
    # Add cargo
    loading_condition.cargos.append(
        Cargo("Heavy Equipment", 2000, 0, 0, 12)
    )
    
    # Initialize calculator
    hydrostatic_table = get_sample_hydrostatic_table()
    calc = FlotationCalculator(hydrostatic_table)
    
    # Calculate flotation
    mean_draft, trim, fwd_draft, aft_draft, hydro = calc.calculate_flotation(
        loading_condition,
        ship_params.lpp
    )
    
    trim_angle = calc.calculate_trim_angle(trim, ship_params.lpp)
    
    # Print results
    print(f"\nTotal Weight: {loading_condition.total_weight:.2f} t")
    print(f"LCG: {loading_condition.lcg:.3f} m")
    print(f"VCG: {loading_condition.vcg:.3f} m")
    print(f"\nMean Draft: {mean_draft:.3f} m")
    print(f"Forward Draft: {fwd_draft:.3f} m")
    print(f"Aft Draft: {aft_draft:.3f} m")
    print(f"Trim: {trim:.3f} m")
    print(f"Trim Angle: {trim_angle:.4f} deg")
    print(f"\nGMT: {hydro.gmt:.3f} m")
    print(f"LCB: {hydro.lcb:.3f} m")
    print(f"VCB: {hydro.vcb:.3f} m")
    
    print("\n✓ Flotation calculation test passed!")
    return loading_condition, hydro


def test_stability_calculation(loading_condition, hydro):
    """Test stability calculation"""
    print("\n" + "=" * 60)
    print("Testing Stability Calculation")
    print("=" * 60)
    
    calc = StabilityCalculator()
    
    # Calculate stability
    heel_angles, gz_values, gmt_corrected, criteria = \
        calc.calculate_stability_with_correction(loading_condition, hydro)
    
    # Print results
    print(f"\nGMT (original): {hydro.gmt:.3f} m")
    print(f"GMT (corrected): {gmt_corrected:.3f} m")
    print(f"Free Surface Moment: {loading_condition.total_fsm:.2f} t·m")
    
    print("\nGZ Curve (selected points):")
    for i in range(0, len(heel_angles), 6):  # Print every 30 degrees
        print(f"  {heel_angles[i]:5.1f}° -> GZ = {gz_values[i]:7.4f} m")
    
    print("\nStability Criteria Check:")
    for key, value in criteria.items():
        if key == 'Overall':
            continue
        status = "✓ PASS" if value['passed'] else "✗ FAIL"
        print(f"  {status} - {value['description']}")
        if 'value' in value:
            print(f"       Actual: {value['value']:.4f}, Required: {value.get('requirement', 'N/A')}")
    
    overall = criteria['Overall']
    if overall['passed']:
        print("\n✓ All stability criteria PASSED!")
    else:
        print("\n✗ Some stability criteria FAILED!")
    
    print("\n✓ Stability calculation test passed!")


def test_strength_calculation(loading_condition):
    """Test strength calculation"""
    print("\n" + "=" * 60)
    print("Testing Strength Calculation")
    print("=" * 60)
    
    calc = StrengthCalculator(lpp=180.0, num_stations=21)
    
    # Calculate strength
    stations, shear_force, bending_moment = calc.calculate_strength(loading_condition)
    
    # Get max values
    max_sf, min_sf, max_bm, min_bm = calc.get_max_values(shear_force, bending_moment)
    
    # Print results
    print(f"\nShear Force:")
    print(f"  Maximum: {max_sf:.2f} t")
    print(f"  Minimum: {min_sf:.2f} t")
    
    print(f"\nBending Moment:")
    print(f"  Maximum: {max_bm:.2f} t·m")
    print(f"  Minimum: {min_bm:.2f} t·m")
    
    print("\nShear Force Distribution (selected stations):")
    for i in range(0, len(stations), 5):  # Print every 5th station
        print(f"  x = {stations[i]:7.2f} m -> SF = {shear_force[i]:8.2f} t")
    
    print("\n✓ Strength calculation test passed!")


def main():
    """Main test function"""
    print("\n" + "=" * 60)
    print("Semi-Submersible Ship Loading Computer - Test Suite")
    print("半潜船装载计算软件 - 测试套件")
    print("=" * 60)
    
    try:
        # Test flotation
        loading_condition, hydro = test_flotation_calculation()
        
        # Test stability
        test_stability_calculation(loading_condition, hydro)
        
        # Test strength
        test_strength_calculation(loading_condition)
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("所有测试通过！")
        print("=" * 60)
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"✗ TEST FAILED: {e}")
        print("测试失败！")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
