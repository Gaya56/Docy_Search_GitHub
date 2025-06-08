# docy_search/database/sql_agent_simple.py
"""Simplified SQL query agent for quick fix"""

import os
from typing import Optional


class SQLAgent:
    """Simplified SQL agent for quick fix"""
    
    def __init__(self, model=None, memory_manager=None):
        self.model = model
        self.memory_manager = memory_manager
    
    async def query(self, message: str, user_id: Optional[str] = None) -> str:
        """Execute natural language query and return summary"""
        # Simplified implementation for quick fix
        return "SQL functionality temporarily disabled - under development"


async def run_sql_query(message: str, user_id: Optional[str] = None) -> str:
    """Run SQL query through agent"""
    # Simplified implementation for quick fix
    return "SQL functionality temporarily disabled - under development"
