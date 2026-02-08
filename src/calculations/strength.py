"""
Strength calculation module for semi-submersible ship loading computer.
强度计算模块
"""

import numpy as np
from typing import List, Tuple
from ..models import LoadingCondition, Compartment, Cargo


class StrengthCalculator:
    """
    强度计算器 / Strength Calculator
    
    Calculates:
    - Shear force distribution / 剪力分布
    - Bending moment distribution / 弯矩分布
    """
    
    def __init__(self, lpp: float, num_stations: int = 21):
        """
        Initialize strength calculator
        
        Args:
            lpp: Length between perpendiculars in meters
            num_stations: Number of calculation stations along the ship
        """
        self.lpp = lpp
        self.num_stations = num_stations
        # Stations from AP (0) to FP (lpp)
        self.stations = np.linspace(-lpp/2, lpp/2, num_stations)
    
    def distribute_weight_along_length(self, 
                                      loading_condition: LoadingCondition,
                                      buoyancy_distribution: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Distribute weight and buoyancy along ship length
        沿船长分布重量和浮力
        
        Args:
            loading_condition: Loading condition with all weights
            buoyancy_distribution: Optional buoyancy distribution (if None, assumes uniform)
            
        Returns:
            Tuple of (weight_distribution, buoyancy_distribution)
            Both are arrays of forces per unit length at each station
        """
        weight_dist = np.zeros(self.num_stations)
        
        # Distribute lightship weight (assumed uniform or concentrated at LCG)
        if loading_condition.ship_params:
            lightship_weight = loading_condition.ship_params.lightship_weight
            lightship_lcg = loading_condition.ship_params.lightship_lcg
            
            # Find nearest station to lightship LCG
            station_idx = np.argmin(np.abs(self.stations - lightship_lcg))
            weight_dist[station_idx] += lightship_weight
        
        # Distribute compartment weights
        for comp in loading_condition.compartments:
            if comp.weight > 0:
                station_idx = np.argmin(np.abs(self.stations - comp.lcg))
                weight_dist[station_idx] += comp.weight
        
        # Distribute cargo weights
        for cargo in loading_condition.cargos:
            if cargo.weight > 0:
                station_idx = np.argmin(np.abs(self.stations - cargo.lcg))
                weight_dist[station_idx] += cargo.weight
        
        # Calculate buoyancy distribution
        if buoyancy_distribution is None:
            # Simplified: uniform distribution equal to total displacement
            total_displacement = loading_condition.total_weight
            buoy_dist = np.ones(self.num_stations) * (total_displacement / self.num_stations)
        else:
            buoy_dist = buoyancy_distribution
        
        return weight_dist, buoy_dist
    
    def calculate_shear_force(self, 
                            weight_distribution: np.ndarray,
                            buoyancy_distribution: np.ndarray) -> np.ndarray:
        """
        Calculate shear force distribution
        计算剪力分布
        
        Shear force at a station = integral of (buoyancy - weight) from AP to that station
        
        Args:
            weight_distribution: Weight per station
            buoyancy_distribution: Buoyancy per station
            
        Returns:
            Array of shear forces at each station (in tonnes)
        """
        # Net load = buoyancy - weight
        net_load = buoyancy_distribution - weight_distribution
        
        # Shear force is cumulative sum of net load from AP
        shear_force = np.cumsum(net_load)
        
        return shear_force
    
    def calculate_bending_moment(self, 
                                shear_force: np.ndarray) -> np.ndarray:
        """
        Calculate bending moment distribution
        计算弯矩分布
        
        Bending moment = integral of shear force
        
        Args:
            shear_force: Shear force distribution
            
        Returns:
            Array of bending moments at each station (in tonne-meters)
        """
        # Station spacing
        dx = self.lpp / (self.num_stations - 1)
        
        # Bending moment is integral of shear force
        # Using trapezoidal integration
        bending_moment = np.zeros(self.num_stations)
        
        for i in range(1, self.num_stations):
            # Trapezoidal rule: area = (f1 + f2) * dx / 2
            bending_moment[i] = bending_moment[i-1] + \
                               (shear_force[i-1] + shear_force[i]) * dx / 2
        
        return bending_moment
    
    def calculate_strength(self, 
                          loading_condition: LoadingCondition,
                          buoyancy_distribution: np.ndarray = None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Complete strength calculation
        完整强度计算
        
        Args:
            loading_condition: Loading condition
            buoyancy_distribution: Optional custom buoyancy distribution
            
        Returns:
            Tuple of (stations, shear_force, bending_moment)
            - stations: Position along ship (m, from midship)
            - shear_force: Shear force at each station (t)
            - bending_moment: Bending moment at each station (t·m)
        """
        # Distribute weights and buoyancy
        weight_dist, buoy_dist = self.distribute_weight_along_length(
            loading_condition,
            buoyancy_distribution
        )
        
        # Calculate shear force
        shear_force = self.calculate_shear_force(weight_dist, buoy_dist)
        
        # Calculate bending moment
        bending_moment = self.calculate_bending_moment(shear_force)
        
        return self.stations.copy(), shear_force, bending_moment
    
    def get_max_values(self, 
                      shear_force: np.ndarray,
                      bending_moment: np.ndarray) -> Tuple[float, float, float, float]:
        """
        Get maximum shear force and bending moment values
        获取最大剪力和弯矩值
        
        Args:
            shear_force: Shear force distribution
            bending_moment: Bending moment distribution
            
        Returns:
            Tuple of (max_sf, min_sf, max_bm, min_bm)
        """
        max_sf = np.max(shear_force)
        min_sf = np.min(shear_force)
        max_bm = np.max(bending_moment)
        min_bm = np.min(bending_moment)
        
        return max_sf, min_sf, max_bm, min_bm
