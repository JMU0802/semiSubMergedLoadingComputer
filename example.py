"""
Example usage of the semi-submersible ship loading computer
半潜船装载计算软件使用示例
"""

import sys
sys.path.insert(0, '.')

from src.models import ShipParameters, LoadingCondition, Compartment, Cargo, CompartmentType
from src.calculations import FlotationCalculator, StabilityCalculator, StrengthCalculator
from src.data import get_sample_hydrostatic_table


def example_calculation():
    """
    示例：完整的装载计算流程
    Example: Complete loading calculation workflow
    """
    
    print("=" * 70)
    print("半潜船装载计算示例 / Semi-Submersible Ship Loading Example")
    print("=" * 70)
    
    # Step 1: Define ship parameters / 第一步：定义船舶参数
    print("\n1. Defining ship parameters / 定义船舶参数...")
    ship_params = ShipParameters(
        loa=190.0,              # 总长 190m
        lpp=180.0,              # 垂线间长 180m
        breadth=40.0,           # 型宽 40m
        depth=18.0,             # 型深 18m
        lightship_weight=12000.0,  # 空船重量 12000t
        lightship_lcg=0.0,      # 空船纵向重心 0m (at midship)
        lightship_tcg=0.0,      # 空船横向重心 0m (at centerline)
        lightship_vcg=9.5,      # 空船垂向重心 9.5m
        design_draft=10.0       # 设计吃水 10m
    )
    print(f"   Ship: LPP={ship_params.lpp}m, Breadth={ship_params.breadth}m")
    print(f"   Lightship: {ship_params.lightship_weight}t")
    
    # Step 2: Create loading condition / 第二步：创建装载工况
    print("\n2. Creating loading condition / 创建装载工况...")
    loading_condition = LoadingCondition(
        name="Example Loading Condition",
        description="Ballast condition with heavy cargo",
        ship_params=ship_params
    )
    
    # Step 3: Add compartments (ballast tanks) / 第三步：添加舱室（压载舱）
    print("\n3. Adding compartments / 添加舱室...")
    
    # Forward ballast tank / 前压载舱
    loading_condition.compartments.append(
        Compartment(
            name="Forward Ballast Tank",
            type=CompartmentType.BALLAST,
            capacity=500.0,     # 500 m³
            lcg=-60.0,          # 60m forward of midship
            tcg=0.0,            # On centerline
            vcg=5.0,            # 5m above baseline
            density=1.025,      # Seawater density
            fill_percentage=80.0,  # 80% full
            fsm=150.0           # Free surface moment
        )
    )
    
    # Aft ballast tank / 后压载舱
    loading_condition.compartments.append(
        Compartment(
            name="Aft Ballast Tank",
            type=CompartmentType.BALLAST,
            capacity=500.0,
            lcg=60.0,           # 60m aft of midship
            tcg=0.0,
            vcg=5.0,
            density=1.025,
            fill_percentage=75.0,  # 75% full
            fsm=145.0
        )
    )
    
    # Fuel tank / 燃油舱
    loading_condition.compartments.append(
        Compartment(
            name="Fuel Oil Tank",
            type=CompartmentType.FUEL,
            capacity=300.0,
            lcg=-30.0,
            tcg=5.0,            # 5m off centerline
            vcg=8.0,
            density=0.95,       # Fuel oil density
            fill_percentage=50.0,
            fsm=100.0
        )
    )
    
    total_comp_weight = sum(c.weight for c in loading_condition.compartments)
    print(f"   Added {len(loading_condition.compartments)} compartments")
    print(f"   Total compartment weight: {total_comp_weight:.2f}t")
    
    # Step 4: Add cargo / 第四步：添加货物
    print("\n4. Adding cargo / 添加货物...")
    
    # Heavy equipment on deck / 甲板重型设备
    loading_condition.cargos.append(
        Cargo(
            name="Heavy Equipment #1",
            weight=2000.0,      # 2000t
            lcg=0.0,            # At midship
            tcg=0.0,            # On centerline
            vcg=12.0            # 12m above baseline
        )
    )
    
    # Container stack / 集装箱堆
    loading_condition.cargos.append(
        Cargo(
            name="Container Stack",
            weight=500.0,
            lcg=40.0,           # 40m aft
            tcg=0.0,
            vcg=10.0
        )
    )
    
    total_cargo_weight = sum(c.weight for c in loading_condition.cargos)
    print(f"   Added {len(loading_condition.cargos)} cargo items")
    print(f"   Total cargo weight: {total_cargo_weight:.2f}t")
    
    # Step 5: Calculate flotation / 第五步：计算浮态
    print("\n5. Calculating flotation / 计算浮态...")
    
    hydrostatic_table = get_sample_hydrostatic_table()
    flotation_calc = FlotationCalculator(hydrostatic_table)
    
    mean_draft, trim, fwd_draft, aft_draft, hydro = flotation_calc.calculate_flotation(
        loading_condition,
        ship_params.lpp
    )
    
    trim_angle = flotation_calc.calculate_trim_angle(trim, ship_params.lpp)
    
    print(f"\n   Flotation Results / 浮态结果:")
    print(f"   --------------------------------")
    print(f"   Total Displacement:    {loading_condition.total_weight:.2f} t")
    print(f"   LCG (from midship):    {loading_condition.lcg:.3f} m")
    print(f"   VCG (from baseline):   {loading_condition.vcg:.3f} m")
    print(f"   Mean Draft:            {mean_draft:.3f} m")
    print(f"   Forward Draft:         {fwd_draft:.3f} m")
    print(f"   Aft Draft:             {aft_draft:.3f} m")
    print(f"   Trim:                  {trim:.3f} m ({'by stern' if trim > 0 else 'by bow'})")
    print(f"   Trim Angle:            {trim_angle:.4f}°")
    print(f"   GMT:                   {hydro.gmt:.3f} m")
    
    # Step 6: Calculate stability / 第六步：计算稳性
    print("\n6. Calculating stability / 计算稳性...")
    
    stability_calc = StabilityCalculator()
    
    heel_angles, gz_values, gmt_corrected, criteria = \
        stability_calc.calculate_stability_with_correction(
            loading_condition,
            hydro
        )
    
    print(f"\n   Stability Results / 稳性结果:")
    print(f"   --------------------------------")
    print(f"   GMT (original):        {hydro.gmt:.3f} m")
    print(f"   Free Surface Moment:   {loading_condition.total_fsm:.2f} t·m")
    print(f"   GMT (corrected):       {gmt_corrected:.3f} m")
    
    max_gz_idx = gz_values.argmax()
    print(f"   Max GZ:                {gz_values[max_gz_idx]:.4f} m at {heel_angles[max_gz_idx]:.1f}°")
    
    print(f"\n   Stability Criteria Check / 稳性衡准检查:")
    print(f"   --------------------------------")
    for key, value in criteria.items():
        if key == 'Overall':
            continue
        status = "✓" if value['passed'] else "✗"
        print(f"   {status} {key}")
    
    if criteria['Overall']['passed']:
        print(f"\n   ✓ All stability criteria PASSED! / 所有稳性衡准满足！")
    else:
        print(f"\n   ✗ Some criteria FAILED! / 部分衡准不满足！")
    
    # Step 7: Calculate strength / 第七步：计算强度
    print("\n7. Calculating strength / 计算强度...")
    
    strength_calc = StrengthCalculator(lpp=ship_params.lpp, num_stations=21)
    
    stations, shear_force, bending_moment = strength_calc.calculate_strength(
        loading_condition
    )
    
    max_sf, min_sf, max_bm, min_bm = strength_calc.get_max_values(
        shear_force,
        bending_moment
    )
    
    print(f"\n   Strength Results / 强度结果:")
    print(f"   --------------------------------")
    print(f"   Max Shear Force:       {max_sf:.2f} t")
    print(f"   Min Shear Force:       {min_sf:.2f} t")
    print(f"   Max Bending Moment:    {max_bm:.2f} t·m")
    print(f"   Min Bending Moment:    {min_bm:.2f} t·m")
    
    # Summary / 总结
    print("\n" + "=" * 70)
    print("Calculation Complete! / 计算完成！")
    print("=" * 70)
    print("\nThis example demonstrates:")
    print("  ✓ Ship parameter definition")
    print("  ✓ Loading condition setup")
    print("  ✓ Compartment and cargo management")
    print("  ✓ Flotation calculation (draft, trim)")
    print("  ✓ Stability calculation (GZ curve, criteria)")
    print("  ✓ Strength calculation (shear force, bending moment)")
    print("\nFor GUI interface, run: python main.py")
    print("=" * 70)


if __name__ == '__main__':
    example_calculation()
