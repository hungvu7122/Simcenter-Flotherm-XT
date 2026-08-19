"""
Device Power Handler
Manages device power consumption configuration
"""
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
from src.flotherm.simulation import Device, FlothermSimulation

logger = setup_logger(__name__)

class DevicePowerHandler:
    """Handler for device power configuration"""
    
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        logger.info("Initialized DevicePowerHandler")
    
    def set_device_power(
        self,
        device_name: str,
        power_watts: float,
        efficiency: float = 0.85,
        location: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Set device power consumption
        
        Args:
            device_name: Name of the device
            power_watts: Power consumption in watts
            efficiency: Device efficiency (0-1)
            location: Optional location coordinates {x, y, z}
        
        Returns:
            Confirmation with device properties
        """
        try:
            # Validate efficiency
            if not (0 <= efficiency <= 1):
                return {
                    "status": "error",
                    "message": "Efficiency must be between 0 and 1"
                }
            
            device = Device(
                name=device_name,
                power_watts=power_watts,
                efficiency=efficiency,
                location=location
            )
            self.devices[device_name] = device
            
            # Calculate heat dissipation
            heat_dissipation = power_watts * (1 - efficiency)
            
            logger.info(f"Device configured: {device_name} ({power_watts}W, efficiency={efficiency})")
            
            return {
                "status": "success",
                "message": f"Device '{device_name}' configured successfully",
                "device": {
                    "name": device.name,
                    "power_watts": device.power_watts,
                    "efficiency": device.efficiency,
                    "heat_dissipation_watts": heat_dissipation,
                    "location": device.location
                }
            }
        except Exception as e:
            logger.error(f"Error setting device power: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_device(self, device_name: str) -> Dict[str, Any]:
        """Retrieve device properties"""
        device = self.devices.get(device_name)
        if not device:
            return {"status": "error", "message": f"Device '{device_name}' not found"}
        
        heat_dissipation = device.power_watts * (1 - device.efficiency)
        
        return {
            "status": "success",
            "device": {
                "name": device.name,
                "power_watts": device.power_watts,
                "efficiency": device.efficiency,
                "heat_dissipation_watts": heat_dissipation,
                "location": device.location
            }
        }
    
    def list_devices(self) -> Dict[str, Any]:
        """List all configured devices"""
        devices_list = []
        total_power = 0
        total_heat = 0
        
        for device in self.devices.values():
            heat_dissipation = device.power_watts * (1 - device.efficiency)
            devices_list.append({
                "name": device.name,
                "power_watts": device.power_watts,
                "efficiency": device.efficiency,
                "heat_dissipation_watts": heat_dissipation,
                "location": device.location
            })
            total_power += device.power_watts
            total_heat += heat_dissipation
        
        return {
            "status": "success",
            "count": len(devices_list),
            "total_power_watts": total_power,
            "total_heat_dissipation_watts": total_heat,
            "devices": devices_list
        }
