# docy_search/database/__init__.py
"""Database query module for natural language SQL with SQLite support"""

try:
    from .sql_agent import SQLAgent, run_sql_query
    from .connection_manager import MCPSQLiteConnection, MCPSQLConnection
    from .db_manager import DatabaseManager, get_db_manager
except ImportError:
    # Fallback to simple version if real SQL agent fails to import
    from .sql_agent_simple import SQLAgent, run_sql_query
    from .connection_manager import MCPSQLiteConnection
    from .db_manager import get_db_manager
    MCPSQLConnection = MCPSQLiteConnection
    DatabaseManager = None

__all__ = ['SQLAgent', 'run_sql_query', 'MCPSQLConnection', 'MCPSQLiteConnection', 
           'DatabaseManager', 'get_db_manager']