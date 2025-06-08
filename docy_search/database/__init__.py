# docy_search/database/__init__.py
"""Database query module for natural language SQL"""

try:
    from .sql_agent import SQLAgent, run_sql_query
    from .connection_manager import MCPSQLConnection
except ImportError:
    # Fallback to simple version if real SQL agent fails to import
    from .sql_agent_simple import SQLAgent, run_sql_query
    MCPSQLConnection = None

__all__ = ['SQLAgent', 'run_sql_query', 'MCPSQLConnection']