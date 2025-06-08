# docy_search/database/connection_manager.py
"""MCP SQL Server connection management"""
import os
from typing import Optional, Dict, Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv

load_dotenv()


class MCPSQLConnection:
    """Manages MCP SQL server connections"""
    
    @staticmethod
    def get_server_params() -> StdioServerParameters:
        """Get MCP SQL server parameters from environment"""
        required_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing database environment variables: {', '.join(missing)}")
        
        return StdioServerParameters(
            command="uvx",
            args=[
                "mcp-sql-server",
                "--db-host", os.getenv("DB_HOST"),
                "--db-user", os.getenv("DB_USER"),
                "--db-password", os.getenv("DB_PASSWORD"),
                "--db-database", os.getenv("DB_NAME"),
            ],
        )
    
    @staticmethod
    async def create_session():
        """Create MCP client session context manager"""
        params = MCPSQLConnection.get_server_params()
        return stdio_client(params)