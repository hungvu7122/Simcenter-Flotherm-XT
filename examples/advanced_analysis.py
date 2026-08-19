"""
Example: Advanced Simulation Analysis
Demonstrates analysis capabilities
"""
import json
from src.server import MCPServer

def example_advanced_analysis():
    """Example of analyzing simulation results"""
    
    # Initialize server
    server = MCPServer()
    
    print("=" * 60)
    print("Example: Advanced Simulation Analysis")
    print("=" * 60)
    
    # Assume we have a completed simulation
    simulation_id = "sim_thermal_001"
    
    print(f"\n1. Reading simulation results for {simulation_id}...")
    result = server.call_tool(
        "read_simulation_results",
        simulation_id=simulation_id,
        result_type="temperature_field"
    )
    print(json.dumps(result, indent=2))
    
    print(f"\n2. Getting temperature summary...")
    result = server.call_tool(
        "get_temperature_summary",
        simulation_id=simulation_id
    )
    print(json.dumps(result, indent=2))
    
    print(f"\n3. Analyzing results with AI...")
    result = server.call_tool(
        "analyze_results",
        simulation_id=simulation_id,
        analysis_type="thermal_hotspots"
    )
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)

if __name__ == "__main__":
    example_advanced_analysis()
