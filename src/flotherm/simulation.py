"""
Flotherm Simulation management
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from src.utils.logger import setup_logger
from src.flotherm.api_client import FlothermAPIClient

logger = setup_logger(__name__)

@dataclass
class Material:
    """Material properties"""
    name: str
    thermal_conductivity: float  # W/(m·K)
    density: float  # kg/m³
    specific_heat: float  # J/(kg·K)
    emissivity: float = 0.5

@dataclass
class HeatSource:
    """Heat source definition"""
    name: str
    power_watts: float
    location: Dict[str, float]  # {x, y, z} coordinates
    type: str = "point_source"  # point_source, planar_source, volumetric_source

@dataclass
class Device:
    """Device with power consumption"""
    name: str
    power_watts: float
    efficiency: float = 0.85
    location: Optional[Dict[str, float]] = None

class FlothermSimulation:
    """High-level Flotherm simulation management"""
    
    def __init__(self, simulation_id: str, api_client: Optional[FlothermAPIClient] = None):
        """
        Initialize Flotherm Simulation
        
        Args:
            simulation_id: Unique identifier for the simulation
            api_client: FlothermAPIClient instance (created if not provided)
        """
        self.simulation_id = simulation_id
        self.api_client = api_client or FlothermAPIClient()
        self.materials: Dict[str, Material] = {}
        self.heat_sources: Dict[str, HeatSource] = {}
        self.devices: Dict[str, Device] = {}
        logger.info(f"Initialized FlothermSimulation: {simulation_id}")
    
    def add_material(self, material: Material) -> None:
        """Add material to simulation"""
        self.materials[material.name] = material
        logger.info(f"Added material: {material.name}")
    
    def get_material(self, name: str) -> Optional[Material]:
        """Get material by name"""
        return self.materials.get(name)
    
    def list_materials(self) -> List[Material]:
        """List all materials"""
        return list(self.materials.values())
    
    def add_heat_source(self, heat_source: HeatSource) -> None:
        """Add heat source to simulation"""
        self.heat_sources[heat_source.name] = heat_source
        logger.info(f"Added heat source: {heat_source.name} ({heat_source.power_watts}W)")
    
    def get_heat_source(self, name: str) -> Optional[HeatSource]:
        """Get heat source by name"""
        return self.heat_sources.get(name)
    
    def list_heat_sources(self) -> List[HeatSource]:
        """List all heat sources"""
        return list(self.heat_sources.values())
    
    def add_device(self, device: Device) -> None:
        """Add device to simulation"""
        self.devices[device.name] = device
        logger.info(f"Added device: {device.name} ({device.power_watts}W)")
    
    def get_device(self, name: str) -> Optional[Device]:
        """Get device by name"""
        return self.devices.get(name)
    
    def list_devices(self) -> List[Device]:
        """List all devices"""
        return list(self.devices.values())
    
    def get_configuration(self) -> Dict[str, Any]:
        """Get current simulation configuration"""
        return {
            "simulation_id": self.simulation_id,
            "materials": [asdict(m) for m in self.materials.values()],
            "heat_sources": [asdict(hs) for hs in self.heat_sources.values()],
            "devices": [asdict(d) for d in self.devices.values()]
        }
    
    def start(self) -> Dict[str, Any]:
        """Start the simulation"""
        config = self.get_configuration()
        logger.info(f"Starting simulation {self.simulation_id}")
        return self.api_client.start_simulation(self.simulation_id)
    
    def stop(self) -> Dict[str, Any]:
        """Stop the simulation"""
        logger.info(f"Stopping simulation {self.simulation_id}")
        return self.api_client.stop_simulation(self.simulation_id)
    
    def get_status(self) -> Dict[str, Any]:
        """Get simulation status"""
        return self.api_client.get_simulation_status(self.simulation_id)
    
    def get_results(self) -> Dict[str, Any]:
        """Get simulation results"""
        logger.info(f"Retrieving results for simulation {self.simulation_id}")
        return self.api_client.get_simulation_results(self.simulation_id)
    
    def calculate_total_heat_generation(self) -> float:
        """Calculate total heat generation in simulation"""
        total = 0.0
        for source in self.heat_sources.values():
            total += source.power_watts
        for device in self.devices.values():
            total += device.power_watts
        return total
