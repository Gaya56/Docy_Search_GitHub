from fastmcp import FastMCP
from dotenv import load_dotenv
import sqlite3
import json
from typing import Dict, Any
import re

# Import activity tracking with graceful fallback
try:
    from .activity_tracker import activity_tracker
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    print("Activity tracking not available - running without tracking")

load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP(
    name="sql_tools",
    version="1.0.0",
    description="Natural language to SQL query tool for docy_search database"
)

# Database configuration
database_config = {
    "db_path": "/workspaces/Docy_Search_GitHub/docy_search.db",
    "allowed_operations": ['SELECT', 'COUNT', 'GROUP BY', 'ORDER BY', 'LIMIT']
}


class SafeSQLExecutor:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.allowed_operations = [
            'SELECT', 'COUNT', 'GROUP BY', 'ORDER BY', 'LIMIT'
        ]
        
    def is_safe_query(self, query: str) -> bool:
        """Check if query is safe (read-only operations)"""
        query_upper = query.upper().strip()
        
        # Must start with SELECT
        if not query_upper.startswith('SELECT'):
            return False
            
        # Block dangerous operations
        dangerous_ops = [
            'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'CREATE', 'EXEC'
        ]
        for op in dangerous_ops:
            if op in query_upper:
                return False
                
        return True
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute safe SQL query"""
        if not self.is_safe_query(query):
            return {
                "error": ("Query not allowed - only SELECT operations "
                          "permitted")
            }
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(query)
                rows = cursor.fetchall()
                
                # Convert to list of dicts
                result = []
                for row in rows:
                    result.append(dict(row))
                
                return {
                    "success": True,
                    "rows": result,
                    "count": len(result)
                }
        except Exception as e:
            return {"error": f"SQL execution error: {str(e)}"}


@mcp.tool()
async def natural_language_query(question: str) -> str:
    """
    Convert natural language question to SQL and execute against database
    
    Args:
        question: Natural language question about the database
    """
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            question_preview = (
                question[:50] + "..." if len(question) > 50 else question
            )
            activity_id = await activity_tracker.start_activity(
                tool_name="natural_language_query",
                params={"question": question_preview}
            )
            await activity_tracker.update_activity(
                activity_id,
                progress=20,
                details={"status": "Converting to SQL"}
            )
    
        db_path = database_config["db_path"]
        
        # Simple NL to SQL conversion patterns
        sql_patterns = {
            r"how many.*conversations":
                "SELECT COUNT(*) as count FROM conversations",
            r"latest.*conversations":
                ("SELECT * FROM conversations ORDER BY created_at DESC "
                 "LIMIT 10"),
            r"search.*memory":
                "SELECT * FROM memory_items WHERE content LIKE '%{}%'",
            r"all.*agents":
                "SELECT * FROM agents",
            r"recent.*activity":
                ("SELECT * FROM conversations ORDER BY updated_at DESC "
                 "LIMIT 5"),
            r"show.*tables":
                "SELECT name FROM sqlite_master WHERE type='table'",
            r"count.*memory":
                "SELECT COUNT(*) as count FROM memory_items",
            r"list.*conversations":
                "SELECT id, title, created_at FROM conversations LIMIT 20"
        }
        
        question_lower = question.lower()
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=50,
                details={"status": "Executing query"}
            )
        
        # Find matching pattern
        sql_query = None
        for pattern, query_template in sql_patterns.items():
            if re.search(pattern, question_lower):
                if '{}' in query_template:
                    # Extract search term (last few words)
                    words = question_lower.split()
                    search_term = ' '.join(words[-2:])
                    sql_query = query_template.format(search_term)
                else:
                    sql_query = query_template
                break
        
        if not sql_query:
            error_msg = (
                f"Could not understand question: '{question}'. "
                f"Try asking about conversations, memory, or agents."
            )
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
        # Execute query
        executor = SafeSQLExecutor(db_path)
        result = executor.execute_query(sql_query)
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=80,
                details={"status": "Formatting results"}
            )
        
        if "error" in result:
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=f"Query failed: {result['error']}")
            return f"Database query failed: {result['error']}"
        
        # Format results
        if result['count'] == 0:
            formatted_result = "No results found."
        else:
            formatted_result = json.dumps(
                result['rows'], indent=2, default=str
            )
        
        # Complete activity tracking with success
        if TRACKING_AVAILABLE and activity_id:
            result_preview = (
                f"Query completed: {result['count']} rows returned"
            )
            await activity_tracker.complete_activity(
                activity_id, result=result_preview)
        
        return formatted_result
        
    except Exception as e:
        error_msg = f"Error processing question: {str(e)}"
        
        # Complete activity tracking with error
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Processing failed: {str(e)[:50]}")
        
        return error_msg


@mcp.tool()
async def get_database_schema() -> str:
    """Get the database schema information"""
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="get_database_schema",
                params={}
            )
            await activity_tracker.update_activity(
                activity_id,
                progress=30,
                details={"status": "Reading schema"}
            )
        
        db_path = database_config["db_path"]
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = cursor.fetchall()
            
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.update_activity(
                    activity_id,
                    progress=70,
                    details={"status": "Getting table details"}
                )
            
            schema_info = {}
            for (table_name,) in tables:
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                schema_info[table_name] = [
                    {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3])
                    }
                    for col in columns
                ]
            
            formatted_schema = json.dumps(schema_info, indent=2)
            
            # Complete activity tracking with success
            if TRACKING_AVAILABLE and activity_id:
                result_preview = f"Schema retrieved: {len(tables)} tables"
                await activity_tracker.complete_activity(
                    activity_id, result=result_preview)
            
            return formatted_schema
            
    except Exception as e:
        error_msg = f"Error getting schema: {str(e)}"
        
        # Complete activity tracking with error
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Schema error: {str(e)[:50]}")
        
        return error_msg


if __name__ == "__main__":
    mcp.run()
