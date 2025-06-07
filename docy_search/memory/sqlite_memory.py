"""
Optimized SQLite-based memory storage with shared functionality.
Reduces code duplication between sync and async implementations.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from contextlib import contextmanager
import aiosqlite


class DatabaseMixin:
    """Shared database functionality for sync and async implementations."""
    
    def __init__(self, db_path: str = "data/memories.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    @staticmethod
    def _get_schema_queries():
        """Get database schema creation queries."""
        return [
            """CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                embedding TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                category TEXT DEFAULT 'general',
                compressed BOOLEAN DEFAULT FALSE,
                archived BOOLEAN DEFAULT FALSE,
                access_count INTEGER DEFAULT 0,
                last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
            )""",
            "CREATE INDEX IF NOT EXISTS idx_user_id ON memories(user_id)",
            "CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_category ON memories(category)",
            "CREATE INDEX IF NOT EXISTS idx_compressed ON memories(compressed)",
            "CREATE INDEX IF NOT EXISTS idx_archived ON memories(archived)"
        ]
    
    @staticmethod
    def _parse_memory_row(row) -> Dict[str, Any]:
        """Parse a database row into a memory dictionary."""
        memory = dict(row)
        # Parse JSON fields with error handling
        for field in ['embedding', 'metadata']:
            if memory.get(field):
                try:
                    memory[field] = json.loads(memory[field])
                except json.JSONDecodeError:
                    memory[field] = None if field == 'embedding' else {}
        return memory


class SQLiteMemory(DatabaseMixin):
    """Lightweight synchronous SQLite interface for memory storage."""
    
    def __init__(self, db_path: str = "data/memories.db"):
        super().__init__(db_path)
        self._initialize_database()
    
    def _initialize_database(self):
        """Create memories table and indices."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for query in self._get_schema_queries():
                cursor.execute(query)
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def save_memory(self, user_id: str, content: str, embedding: Optional[List[float]] = None,
                   metadata: Optional[Dict[str, Any]] = None, category: str = "general") -> int:
        """Save a memory to the database."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memories (user_id, content, embedding, metadata, category)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id, content,
                json.dumps(embedding) if embedding else None,
                json.dumps(metadata) if metadata else None,
                category
            ))
            conn.commit()
            return cursor.lastrowid or 0
    
    def get_memories(self, user_id: str, limit: int = 10, 
                    category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve memories for a user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM memories WHERE user_id = ? AND archived = FALSE"
            params = [user_id]
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            return [self._parse_memory_row(row) for row in cursor.fetchall()]
    
    def delete_memory(self, memory_id: int) -> bool:
        """Delete a specific memory."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount


class AsyncSQLiteMemory(DatabaseMixin):
    """Asynchronous SQLite interface with lifecycle management."""
    
    def __init__(self, db_path: str = "data/memories.db"):
        super().__init__(db_path)
        self._initialized = False
    
    async def initialize_database(self):
        """Create memories table and indices."""
        if self._initialized:
            return
            
        async with aiosqlite.connect(self.db_path) as conn:
            for query in self._get_schema_queries():
                await conn.execute(query)
            await conn.commit()
            self._initialized = True
    
    async def save_memory(self, user_id: str, content: str, embedding: Optional[List[float]] = None,
                         metadata: Optional[Dict[str, Any]] = None, category: str = "general") -> int:
        """Save a memory with optional embedding (async)."""
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO memories (user_id, content, embedding, metadata, category)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id, content,
                json.dumps(embedding) if embedding else None,
                json.dumps(metadata) if metadata else None,
                category
            ))
            await conn.commit()
            return cursor.lastrowid
    
    async def get_memories(self, user_id: str, limit: int = 10,
                          category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve memories for a user (async)."""
        await self.initialize_database()
        
        query = "SELECT * FROM memories WHERE user_id = ? AND archived = FALSE"
        params: List[Union[str, int]] = [user_id]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        async with aiosqlite.connect(self.db_path) as conn:
            conn.row_factory = aiosqlite.Row
            cursor = await conn.cursor()
            await cursor.execute(query, params)
            rows = await cursor.fetchall()
            
            # Update access tracking
            if rows:
                memory_ids = [row['id'] for row in rows]
                placeholders = ','.join(['?' for _ in memory_ids])
                await cursor.execute(f"""
                    UPDATE memories 
                    SET access_count = access_count + 1, last_accessed = CURRENT_TIMESTAMP
                    WHERE id IN ({placeholders})
                """, memory_ids)
                await conn.commit()
            
            return [self._parse_memory_row(row) for row in rows]
    
    async def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user (async)."""
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute("DELETE FROM memories WHERE user_id = ?", (user_id,))
            await conn.commit()
            return cursor.rowcount
    
    async def compress_old_memories(self, days_threshold: int = 30) -> int:
        """Compress memories older than threshold."""
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute(f"""
                UPDATE memories 
                SET compressed = TRUE,
                    content = substr(content, 1, 500) || '...[compressed]'
                WHERE compressed = FALSE 
                AND datetime('now', '-{days_threshold} days') > timestamp
                AND access_count < 5
            """)
            await conn.commit()
            return cursor.rowcount
    
    async def archive_old_memories(self, days_threshold: int = 90) -> int:
        """Archive memories older than threshold."""
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute(f"""
                UPDATE memories 
                SET archived = TRUE
                WHERE archived = FALSE 
                AND datetime('now', '-{days_threshold} days') > timestamp
                AND access_count < 2
            """)
            await conn.commit()
            return cursor.rowcount
    
    async def get_memory_stats(self, user_id: str) -> Dict[str, int]:
        """Get memory statistics for a user."""
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            
            # Get all stats in one batch
            stats_queries = [
                ("total", "SELECT COUNT(*) FROM memories WHERE user_id = ?"),
                ("active", "SELECT COUNT(*) FROM memories WHERE user_id = ? AND archived = FALSE"),
                ("compressed", "SELECT COUNT(*) FROM memories WHERE user_id = ? AND compressed = TRUE"),
                ("archived", "SELECT COUNT(*) FROM memories WHERE user_id = ? AND archived = TRUE")
            ]
            
            stats = {}
            for stat_name, query in stats_queries:
                await cursor.execute(query, (user_id,))
                stats[stat_name] = (await cursor.fetchone())[0]
            
            return stats
