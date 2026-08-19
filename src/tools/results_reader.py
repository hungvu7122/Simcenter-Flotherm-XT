"""
Results Reader
Reads and extracts simulation results from Flotherm
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
from src.utils.config import Config

logger = setup_logger(__name__)

class ResultsReader:
    """Handler for reading simulation results"""
    
    def __init__(self):
        logger.info("Initialized ResultsReader")
    
    def read_simulation_results(
        self,
        simulation_id: str,
        result_type: str = "temperature_field"
    ) -> Dict[str, Any]:
        """
        Read simulation results
        
        Args:
            simulation_id: Simulation identifier
            result_type: Type of result (temperature_field, heat_flux, etc.)
        
        Returns:
            Simulation results
        """
        try:
            results_path = Path(Config.RESULTS_CACHE_DIR) / f"{simulation_id}_{result_type}.json"
            
            if not results_path.exists():
                return {
                    "status": "error",
                    "message": f"No results found for simulation {simulation_id}"
                }
            
            with open(results_path, 'r') as f:
                results = json.load(f)
            
            logger.info(f"Results retrieved for simulation {simulation_id}")
            
            return {
                "status": "success",
                "simulation_id": simulation_id,
                "result_type": result_type,
                "results": results
            }
        except Exception as e:
            logger.error(f"Error reading results: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def get_temperature_summary(
        self,
        simulation_id: str
    ) -> Dict[str, Any]:
        """
        Get temperature summary from simulation
        
        Returns:
            Min, max, and average temperatures
        """
        try:
            results_path = Path(Config.RESULTS_CACHE_DIR) / f"{simulation_id}_temperature_field.json"
            
            if not results_path.exists():
                return {
                    "status": "error",
                    "message": f"No temperature data found for simulation {simulation_id}"
                }
            
            with open(results_path, 'r') as f:
                data = json.load(f)
            
            temperatures = data.get('temperatures', [])
            if not temperatures:
                return {"status": "error", "message": "No temperature data available"}
            
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            avg_temp = sum(temperatures) / len(temperatures)
            
            return {
                "status": "success",
                "simulation_id": simulation_id,
                "temperature_summary": {
                    "min_celsius": min_temp,
                    "max_celsius": max_temp,
                    "average_celsius": avg_temp,
                    "data_points": len(temperatures)
                }
            }
        except Exception as e:
            logger.error(f"Error calculating temperature summary: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
