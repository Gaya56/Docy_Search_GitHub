# docy_search/database/sql_agent.py
"""Natural language SQL query agent"""
import asyncio
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic_ai import Agent
from pydantic_ai.tools.mcp import MCPTools
from mcp import ClientSession

from docy_search.activity_tracker import activity_tracker
from docy_search.memory.memory_manager import MemoryManager
from .connection_manager import MCPSQLConnection


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
        
    async def create_agent(self, session: ClientSession) -> Agent:
        """Create pydantic-ai agent with MCP tools"""
        mcp_tools = MCPTools(session=session)
        await mcp_tools.initialize()
        
        return Agent(
            self.model,
            mcp_servers=[],  # Tools already initialized via MCPTools
            tools=[mcp_tools],
            system_prompt=SQL_AGENT_PROMPT
        )
    
    async def query(self, message: str, user_id: Optional[str] = None) -> str:
        """Execute natural language query and return summary"""
        activity_id = None
        
        try:
            # Start activity tracking
            activity_id = await activity_tracker.start_activity(
                "sql_query",
                {"query": message[:100], "user_id": user_id}
            )
            
            # Create MCP session
            async with await MCPSQLConnection.create_session() as (read, write):
                async with ClientSession(read, write) as session:
                    # Create and run agent
                    agent = await self.create_agent(session)
                    await activity_tracker.update_activity(
                        activity_id, 0.5, {"status": "Executing query"}
                    )
                    
                    result = await agent.run(message)
                    response = result.output
                    
                    # Save to memory if available
                    if self.memory_manager and user_id and len(response) > 100:
                        memory_content = f"SQL Query: {message[:200]}\nResult: {response[:500]}"
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
                    
        except Exception as e:
            if activity_id:
                await activity_tracker.complete_activity(
                    activity_id, f"Query failed: {str(e)[:100]}"
                )
            raise


# Convenience function for direct usage
async def run_sql_query(message: str, model=None, user_id: Optional[str] = None) -> str:
    """Run a SQL query with the default or specified model"""
    from docy_search.app import get_model_from_name, memory_manager
    
    if model is None:
        model = get_model_from_name(os.getenv("AI_MODEL", "openai"))
    
    agent = SQLAgent(model, memory_manager)
    return await agent.query(message, user_id)