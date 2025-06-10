# docy_search/database/connection_manager.py
"""MCP SQLite Server connection management - No credentials needed!"""
import sqlite3
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
        """Initialize SQLite database with required tables"""
        db_path = MCPSQLiteConnection.get_sqlite_db_path()

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Chat history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    model_used TEXT,
                    tools_used TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    memory_id TEXT,
                    cost REAL DEFAULT 0.0
                )
            """)

            # Memory entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    status TEXT DEFAULT 'active',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Activity log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT,
                    metadata TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()
            print(f"✅ SQLite database initialized at: {db_path}")


# Backward compatibility alias
MCPSQLConnection = MCPSQLiteConnection