# docy_search/database/sql_agent_simple.py
"""Simple fallback SQL agent for testing without database connection"""
import asyncio
from typing import Optional
from datetime import datetime

from docy_search.activity_tracker import activity_tracker
from docy_search.memory.memory_manager import MemoryManager


class SQLAgent:
    """Simple fallback SQL agent for testing"""
    
    def __init__(self, model, memory_manager: Optional[MemoryManager] = None):
        self.model = model
        self.memory_manager = memory_manager
        
    async def query(self, message: str, user_id: Optional[str] = None) -> str:
        """Mock query execution for testing"""
        activity_id = await activity_tracker.start_activity(
            "sql_query_mock",
            {"query": message[:100], "user_id": user_id}
        )
        
        try:
            # Simulate processing delay
            await asyncio.sleep(0.5)
            
            # Mock response
            response = f"""Mock SQL Response for: {message[:50]}...
            
Database Schema Analysis:
- Tables found: users, orders, products
- Total records: ~10,000
- Key metrics: 150 active users, 50 recent orders

This is a mock response for testing the dashboard system.
Set up proper database credentials to get real data."""
            
            await activity_tracker.complete_activity(
                activity_id, f"Mock query completed: {len(response)} chars"
            )
            
            return response
            
        except Exception as e:
            await activity_tracker.complete_activity(
                activity_id, f"Mock query failed: {str(e)[:100]}"
            )
            raise


# Convenience function for direct usage
async def run_sql_query(
    message: str, model=None, user_id: Optional[str] = None
) -> str:
    """Run a mock SQL query"""
    from docy_search.app import get_model_from_name, memory_manager
    import os

    if model is None:
        model = get_model_from_name(os.getenv("AI_MODEL", "openai"))

    agent = SQLAgent(model, memory_manager)
    return await agent.query(message, user_id)