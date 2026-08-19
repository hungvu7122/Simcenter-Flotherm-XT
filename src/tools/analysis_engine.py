"""
Analysis Engine
AI-powered analysis of simulation results
"""
from typing import Dict, Any, Optional, List
from src.utils.logger import setup_logger
from src.utils.config import Config
import anthropic
import json
from pathlib import Path

logger = setup_logger(__name__)

class AnalysisEngine:
    """Engine for AI-powered analysis of simulation results"""
    
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=Config.CLAUDE_API_KEY)
        self.model = Config.CLAUDE_MODEL
        logger.info("Initialized AnalysisEngine")
    
    def analyze_results(
        self,
        simulation_id: str,
        analysis_type: str = "thermal_hotspots"
    ) -> Dict[str, Any]:
        """
        Analyze simulation results using Claude AI
        
        Args:
            simulation_id: Simulation identifier
            analysis_type: Type of analysis (thermal_hotspots, performance, etc.)
        
        Returns:
            Analysis results and recommendations
        """
        try:
            # Read simulation results
            results_path = Path(Config.RESULTS_CACHE_DIR) / f"{simulation_id}_temperature_field.json"
            
            if not results_path.exists():
                return {
                    "status": "error",
                    "message": f"No results found for simulation {simulation_id}"
                }
            
            with open(results_path, 'r') as f:
                results = json.load(f)
            
            # Prepare analysis prompt
            prompt = self._prepare_analysis_prompt(analysis_type, results)
            
            # Call Claude API
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            analysis_text = message.content[0].text
            logger.info(f"Analysis completed for simulation {simulation_id}")
            
            return {
                "status": "success",
                "simulation_id": simulation_id,
                "analysis_type": analysis_type,
                "analysis": analysis_text,
                "model_used": self.model
            }
        except Exception as e:
            logger.error(f"Error analyzing results: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def _prepare_analysis_prompt(self, analysis_type: str, results: Dict[str, Any]) -> str:
        """
        Prepare analysis prompt for Claude
        
        Args:
            analysis_type: Type of analysis
            results: Simulation results data
        
        Returns:
            Analysis prompt
        """
        if analysis_type == "thermal_hotspots":
            return f"""
Analyze the following thermal simulation results and identify thermal hotspots and potential issues:

Simulation Results:
{json.dumps(results, indent=2)}

Please provide:
1. Identified hotspots (locations with high temperatures)
2. Potential thermal issues or bottlenecks
3. Recommendations for thermal management improvements
4. Risk assessment for equipment reliability
"""
        elif analysis_type == "performance":
            return f"""
Analyze the following thermal simulation results for thermal performance:

Simulation Results:
{json.dumps(results, indent=2)}

Please provide:
1. Overall thermal performance assessment
2. Efficiency metrics
3. Areas for optimization
4. Suggested improvements
"""
        else:
            return f"""
Provide a comprehensive analysis of the following thermal simulation results:

Simulation Results:
{json.dumps(results, indent=2)}
"""
