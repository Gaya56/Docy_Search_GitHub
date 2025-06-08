# docy_search/database/sql_agent.py
"""Natural language SQL query agent"""
from typing import Optional

from docy_search.activity_tracker import activity_tracker
from docy_search.memory.memory_manager import MemoryManager

# TODO: Re-enable when MCP integration is fixed
# from pydantic_ai import Agent
# from pydantic_ai.mcp import MCPServerStdio
# from .connection_manager import MCPSQLConnection


SQL_AGENT_PROMPT = """You are an intelligent SQL assistant.

Your responsibilities:
1. Understand natural language questions about data
2. Retrieve database schema when needed
3. Generate valid SQL SELECT queries using correct table/column names
4. Execute queries and return results
5. Provide clear, natural language summaries of the data

Constraints:
- Only use SELECT queries (no INSERT/UPDATE/DELETE)
- Return human-friendly explanations, not raw SQL
- Focus on insights, trends, and key findings
- Include relevant numbers and observations

Respond with clear summaries suitable for business users."""


class SQLAgent:
    """Handles natural language database queries"""

    def __init__(self, model=None,
                 memory_manager: Optional[MemoryManager] = None):
        self.model = model
        self.memory_manager = memory_manager

    async def query(self, message: str, user_id: Optional[str] = None) -> str:
        """Execute natural language query and return summary"""
        # TODO: Implement full SQL agent functionality when MCP is fixed
        activity_id = None

        try:
            # Start activity tracking
            activity_id = await activity_tracker.start_activity(
                "sql_query",
                {"query": message[:100], "user_id": user_id}
            )

            # Placeholder response
            response = (
                "SQL database functionality is currently being developed. "
                "This feature will allow you to query your database using "
                "natural language and receive insights about your data."
            )

            # Complete activity tracking
            await activity_tracker.complete_activity(
                activity_id, "SQL query placeholder completed"
            )

            return response

        except Exception as e:
            if activity_id:
                await activity_tracker.complete_activity(
                    activity_id, f"SQL query failed: {str(e)[:100]}"
                )
            return f"SQL query error: {str(e)}"


async def run_sql_query(message: str, user_id: Optional[str] = None) -> str:
    """Run SQL query through agent"""
    try:
        # TODO: Re-enable when dependencies are fixed
        # from docy_search.app import get_model_from_name, memory_manager
        # model = get_model_from_name(os.getenv("AI_MODEL", "openai"))
        # agent = SQLAgent(model, memory_manager)

        agent = SQLAgent()
        return await agent.query(message, user_id)

    except Exception as e:
        return f"Database query error: {str(e)}"
