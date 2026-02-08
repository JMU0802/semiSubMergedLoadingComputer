"""
Data models for the semi-submersible ship loading computer.
船舶装载计算数据模型
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class CompartmentType(Enum):
    """舱室类型 / Compartment Type"""
    BALLAST = "压载舱"  # Ballast tank
    FUEL = "燃油舱"  # Fuel tank
    FRESH_WATER = "淡水舱"  # Fresh water tank
    CARGO = "货舱"  # Cargo hold


@dataclass
class Compartment:
    """
    舱室数据模型 / Compartment Data Model
    """
    name: str  # 舱室名称
    type: CompartmentType  # 舱室类型
    capacity: float  # 容积 (m³)
    lcg: float  # 纵向重心 (m, 从船中计)
    tcg: float  # 横向重心 (m, 从中线计)
    vcg: float  # 垂向重心 (m, 从基线计)
    density: float = 1.025  # 液体密度 (t/m³)
    fill_percentage: float = 0.0  # 装载百分比 (0-100)
    fsm: float = 0.0  # 自由液面力矩 (t·m)
    
    @property
    def weight(self) -> float:
        """计算舱室重量 / Calculate compartment weight"""
        return self.capacity * (self.fill_percentage / 100.0) * self.density
    
    @property
    def moment_lcg(self) -> float:
        """纵向力矩 / Longitudinal moment"""
        return self.weight * self.lcg
    
    @property
    def moment_tcg(self) -> float:
        """横向力矩 / Transverse moment"""
        return self.weight * self.tcg
    
    @property
    def moment_vcg(self) -> float:
        """垂向力矩 / Vertical moment"""
        return self.weight * self.vcg


@dataclass
class Cargo:
    """
    货物数据模型 / Cargo Data Model
    """
    name: str  # 货物名称
    weight: float  # 重量 (t)
    lcg: float  # 纵向重心 (m)
    tcg: float  # 横向重心 (m)
    vcg: float  # 垂向重心 (m)
    
    @property
    def moment_lcg(self) -> float:
        """纵向力矩"""
        return self.weight * self.lcg
    
    @property
    def moment_tcg(self) -> float:
        """横向力矩"""
        return self.weight * self.tcg
    
    @property
    def moment_vcg(self) -> float:
        """垂向力矩"""
        return self.weight * self.vcg


@dataclass
class ShipParameters:
    """
    船舶基本参数 / Ship Basic Parameters
    """
    loa: float  # 总长 (m) - Length overall
    lpp: float  # 垂线间长 (m) - Length between perpendiculars
    breadth: float  # 型宽 (m) - Breadth
    depth: float  # 型深 (m) - Depth
    lightship_weight: float  # 空船重量 (t)
    lightship_lcg: float  # 空船纵向重心 (m)
    lightship_tcg: float  # 空船横向重心 (m)
    lightship_vcg: float  # 空船垂向重心 (m)
    design_draft: float  # 设计吃水 (m)


@dataclass
class LoadingCondition:
    """
    装载工况 / Loading Condition
    """
    name: str  # 工况名称
    description: str = ""  # 工况描述
    ship_params: ShipParameters = None  # 船舶参数
    compartments: List[Compartment] = field(default_factory=list)  # 舱室列表
    cargos: List[Cargo] = field(default_factory=list)  # 货物列表
    
    @property
    def total_weight(self) -> float:
        """总重量 / Total weight"""
        weight = self.ship_params.lightship_weight if self.ship_params else 0
        weight += sum(c.weight for c in self.compartments)
        weight += sum(c.weight for c in self.cargos)
        return weight
    
    @property
    def lcg(self) -> float:
        """纵向重心 / Longitudinal center of gravity"""
        if self.total_weight == 0:
            return 0
        
        moment = 0
        if self.ship_params:
            moment += self.ship_params.lightship_weight * self.ship_params.lightship_lcg
        moment += sum(c.moment_lcg for c in self.compartments)
        moment += sum(c.moment_lcg for c in self.cargos)
        
        return moment / self.total_weight
    
    @property
    def tcg(self) -> float:
        """横向重心 / Transverse center of gravity"""
        if self.total_weight == 0:
            return 0
        
        moment = 0
        if self.ship_params:
            moment += self.ship_params.lightship_weight * self.ship_params.lightship_tcg
        moment += sum(c.moment_tcg for c in self.compartments)
        moment += sum(c.moment_tcg for c in self.cargos)
        
        return moment / self.total_weight
    
    @property
    def vcg(self) -> float:
        """垂向重心 / Vertical center of gravity"""
        if self.total_weight == 0:
            return 0
        
        moment = 0
        if self.ship_params:
            moment += self.ship_params.lightship_weight * self.ship_params.lightship_vcg
        moment += sum(c.moment_vcg for c in self.compartments)
        moment += sum(c.moment_vcg for c in self.cargos)
        
        return moment / self.total_weight
    
    @property
    def total_fsm(self) -> float:
        """总自由液面力矩 / Total free surface moment"""
        return sum(c.fsm for c in self.compartments if c.fill_percentage > 0 and c.fill_percentage < 100)


@dataclass
class HydrostaticData:
    """
    静水力数据 / Hydrostatic Data
    """
    draft: float  # 吃水 (m)
    displacement: float  # 排水量 (t)
    lcb: float  # 浮心纵向位置 (m)
    vcb: float  # 浮心垂向位置 (m)
    lcf: float  # 漂心纵向位置 (m)
    tpc: float  # 每厘米吃水吨数 (t/cm)
    mct: float  # 纵倾力矩 (t·m/cm)
    kb: float  # 基线到浮心 (m)
    bm: float  # 浮心到稳心 (m)
    gmt: float  # 初稳性高 (m)
    bmt: float  # 横稳心半径 (m)
    waterplane_area: float = 0.0  # 水线面面积 (m²)
