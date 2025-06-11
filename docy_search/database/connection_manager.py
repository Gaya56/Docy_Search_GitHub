# docy_search/database/connection_manager.py
"""MCP SQLite Server connection management - No credentials needed!"""
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from pathlib import Path


class MCPSQLiteConnection:
    """Manages MCP SQLite server connections - credential-free"""

    @staticmethod
    def get_sqlite_db_path() -> str:
        """Get SQLite database path"""
        project_root = Path(__file__).parent.parent.parent
        db_path = project_root / "docy_search.db"
        return str(db_path)

    @staticmethod
    def get_server_params() -> StdioServerParameters:
        """Get MCP SQLite server parameters - no credentials required"""
        db_path = MCPSQLiteConnection.get_sqlite_db_path()

        return StdioServerParameters(
            command="uvx",
            args=[
                "mcp-server-sqlite",
                "--db-path", db_path
            ],
        )

    @staticmethod
    async def create_session():
        """Create MCP client session context manager"""
        params = MCPSQLiteConnection.get_server_params()
        return stdio_client(params)

    @staticmethod
    def initialize_database():
        """Initialize SQLite database - delegates to DatabaseManager"""
        from .db_manager import get_db_manager
        db_manager = get_db_manager()
        print(f"✅ SQLite database initialized at: {db_manager.db_path}")


# Backward compatibility alias
MCPSQLConnection = MCPSQLiteConnection