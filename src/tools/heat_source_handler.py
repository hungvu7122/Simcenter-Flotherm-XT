"""
Heat Source Handler
Manages heat source configuration in simulations
"""
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
from src.flotherm.simulation import HeatSource, FlothermSimulation

logger = setup_logger(__name__)

class HeatSourceHandler:
    """Handler for heat source configuration"""
    
    def __init__(self):
        self.heat_sources: Dict[str, HeatSource] = {}
        logger.info("Initialized HeatSourceHandler")
    
    def configure_heat_source(
        self,
        source_name: str,
        power_watts: float,
        location: Dict[str, float],
        source_type: str = "point_source"
    ) -> Dict[str, Any]:
        """
        Configure a heat source for simulation
        
        Args:
            source_name: Name of the heat source
            power_watts: Power dissipation in watts
            location: Location coordinates {x, y, z}
            source_type: Type of source (point_source, planar_source, volumetric_source)
        
        Returns:
            Confirmation with heat source properties
        """
        try:
            # Validate location
            if not all(key in location for key in ['x', 'y', 'z']):
                return {
                    "status": "error",
                    "message": "Location must contain x, y, z coordinates"
                }
            
            heat_source = HeatSource(
                name=source_name,
                power_watts=power_watts,
                location=location,
                type=source_type
            )
            self.heat_sources[source_name] = heat_source
            logger.info(f"Heat source configured: {source_name} ({power_watts}W)")
            
            return {
                "status": "success",
                "message": f"Heat source '{source_name}' configured successfully",
                "heat_source": {
                    "name": heat_source.name,
                    "power_watts": heat_source.power_watts,
                    "location": heat_source.location,
                    "type": heat_source.type
                }
            }
        except Exception as e:
            logger.error(f"Error configuring heat source: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_heat_source(self, source_name: str) -> Dict[str, Any]:
        """Retrieve heat source properties"""
        source = self.heat_sources.get(source_name)
        if not source:
            return {"status": "error", "message": f"Heat source '{source_name}' not found"}
        
        return {
            "status": "success",
            "heat_source": {
                "name": source.name,
                "power_watts": source.power_watts,
                "location": source.location,
                "type": source.type
            }
        }
    
    def list_heat_sources(self) -> Dict[str, Any]:
        """List all configured heat sources"""
        sources_list = [
            {
                "name": hs.name,
                "power_watts": hs.power_watts,
                "location": hs.location,
                "type": hs.type
            }
            for hs in self.heat_sources.values()
        ]
        total_power = sum(hs.power_watts for hs in self.heat_sources.values())
        return {
            "status": "success",
            "count": len(sources_list),
            "total_power_watts": total_power,
            "heat_sources": sources_list
        }
