"""
MCP Server Implementation
Main server that handles MCP protocol and tool registration
"""
import json
from typing import Any, Dict, List, Callable, Optional
from src.utils.logger import setup_logger
from src.tools.material_handler import MaterialHandler
from src.tools.heat_source_handler import HeatSourceHandler
from src.tools.device_power_handler import DevicePowerHandler
from src.tools.results_reader import ResultsReader
from src.tools.analysis_engine import AnalysisEngine

logger = setup_logger(__name__)

class MCPServer:
    """Model Context Protocol Server for Flotherm-Claude Integration"""
    
    def __init__(self):
        """Initialize MCP Server with all handlers"""
        self.material_handler = MaterialHandler()
        self.heat_source_handler = HeatSourceHandler()
        self.device_power_handler = DevicePowerHandler()
        self.results_reader = ResultsReader()
        self.analysis_engine = AnalysisEngine()
        
        self.tools: Dict[str, Dict[str, Any]] = {}
        self._register_tools()
        logger.info("MCP Server initialized")
    
    def _register_tools(self) -> None:
        """Register all available tools"""
        # Material tools
        self.tools["setup_material_properties"] = {
            "description": "Setup thermal properties for a material",
            "handler": self.material_handler.setup_material_properties,
            "parameters": {
                "material_name": {"type": "string", "description": "Name of the material"},
                "thermal_conductivity": {"type": "number", "description": "Thermal conductivity in W/(m·K)"},
                "density": {"type": "number", "description": "Density in kg/m³"},
                "specific_heat": {"type": "number", "description": "Specific heat in J/(kg·K)"},
                "emissivity": {"type": "number", "description": "Thermal emissivity (0-1)", "default": 0.5}
            }
        }
        
        self.tools["get_material"] = {
            "description": "Retrieve material properties",
            "handler": self.material_handler.get_material,
            "parameters": {
                "material_name": {"type": "string", "description": "Name of the material"}
            }
        }
        
        self.tools["list_materials"] = {
            "description": "List all configured materials",
            "handler": self.material_handler.list_materials,
            "parameters": {}
        }
        
        # Heat source tools
        self.tools["configure_heat_source"] = {
            "description": "Configure a heat source in the simulation",
            "handler": self.heat_source_handler.configure_heat_source,
            "parameters": {
                "source_name": {"type": "string", "description": "Name of the heat source"},
                "power_watts": {"type": "number", "description": "Power dissipation in watts"},
                "location": {"type": "object", "description": "Location coordinates {x, y, z}"},
                "source_type": {"type": "string", "description": "Type of source", "default": "point_source"}
            }
        }
        
        self.tools["get_heat_source"] = {
            "description": "Get heat source properties",
            "handler": self.heat_source_handler.get_heat_source,
            "parameters": {
                "source_name": {"type": "string", "description": "Name of the heat source"}
            }
        }
        
        self.tools["list_heat_sources"] = {
            "description": "List all configured heat sources",
            "handler": self.heat_source_handler.list_heat_sources,
            "parameters": {}
        }
        
        # Device power tools
        self.tools["set_device_power"] = {
            "description": "Set device power consumption",
            "handler": self.device_power_handler.set_device_power,
            "parameters": {
                "device_name": {"type": "string", "description": "Name of the device"},
                "power_watts": {"type": "number", "description": "Power consumption in watts"},
                "efficiency": {"type": "number", "description": "Device efficiency (0-1)", "default": 0.85},
                "location": {"type": "object", "description": "Location coordinates {x, y, z}"}
            }
        }
        
        self.tools["get_device"] = {
            "description": "Get device properties",
            "handler": self.device_power_handler.get_device,
            "parameters": {
                "device_name": {"type": "string", "description": "Name of the device"}
            }
        }
        
        self.tools["list_devices"] = {
            "description": "List all configured devices",
            "handler": self.device_power_handler.list_devices,
            "parameters": {}
        }
        
        # Results tools
        self.tools["read_simulation_results"] = {
            "description": "Read simulation results from Flotherm",
            "handler": self.results_reader.read_simulation_results,
            "parameters": {
                "simulation_id": {"type": "string", "description": "Simulation identifier"},
                "result_type": {"type": "string", "description": "Type of result", "default": "temperature_field"}
            }
        }
        
        self.tools["get_temperature_summary"] = {
            "description": "Get temperature summary from simulation",
            "handler": self.results_reader.get_temperature_summary,
            "parameters": {
                "simulation_id": {"type": "string", "description": "Simulation identifier"}
            }
        }
        
        # Analysis tools
        self.tools["analyze_results"] = {
            "description": "Analyze simulation results using AI",
            "handler": self.analysis_engine.analyze_results,
            "parameters": {
                "simulation_id": {"type": "string", "description": "Simulation identifier"},
                "analysis_type": {"type": "string", "description": "Type of analysis", "default": "thermal_hotspots"}
            }
        }
        
        logger.info(f"Registered {len(self.tools)} tools")
    
    def get_tools_list(self) -> List[Dict[str, Any]]:
        """Get list of available tools for MCP protocol"""
        return [
            {
                "name": tool_name,
                "description": tool_info["description"],
                "parameters": tool_info["parameters"]
            }
            for tool_name, tool_info in self.tools.items()
        ]
    
    def call_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """Call a registered tool"""
        if tool_name not in self.tools:
            return {
                "status": "error",
                "message": f"Tool '{tool_name}' not found"
            }
        
        try:
            handler = self.tools[tool_name]["handler"]
            result = handler(**kwargs)
            logger.info(f"Tool called: {tool_name} - Status: {result.get('status', 'unknown')}")
            return result
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
