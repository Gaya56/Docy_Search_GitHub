"""
Cost tracking for OpenAI API usage and other services
"""
import aiosqlite
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
import tiktoken


class CostTracker:
    """Track API usage costs across all services"""
    
    # Cost per 1K tokens (USD)
    COSTS = {
        "text-embedding-3-small": 0.00002,
        "text-embedding-3-large": 0.00013,
        "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gemini-1.5-flash": 0.00001,  # rough estimate
        "claude-3-opus": {"input": 0.015, "output": 0.075}
    }
    
    def __init__(self, db_path: str = "data/costs.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialized = False
    
    async def initialize(self):
        """Create cost tracking table"""
        if self._initialized:
            return
            
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS api_costs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    service TEXT NOT NULL,
                    model TEXT NOT NULL,
                    operation TEXT NOT NULL,
                    tokens INTEGER,
                    cost REAL NOT NULL,
                    metadata TEXT
                )
            """)
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON api_costs(timestamp)")
            await conn.execute("CREATE INDEX IF NOT EXISTS idx_service ON api_costs(service)")
            await conn.commit()
        self._initialized = True
    
    def count_tokens(self, text: str, model: str = "text-embedding-3-small") -> int:
        """Count tokens for text using tiktoken"""
        try:
            if "embedding" in model:
                encoding = tiktoken.get_encoding("cl100k_base")
            else:
                encoding = tiktoken.encoding_for_model(model.replace("gpt-4o-mini", "gpt-4"))
            return len(encoding.encode(text))
        except:
            # Fallback estimation
            return int(len(text.split()) * 1.3)
    
    async def log_embedding_cost(self, text: str, model: str = "text-embedding-3-small"):
        """Log embedding API usage"""
        await self.initialize()
        
        tokens = self.count_tokens(text, model)
        cost = (tokens / 1000) * self.COSTS.get(model, 0)
        
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("""
                INSERT INTO api_costs (service, model, operation, tokens, cost)
                VALUES (?, ?, ?, ?, ?)
            """, ("openai", model, "embedding", tokens, cost))
            await conn.commit()
        
        return {"tokens": tokens, "cost": cost}
    
    async def log_llm_cost(self, input_text: str, output_text: str, model: str):
        """Log LLM API usage"""
        await self.initialize()
        
        input_tokens = self.count_tokens(input_text, model)
        output_tokens = self.count_tokens(output_text, model)
        
        if isinstance(self.COSTS.get(model, 0), dict):
            cost = (input_tokens / 1000) * self.COSTS[model]["input"]
            cost += (output_tokens / 1000) * self.COSTS[model]["output"]
        else:
            total_tokens = input_tokens + output_tokens
            cost = (total_tokens / 1000) * self.COSTS.get(model, 0)
        
        async with aiosqlite.connect(self.db_path) as conn:
            await conn.execute("""
                INSERT INTO api_costs (service, model, operation, tokens, cost)
                VALUES (?, ?, ?, ?, ?)
            """, ("openai", model, "chat", input_tokens + output_tokens, cost))
            await conn.commit()
        
        return {"input_tokens": input_tokens, "output_tokens": output_tokens, "cost": cost}
    
    async def get_costs_by_period(self, hours: int = 24) -> Dict[str, float]:
        """Get costs for the last N hours"""
        await self.initialize()
        
        since = datetime.now() - timedelta(hours=hours)
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute("""
                SELECT service, SUM(cost) as total_cost
                FROM api_costs
                WHERE timestamp >= ?
                GROUP BY service
            """, (since.isoformat(),))
            
            costs = {}
            async for row in cursor:
                costs[row[0]] = row[1]
            
            cursor = await conn.execute("""
                SELECT SUM(cost) as total
                FROM api_costs
                WHERE timestamp >= ?
            """, (since.isoformat(),))
            
            row = await cursor.fetchone()
            costs['total'] = row[0] or 0
            
            return costs
    
    async def get_daily_cost(self) -> float:
        """Get today's total cost"""
        costs = await self.get_costs_by_period(24)
        return costs.get('total', 0)
    
    async def get_monthly_cost(self) -> float:
        """Get this month's total cost"""
        costs = await self.get_costs_by_period(24 * 30)
        return costs.get('total', 0)