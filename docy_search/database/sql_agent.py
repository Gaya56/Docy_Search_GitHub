# docy_search/database/sql_agent.py
"""Natural language SQL query agent"""
import asyncio
import os
from typing import Optional
from datetime import datetime
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio

from docy_search.activity_tracker import activity_tracker
from docy_search.memory.memory_manager import MemoryManager


async def retry_on_failure(func, max_retries=2, delay=1):
    """Retry async function on failure"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"SQL operation failed after {max_retries} attempts: {e}")
                raise
            wait_time = delay * (attempt + 1)
            print(f"SQL attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
            await asyncio.sleep(wait_time)


SQL_AGENT_PROMPT = """You are an intelligent SQL assistant with database access through MCP tools.

Your responsibilities:
1. Understand natural language questions about data
2. Use `get_schema` to retrieve database structure when needed
3. Generate valid SQL SELECT queries using correct table/column names
4. Use `read_query` to execute queries and get results
5. Provide clear, natural language summaries of the data

Constraints:
- Only use SELECT queries (no INSERT/UPDATE/DELETE)
- Return human-friendly explanations, not raw SQL
- Focus on insights, trends, and key findings
- Include relevant numbers and observations

Available tools:
- `get_schema`: Get database schema
- `read_query`: Execute SELECT queries

Respond with clear summaries suitable for business users."""


class SQLAgent:
    """Handles natural language database queries"""
    
    def __init__(self, model, memory_manager: Optional[MemoryManager] = None):
        self.model = model
        self.memory_manager = memory_manager
        
    async def create_agent(self) -> Agent:
        """Create pydantic-ai agent with MCP SQL server"""
        # Create MCP SQL server
        mcp_sql_server = MCPServerStdio(
            command="uvx",
            args=[
                "mcp-sql-server",
                "--db-host", os.getenv("DB_HOST"),
                "--db-user", os.getenv("DB_USER"),
                "--db-password", os.getenv("DB_PASSWORD"),
                "--db-database", os.getenv("DB_NAME"),
                "--timeout", "30"
            ],
        )
        
        return Agent(
            self.model,
            mcp_servers=[mcp_sql_server],
            system_prompt=SQL_AGENT_PROMPT
        )
    
    async def query(self, message: str, user_id: Optional[str] = None) -> str:
        """Execute natural language query with retry logic"""
        activity_id = None

        async def execute_query():
            nonlocal activity_id
            # Start activity tracking
            activity_id = await activity_tracker.start_activity(
                "sql_query",
                {"query": message[:100], "user_id": user_id}
            )

            # Create and run agent
            agent = await self.create_agent()
            await activity_tracker.update_activity(
                activity_id, 0.5, {"status": "Executing query"}
            )

            result = await agent.run(message)
            response = result.output

            # Save to memory if available
            if self.memory_manager and user_id and len(response) > 100:
                memory_content = (f"SQL Query: {message[:200]}\n"
                                  f"Result: {response[:500]}")
                await self.memory_manager.async_manager.save_memory(
                    user_id=user_id,
                    content=memory_content,
                    category="database_query",
                    metadata={
                        "query_type": "natural_language_sql",
                        "timestamp": datetime.now().isoformat()
                    }
                )

            await activity_tracker.complete_activity(
                activity_id, f"Query completed: {len(response)} chars"
            )

            return response

        try:
            return await retry_on_failure(execute_query)
        except Exception as e:
            if activity_id:
                await activity_tracker.complete_activity(
                    activity_id, f"Query failed: {str(e)[:100]}"
                )
            raise


# Convenience function for direct usage
async def run_sql_query(
    message: str, model=None, user_id: Optional[str] = None
) -> str:
    """Run a SQL query with the default or specified model"""
    from docy_search.app import get_model_from_name, memory_manager

    if model is None:
        model = get_model_from_name(os.getenv("AI_MODEL", "openai"))

    agent = SQLAgent(model, memory_manager)
    return await agent.query(message, user_id)