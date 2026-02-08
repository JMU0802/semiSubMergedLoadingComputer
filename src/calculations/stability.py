"""
Stability calculation module for semi-submersible ship loading computer.
稳性计算模块
"""

import numpy as np
from typing import List, Tuple, Dict
from ..models import LoadingCondition, HydrostaticData


class StabilityCalculator:
    """
    稳性计算器 / Stability Calculator
    
    Calculates:
    - GZ curve / GZ曲线
    - Stability criteria / 稳性衡准
    - Free surface correction / 自由液面修正
    """
    
    def __init__(self):
        """Initialize stability calculator"""
        pass
    
    def calculate_gz_curve(self, 
                          displacement: float,
                          vcg: float,
                          gmt: float,
                          bmt: float,
                          max_angle: float = 90.0,
                          angle_step: float = 5.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calculate GZ (righting arm) curve
        计算GZ（复原力臂）曲线
        
        Uses simplified GZ formula for semi-submersibles:
        GZ = GMT * sin(θ) for small angles
        GZ = (KM - KG) * sin(θ) for larger angles
        
        Args:
            displacement: Displacement in tonnes
            vcg: Vertical center of gravity (KG) in meters
            gmt: Transverse metacentric height in meters
            bmt: Transverse metacentric radius in meters
            max_angle: Maximum heel angle in degrees
            angle_step: Step size for angle calculation in degrees
            
        Returns:
            Tuple of (heel_angles, gz_values)
            - heel_angles: Array of heel angles in degrees
            - gz_values: Array of GZ values in meters
        """
        # Generate heel angles
        heel_angles = np.arange(0, max_angle + angle_step, angle_step)
        heel_rad = np.radians(heel_angles)
        
        # Calculate GZ values
        gz_values = np.zeros_like(heel_angles)
        
        for i, (angle, angle_rad) in enumerate(zip(heel_angles, heel_rad)):
            if angle <= 15:
                # For small angles, use linear approximation
                gz_values[i] = gmt * np.sin(angle_rad)
            else:
                # For larger angles, use simplified wall-sided formula
                # This is a simplified approach; actual calculation requires cross curves
                # GZ ≈ GMT * sin(θ) + (BMT/2) * sin(θ) * (1 - cos(θ))
                gz_values[i] = gmt * np.sin(angle_rad) + \
                              (bmt / 2.0) * np.sin(angle_rad) * (1 - np.cos(angle_rad))
        
        return heel_angles, gz_values
    
    def apply_free_surface_correction(self, gmt: float, 
                                     total_fsm: float,
                                     displacement: float) -> float:
        """
        Apply free surface correction to GMT
        对GMT进行自由液面修正
        
        Args:
            gmt: Original GMT in meters
            total_fsm: Total free surface moment in t·m
            displacement: Displacement in tonnes
            
        Returns:
            Corrected GMT in meters
        """
        if displacement == 0:
            return gmt
        
        # GMT_corrected = GMT - (FSM / Displacement)
        gm_correction = total_fsm / displacement
        gmt_corrected = gmt - gm_correction
        
        return gmt_corrected
    
    def check_stability_criteria(self, 
                                 heel_angles: np.ndarray,
                                 gz_values: np.ndarray,
                                 gmt: float,
                                 displacement: float) -> Dict[str, Dict]:
        """
        Check IMO stability criteria
        检查IMO稳性衡准
        
        Common IMO criteria:
        1. GMT ≥ 0.15 m (minimum)
        2. Maximum GZ ≥ 0.20 m at angle ≥ 30°
        3. Area under GZ curve 0-30° ≥ 0.055 m·rad
        4. Area under GZ curve 0-40° ≥ 0.090 m·rad
        5. Area under GZ curve 30-40° ≥ 0.030 m·rad
        6. Angle of maximum GZ ≥ 25°
        
        Args:
            heel_angles: Array of heel angles in degrees
            gz_values: Array of GZ values in meters
            gmt: Transverse metacentric height in meters
            displacement: Displacement in tonnes
            
        Returns:
            Dictionary with criteria check results
        """
        results = {}
        
        # Criterion 1: GMT ≥ 0.15 m
        results['GMT'] = {
            'value': gmt,
            'requirement': 0.15,
            'passed': gmt >= 0.15,
            'description': 'GMT ≥ 0.15 m / 初稳性高'
        }
        
        # Find maximum GZ and its angle
        max_gz_idx = np.argmax(gz_values)
        max_gz = gz_values[max_gz_idx]
        max_gz_angle = heel_angles[max_gz_idx]
        
        # Criterion 2: Maximum GZ ≥ 0.20 m at angle ≥ 30°
        max_gz_at_30 = max_gz if max_gz_angle >= 30 else 0
        results['Max_GZ'] = {
            'value': max_gz,
            'angle': max_gz_angle,
            'requirement': 0.20,
            'passed': max_gz >= 0.20 and max_gz_angle >= 30,
            'description': 'Max GZ ≥ 0.20 m at ≥ 30° / 最大GZ值'
        }
        
        # Calculate areas under GZ curve using trapezoidal integration
        # Convert angles to radians for area calculation
        heel_rad = np.radians(heel_angles)
        
        # Area 0-30°
        mask_30 = heel_angles <= 30
        if np.any(mask_30):
            try:
                # Try new numpy API (numpy >= 2.0)
                area_0_30 = np.trapezoid(gz_values[mask_30], heel_rad[mask_30])
            except AttributeError:
                # Fall back to old API (numpy < 2.0)
                area_0_30 = np.trapz(gz_values[mask_30], heel_rad[mask_30])
        else:
            area_0_30 = 0
        
        results['Area_0_30'] = {
            'value': area_0_30,
            'requirement': 0.055,
            'passed': area_0_30 >= 0.055,
            'description': 'Area 0-30° ≥ 0.055 m·rad / 0-30度面积'
        }
        
        # Area 0-40°
        mask_40 = heel_angles <= 40
        if np.any(mask_40):
            try:
                area_0_40 = np.trapezoid(gz_values[mask_40], heel_rad[mask_40])
            except AttributeError:
                area_0_40 = np.trapz(gz_values[mask_40], heel_rad[mask_40])
        else:
            area_0_40 = 0
        
        results['Area_0_40'] = {
            'value': area_0_40,
            'requirement': 0.090,
            'passed': area_0_40 >= 0.090,
            'description': 'Area 0-40° ≥ 0.090 m·rad / 0-40度面积'
        }
        
        # Area 30-40°
        mask_30_40 = (heel_angles >= 30) & (heel_angles <= 40)
        if np.any(mask_30_40):
            try:
                area_30_40 = np.trapezoid(gz_values[mask_30_40], heel_rad[mask_30_40])
            except AttributeError:
                area_30_40 = np.trapz(gz_values[mask_30_40], heel_rad[mask_30_40])
        else:
            area_30_40 = 0
        
        results['Area_30_40'] = {
            'value': area_30_40,
            'requirement': 0.030,
            'passed': area_30_40 >= 0.030,
            'description': 'Area 30-40° ≥ 0.030 m·rad / 30-40度面积'
        }
        
        # Criterion 6: Angle of maximum GZ ≥ 25°
        results['Max_GZ_Angle'] = {
            'value': max_gz_angle,
            'requirement': 25.0,
            'passed': max_gz_angle >= 25.0,
            'description': 'Angle of max GZ ≥ 25° / 最大GZ角度'
        }
        
        # Overall pass/fail
        all_passed = all(r['passed'] for r in results.values())
        results['Overall'] = {
            'passed': all_passed,
            'description': 'All criteria passed / 所有衡准满足' if all_passed 
                          else 'Some criteria failed / 部分衡准不满足'
        }
        
        return results
    
    def calculate_stability_with_correction(self,
                                           loading_condition: LoadingCondition,
                                           hydro_data: HydrostaticData,
                                           max_angle: float = 90.0,
                                           angle_step: float = 5.0) -> Tuple[np.ndarray, np.ndarray, float, Dict]:
        """
        Complete stability calculation with free surface correction
        完整稳性计算（含自由液面修正）
        
        Args:
            loading_condition: Loading condition
            hydro_data: Hydrostatic data at current draft
            max_angle: Maximum heel angle for GZ curve
            angle_step: Step size for GZ curve calculation
            
        Returns:
            Tuple of (heel_angles, gz_values, gmt_corrected, criteria_results)
        """
        # Get basic parameters
        displacement = loading_condition.total_weight
        vcg = loading_condition.vcg
        total_fsm = loading_condition.total_fsm
        
        # Apply free surface correction
        gmt_corrected = self.apply_free_surface_correction(
            hydro_data.gmt,
            total_fsm,
            displacement
        )
        
        # Calculate GZ curve with corrected GMT
        heel_angles, gz_values = self.calculate_gz_curve(
            displacement,
            vcg,
            gmt_corrected,
            hydro_data.bmt,
            max_angle,
            angle_step
        )
        
        # Check stability criteria
        criteria_results = self.check_stability_criteria(
            heel_angles,
            gz_values,
            gmt_corrected,
            displacement
        )
        
        return heel_angles, gz_values, gmt_corrected, criteria_results
