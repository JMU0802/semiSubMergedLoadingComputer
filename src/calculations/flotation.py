"""
Flotation calculation module for semi-submersible ship loading computer.
浮态计算模块
"""

import numpy as np
from scipy.interpolate import interp1d
from typing import List, Tuple, Optional
from ..models import HydrostaticData, LoadingCondition


class FlotationCalculator:
    """
    浮态计算器 / Flotation Calculator
    
    Based on hydrostatic curves, calculates:
    - Displacement / 排水量
    - Draft (mean, forward, aft) / 吃水
    - Trim (value and angle) / 纵倾
    - Hydrostatic parameters / 静水力参数
    """
    
    def __init__(self, hydrostatic_table: List[HydrostaticData]):
        """
        Initialize with hydrostatic data table
        
        Args:
            hydrostatic_table: List of hydrostatic data points
        """
        self.hydrostatic_table = sorted(hydrostatic_table, key=lambda x: x.draft)
        self._build_interpolators()
    
    def _build_interpolators(self):
        """Build interpolation functions for hydrostatic parameters"""
        if not self.hydrostatic_table:
            raise ValueError("Hydrostatic table cannot be empty")
        
        drafts = np.array([h.draft for h in self.hydrostatic_table])
        
        # Create interpolators for each parameter
        self.disp_interp = interp1d(
            drafts,
            [h.displacement for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.lcb_interp = interp1d(
            drafts,
            [h.lcb for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.vcb_interp = interp1d(
            drafts,
            [h.vcb for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.lcf_interp = interp1d(
            drafts,
            [h.lcf for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.tpc_interp = interp1d(
            drafts,
            [h.tpc for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.mct_interp = interp1d(
            drafts,
            [h.mct for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.kb_interp = interp1d(
            drafts,
            [h.kb for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.bm_interp = interp1d(
            drafts,
            [h.bm for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.gmt_interp = interp1d(
            drafts,
            [h.gmt for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
        
        self.bmt_interp = interp1d(
            drafts,
            [h.bmt for h in self.hydrostatic_table],
            kind='cubic',
            fill_value='extrapolate'
        )
    
    def get_draft_from_displacement(self, displacement: float, 
                                   initial_guess: float = None,
                                   tolerance: float = 0.001) -> float:
        """
        Calculate draft from displacement using iteration
        根据排水量计算吃水（迭代法）
        
        Args:
            displacement: Target displacement in tonnes
            initial_guess: Initial draft guess (m)
            tolerance: Convergence tolerance
            
        Returns:
            Draft in meters
        """
        if initial_guess is None:
            # Use mid-range draft as initial guess
            initial_guess = np.mean([h.draft for h in self.hydrostatic_table])
        
        draft = initial_guess
        max_iterations = 100
        
        for i in range(max_iterations):
            current_disp = float(self.disp_interp(draft))
            error = displacement - current_disp
            
            if abs(error) < tolerance:
                return draft
            
            # Use TPC to estimate draft change
            tpc = float(self.tpc_interp(draft))
            if tpc > 0:
                # TPC is in t/cm, convert to t/m
                draft_change = error / (tpc * 100)
                draft += draft_change
            else:
                # Fallback to simple bisection if TPC is invalid
                draft += error / 1000
        
        # If not converged, return best estimate
        return draft
    
    def interpolate_hydrostatic_data(self, draft: float) -> HydrostaticData:
        """
        Interpolate all hydrostatic parameters at given draft
        在给定吃水处插值所有静水力参数
        
        Args:
            draft: Draft in meters
            
        Returns:
            HydrostaticData object with interpolated values
        """
        return HydrostaticData(
            draft=draft,
            displacement=float(self.disp_interp(draft)),
            lcb=float(self.lcb_interp(draft)),
            vcb=float(self.vcb_interp(draft)),
            lcf=float(self.lcf_interp(draft)),
            tpc=float(self.tpc_interp(draft)),
            mct=float(self.mct_interp(draft)),
            kb=float(self.kb_interp(draft)),
            bm=float(self.bm_interp(draft)),
            gmt=float(self.gmt_interp(draft)),
            bmt=float(self.bmt_interp(draft))
        )
    
    def calculate_flotation(self, loading_condition: LoadingCondition,
                           lpp: float) -> Tuple[float, float, float, float, HydrostaticData]:
        """
        Calculate complete flotation state
        计算完整的浮态
        
        Args:
            loading_condition: Loading condition with all weights
            lpp: Length between perpendiculars (m)
            
        Returns:
            Tuple of (mean_draft, trim, fwd_draft, aft_draft, hydrostatic_data)
            - mean_draft: Mean draft in meters / 平均吃水
            - trim: Trim value in meters (positive = trim by stern) / 纵倾值
            - fwd_draft: Forward draft in meters / 首吃水
            - aft_draft: Aft draft in meters / 尾吃水
            - hydrostatic_data: Hydrostatic parameters at mean draft / 静水力参数
        """
        # Get total displacement
        displacement = loading_condition.total_weight
        
        # Get longitudinal center of gravity from midship
        lcg = loading_condition.lcg
        
        # Initial calculation: get draft from displacement
        mean_draft_initial = self.get_draft_from_displacement(displacement)
        
        # Get hydrostatic data at initial draft
        hydro = self.interpolate_hydrostatic_data(mean_draft_initial)
        
        # Calculate trim moment
        # Trim moment = (LCG - LCB) * Displacement
        trim_moment = (lcg - hydro.lcb) * displacement
        
        # Calculate trim (in cm first, then convert to m)
        # Trim (cm) = Trim Moment / MCT
        if hydro.mct > 0:
            trim_cm = trim_moment / hydro.mct
            trim = trim_cm / 100.0  # Convert to meters
        else:
            trim = 0.0
        
        # Calculate draft corrections at FP and AP
        # LCF is the position where trim pivots
        # Distance from midship to FP and AP
        lcf_to_fp = lpp / 2.0 - hydro.lcf
        lcf_to_ap = -lpp / 2.0 - hydro.lcf
        
        # Draft change = trim * distance / lpp
        fwd_draft = mean_draft_initial + trim * lcf_to_fp / lpp
        aft_draft = mean_draft_initial + trim * lcf_to_ap / lpp
        
        # Recalculate mean draft (should be very close to initial)
        mean_draft = (fwd_draft + aft_draft) / 2.0
        
        # Get final hydrostatic data
        final_hydro = self.interpolate_hydrostatic_data(mean_draft)
        
        return mean_draft, trim, fwd_draft, aft_draft, final_hydro
    
    def calculate_trim_angle(self, trim: float, lpp: float) -> float:
        """
        Calculate trim angle in degrees
        计算纵倾角（度）
        
        Args:
            trim: Trim value in meters
            lpp: Length between perpendiculars in meters
            
        Returns:
            Trim angle in degrees (positive = trim by stern)
        """
        if lpp == 0:
            return 0.0
        
        # tan(angle) = trim / lpp
        angle_rad = np.arctan(trim / lpp)
        angle_deg = np.degrees(angle_rad)
        
        return angle_deg
