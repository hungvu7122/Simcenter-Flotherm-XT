"""
Flotherm API Client for direct interaction with Simcenter Flotherm
"""
import requests
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
from src.utils.config import Config

logger = setup_logger(__name__)

class FlothermAPIClient:
    """Client for communicating with Flotherm via REST API"""
    
    def __init__(self, base_url: Optional[str] = None):
        """
        Initialize Flotherm API Client
        
        Args:
            base_url: Base URL for Flotherm API (default: localhost:port)
        """
        self.base_url = base_url or f"http://localhost:{Config.FLOTHERM_API_PORT}"
        self.timeout = Config.FLOTHERM_TIMEOUT
        logger.info(f"Initialized FlothermAPIClient with base_url: {self.base_url}")
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Flotherm API
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
        
        Returns:
            Response JSON
        """
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = requests.get(url, params=params, timeout=self.timeout)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, params=params, timeout=self.timeout)
            elif method.upper() == "DELETE":
                response = requests.delete(url, params=params, timeout=self.timeout)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            raise
    
    def get_simulation_status(self, simulation_id: str) -> Dict[str, Any]:
        """Get status of a simulation"""
        return self._make_request("GET", f"/simulations/{simulation_id}/status")
    
    def start_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """Start a simulation"""
        return self._make_request("POST", f"/simulations/{simulation_id}/start")
    
    def stop_simulation(self, simulation_id: str) -> Dict[str, Any]:
        """Stop a running simulation"""
        return self._make_request("POST", f"/simulations/{simulation_id}/stop")
    
    def get_simulation_results(self, simulation_id: str) -> Dict[str, Any]:
        """Get results from a completed simulation"""
        return self._make_request("GET", f"/simulations/{simulation_id}/results")
    
    def create_simulation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new simulation with given configuration"""
        return self._make_request("POST", "/simulations", data=config)
    
    def update_simulation(self, simulation_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update simulation configuration"""
        return self._make_request("PUT", f"/simulations/{simulation_id}", data=config)
    
    def list_simulations(self) -> List[Dict[str, Any]]:
        """List all simulations"""
        response = self._make_request("GET", "/simulations")
        return response.get("simulations", [])
