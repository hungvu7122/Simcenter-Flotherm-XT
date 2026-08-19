"""
Configuration management for Flotherm MCP Server
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flotherm Configuration
    FLOTHERM_INSTALL_PATH = os.getenv(
        "FLOTHERM_INSTALL_PATH",
        r"C:\Program Files\Siemens\Simcenter\Flotherm"
    )
    FLOTHERM_API_PORT = int(os.getenv("FLOTHERM_API_PORT", 8080))
    FLOTHERM_TIMEOUT = int(os.getenv("FLOTHERM_TIMEOUT", 300))
    
    # Claude AI Configuration
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
    CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-opus-20240229")
    
    # MCP Server Configuration
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 3000))
    MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "127.0.0.1")
    
    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/flotherm_mcp.log")
    
    # Simulation Configuration
    SIMULATION_TIMEOUT = int(os.getenv("SIMULATION_TIMEOUT", 600))
    RESULTS_CACHE_DIR = os.getenv("RESULTS_CACHE_DIR", "./results_cache")
    TEMP_DIR = os.getenv("TEMP_DIR", "./temp")
    
    # Create necessary directories
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        Path(cls.RESULTS_CACHE_DIR).mkdir(parents=True, exist_ok=True)
        Path(cls.TEMP_DIR).mkdir(parents=True, exist_ok=True)
        Path(Path(cls.LOG_FILE).parent).mkdir(parents=True, exist_ok=True)

# Initialize directories on import
Config.ensure_directories()
