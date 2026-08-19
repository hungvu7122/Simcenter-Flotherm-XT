"""
Main entry point for Flotherm MCP Server
"""
import json
import sys
from pathlib import Path
from src.server import MCPServer
from src.utils.logger import setup_logger
from src.utils.config import Config

logger = setup_logger(__name__)

def main():
    """Start the MCP Server"""
    try:
        logger.info("Starting Flotherm MCP Server")
        logger.info(f"Configuration: {Config.__dict__}")
        
        # Initialize server
        server = MCPServer()
        
        # Get available tools
        tools = server.get_tools_list()
        logger.info(f"Available tools: {[t['name'] for t in tools]}")
        
        # Example: Print tools list
        print(json.dumps({
            "status": "ready",
            "message": "Flotherm MCP Server is ready",
            "tools_count": len(tools),
            "tools": tools
        }, indent=2))
        
        # Server is ready for MCP connections
        logger.info("Server ready for MCP connections")
        
        # Keep server running
        import time
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Server shutdown requested")
            
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
