"""
Example: Basic Flotherm Simulation Setup
Demonstrates how to use the MCP Server tools
"""
import json
from src.server import MCPServer

def example_basic_simulation():
    """Example of setting up a basic simulation"""
    
    # Initialize server
    server = MCPServer()
    
    print("=" * 60)
    print("Example: Basic Thermal Simulation Setup")
    print("=" * 60)
    
    # Step 1: Setup materials
    print("\n1. Setting up materials...")
    result = server.call_tool(
        "setup_material_properties",
        material_name="Copper",
        thermal_conductivity=400,
        density=8960,
        specific_heat=385
    )
    print(json.dumps(result, indent=2))
    
    # Step 2: Configure heat sources
    print("\n2. Configuring heat sources...")
    result = server.call_tool(
        "configure_heat_source",
        source_name="CPU",
        power_watts=65.5,
        location={"x": 50, "y": 50, "z": 10}
    )
    print(json.dumps(result, indent=2))
    
    result = server.call_tool(
        "configure_heat_source",
        source_name="GPU",
        power_watts=150.0,
        location={"x": 50, "y": 100, "z": 10}
    )
    print(json.dumps(result, indent=2))
    
    # Step 3: Set device power
    print("\n3. Setting device power consumption...")
    result = server.call_tool(
        "set_device_power",
        device_name="LED Array",
        power_watts=120.0,
        efficiency=0.85
    )
    print(json.dumps(result, indent=2))
    
    # Step 4: List configured elements
    print("\n4. Listing configured elements...")
    
    print("\nMaterials:")
    result = server.call_tool("list_materials")
    print(json.dumps(result, indent=2))
    
    print("\nHeat Sources:")
    result = server.call_tool("list_heat_sources")
    print(json.dumps(result, indent=2))
    
    print("\nDevices:")
    result = server.call_tool("list_devices")
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)

if __name__ == "__main__":
    example_basic_simulation()
