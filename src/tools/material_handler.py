"""
Material Properties Handler
Manages material thermal properties configuration
"""
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
from src.flotherm.simulation import Material, FlothermSimulation

logger = setup_logger(__name__)

class MaterialHandler:
    """Handler for material property configuration"""
    
    def __init__(self):
        self.materials: Dict[str, Material] = {}
        logger.info("Initialized MaterialHandler")
    
    def setup_material_properties(
        self,
        material_name: str,
        thermal_conductivity: float,
        density: float,
        specific_heat: float,
        emissivity: float = 0.5
    ) -> Dict[str, Any]:
        """
        Setup material properties for simulation
        
        Args:
            material_name: Name of the material
            thermal_conductivity: W/(m·K)
            density: kg/m³
            specific_heat: J/(kg·K)
            emissivity: Thermal emissivity (0-1)
        
        Returns:
            Confirmation with material properties
        """
        try:
            material = Material(
                name=material_name,
                thermal_conductivity=thermal_conductivity,
                density=density,
                specific_heat=specific_heat,
                emissivity=emissivity
            )
            self.materials[material_name] = material
            logger.info(f"Material configured: {material_name}")
            
            return {
                "status": "success",
                "message": f"Material '{material_name}' configured successfully",
                "material": {
                    "name": material.name,
                    "thermal_conductivity": material.thermal_conductivity,
                    "density": material.density,
                    "specific_heat": material.specific_heat,
                    "emissivity": material.emissivity
                }
            }
        except Exception as e:
            logger.error(f"Error setting up material: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_material(self, material_name: str) -> Dict[str, Any]:
        """Retrieve material properties"""
        material = self.materials.get(material_name)
        if not material:
            return {"status": "error", "message": f"Material '{material_name}' not found"}
        
        return {
            "status": "success",
            "material": {
                "name": material.name,
                "thermal_conductivity": material.thermal_conductivity,
                "density": material.density,
                "specific_heat": material.specific_heat,
                "emissivity": material.emissivity
            }
        }
    
    def list_materials(self) -> Dict[str, Any]:
        """List all configured materials"""
        materials_list = [
            {
                "name": m.name,
                "thermal_conductivity": m.thermal_conductivity,
                "density": m.density,
                "specific_heat": m.specific_heat,
                "emissivity": m.emissivity
            }
            for m in self.materials.values()
        ]
        return {
            "status": "success",
            "count": len(materials_list),
            "materials": materials_list
        }
