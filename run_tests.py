"""
Test suite runner for semi-submersible ship loading computer
测试套件运行器
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests import test_calculations
from tests import test_gui


def run_all_tests():
    """Run all test suites"""
    print("\n" + "=" * 70)
    print("SEMI-SUBMERSIBLE SHIP LOADING COMPUTER - FULL TEST SUITE")
    print("半潜船装载计算软件 - 完整测试套件")
    print("=" * 70)
    
    results = []
    
    # Run calculation tests
    print("\n" + "=" * 70)
    print("PART 1: CALCULATION TESTS")
    print("=" * 70)
    result1 = test_calculations.main()
    results.append(("Calculation Tests", result1 == 0))
    
    # Run GUI tests
    print("\n" + "=" * 70)
    print("PART 2: GUI TESTS")
    print("=" * 70)
    result2 = test_gui.main()
    results.append(("GUI Tests", result2 == 0))
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY / 测试总结")
    print("=" * 70)
    
    for name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{status:12} - {name}")
    
    all_passed = all(passed for _, passed in results)
    
    print("=" * 70)
    if all_passed:
        print("✓ ALL TEST SUITES PASSED!")
        print("✓ 所有测试套件通过！")
    else:
        print("✗ SOME TEST SUITES FAILED!")
        print("✗ 部分测试套件失败！")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
