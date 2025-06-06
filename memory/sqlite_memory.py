"""
SQLite-based memory storage for persistent user interactions.
Handles database operations for storing and retrieving memories with embeddings.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any, Union
from contextlib import contextmanager
import aiosqlite
from contextlib import asynccontextmanager


class SQLiteMemory:
    """Lightweight SQLite interface for memory storage."""
    
    def __init__(self, db_path: str = "data/memories.db"):
        """Initialize SQLite memory storage.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialize_database()
    
    def _initialize_database(self):
        """Create memories table if it doesn't exist and handle migrations."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Create table with basic schema first
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding TEXT,  -- JSON blob
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,   -- JSON blob
                    category TEXT DEFAULT 'general'
                )
            """)
            
            # Check and add new columns for lifecycle management
            self._migrate_database(cursor)
            
            # Create indices for efficient queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON memories(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_compressed ON memories(compressed)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_archived ON memories(archived)")
            conn.commit()
    
    def _migrate_database(self, cursor):
        """Handle database migrations for new columns."""
        # Check if new columns exist and add them if they don't
        cursor.execute("PRAGMA table_info(memories)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # Add missing columns with constant defaults
        if 'compressed' not in column_names:
            cursor.execute("ALTER TABLE memories ADD COLUMN compressed BOOLEAN DEFAULT FALSE")
        
        if 'archived' not in column_names:
            cursor.execute("ALTER TABLE memories ADD COLUMN archived BOOLEAN DEFAULT FALSE")
        
        if 'access_count' not in column_names:
            cursor.execute("ALTER TABLE memories ADD COLUMN access_count INTEGER DEFAULT 0")
        
        if 'last_accessed' not in column_names:
            # Use NULL as default and update existing records
            cursor.execute("ALTER TABLE memories ADD COLUMN last_accessed DATETIME DEFAULT NULL")
            # Update existing records to have current timestamp
            cursor.execute("UPDATE memories SET last_accessed = timestamp WHERE last_accessed IS NULL")
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()
    
    def save_memory(self, 
                   user_id: str, 
                   content: str,
                   embedding: Optional[List[float]] = None,
                   metadata: Optional[Dict[str, Any]] = None,
                   category: str = "general") -> int:
        """Save a memory to the database.
        
        Args:
            user_id: Unique user identifier
            content: Memory content text
            embedding: Optional embedding vector
            metadata: Optional metadata dictionary
            category: Memory category (default: "general")
            
        Returns:
            ID of inserted memory
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO memories (user_id, content, embedding, metadata, category)
                VALUES (?, ?, ?, ?, ?)
            """, (
                user_id,
                content,
                json.dumps(embedding) if embedding else None,
                json.dumps(metadata) if metadata else None,
                category
            ))
            conn.commit()
            memory_id = cursor.lastrowid
            return memory_id if memory_id is not None else 0
    
    def get_memories(self, 
                    user_id: str, 
                    limit: int = 10,
                    category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve memories for a user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of memories to return
            category: Optional category filter
            
        Returns:
            List of memory dictionaries
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM memories WHERE user_id = ?"
            params = [user_id]
            
            if category:
                query += " AND category = ?"
                params.append(category)
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(str(limit))
            
            cursor.execute(query, params)
            
            memories = []
            for row in cursor.fetchall():
                memory = dict(row)
                # Parse JSON fields
                if memory['embedding']:
                    memory['embedding'] = json.loads(memory['embedding'])
                if memory['metadata']:
                    memory['metadata'] = json.loads(memory['metadata'])
                memories.append(memory)
            
            return memories
    
    def delete_memory(self, memory_id: int) -> bool:
        """Delete a specific memory.
        
        Args:
            memory_id: ID of memory to delete
            
        Returns:
            True if deleted, False if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of memories deleted
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM memories WHERE user_id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount


class AsyncSQLiteMemory:
    """Async SQLite interface for memory storage with lifecycle management."""
    
    def __init__(self, db_path: str = "data/memories.db"):
        """Initialize async SQLite memory storage.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._initialized = False
    
    async def initialize_database(self):
        """Create memories table if it doesn't exist and handle migrations."""
        if self._initialized:
            return
            
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            
            # Create table with basic schema first
            await cursor.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    embedding TEXT,  -- JSON blob
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,   -- JSON blob
                    category TEXT DEFAULT 'general'
                )
            """)
            
            # Check and add new columns for lifecycle management
            await self._migrate_database(cursor)
            
            # Create indices for efficient queries
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON memories(user_id)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_compressed ON memories(compressed)")
            await cursor.execute("CREATE INDEX IF NOT EXISTS idx_archived ON memories(archived)")
            await conn.commit()
            self._initialized = True
    
    async def _migrate_database(self, cursor):
        """Handle database migrations for new columns."""
        # Check if new columns exist and add them if they don't
        await cursor.execute("PRAGMA table_info(memories)")
        columns = await cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # Add missing columns with constant defaults
        if 'compressed' not in column_names:
            await cursor.execute("ALTER TABLE memories ADD COLUMN compressed BOOLEAN DEFAULT FALSE")
        
        if 'archived' not in column_names:
            await cursor.execute("ALTER TABLE memories ADD COLUMN archived BOOLEAN DEFAULT FALSE")
        
        if 'access_count' not in column_names:
            await cursor.execute("ALTER TABLE memories ADD COLUMN access_count INTEGER DEFAULT 0")
        
        if 'last_accessed' not in column_names:
            # Use NULL as default and update existing records
            await cursor.execute("ALTER TABLE memories ADD COLUMN last_accessed DATETIME DEFAULT NULL")
            # Update existing records to have current timestamp
            await cursor.execute("UPDATE memories SET last_accessed = timestamp WHERE last_accessed IS NULL")
    
    async def save_memory(self,
                         user_id: str,
                         content: str,
                         embedding: Optional[List[float]] = None,
                         metadata: Optional[Dict[str, Any]] = None,
                         category: str = "general") -> int:
        """Save a memory with optional embedding (async).
        
        Args:
            user_id: User identifier
            content: Memory content
            embedding: Optional embedding vector
            metadata: Optional metadata dictionary
            category: Memory category
            
        Returns:
            Memory ID
        """
        await self.initialize_database()
        
        # Serialize JSON fields
        embedding_json = json.dumps(embedding) if embedding else None
        metadata_json = json.dumps(metadata) if metadata else None
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute("""
                INSERT INTO memories (user_id, content, embedding, metadata, category)
                VALUES (?, ?, ?, ?, ?)
            """, (user_id, content, embedding_json, metadata_json, category))
            
            await conn.commit()
            return cursor.lastrowid
    
    async def get_memories(self,
                          user_id: str,
                          limit: int = 10,
                          category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve memories for a user (async).
        
        Args:
            user_id: User identifier
            limit: Maximum number of memories to return
            category: Optional category filter
            
        Returns:
            List of memory dictionaries
        """
        await self.initialize_database()
        
        # Build query with optional category filter
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
            
            # Convert to dictionaries and deserialize JSON fields
            memories = []
            for row in rows:
                memory = dict(row)
                # Parse JSON fields
                if memory['embedding']:
                    try:
                        memory['embedding'] = json.loads(memory['embedding'])
                    except json.JSONDecodeError:
                        memory['embedding'] = None
                
                if memory['metadata']:
                    try:
                        memory['metadata'] = json.loads(memory['metadata'])
                    except json.JSONDecodeError:
                        memory['metadata'] = {}
                
                memories.append(memory)
            
            return memories
    
    async def clear_user_memories(self, user_id: str) -> int:
        """Clear all memories for a user (async).
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of deleted memories
        """
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute("DELETE FROM memories WHERE user_id = ?", (user_id,))
            await conn.commit()
            return cursor.rowcount
    
    async def compress_old_memories(self, days_threshold: int = 30) -> int:
        """Compress memories older than threshold (async).
        
        Args:
            days_threshold: Age threshold in days
            
        Returns:
            Number of compressed memories
        """
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute("""
                UPDATE memories 
                SET compressed = TRUE,
                    content = substr(content, 1, 500) || '...[compressed]'
                WHERE compressed = FALSE 
                AND datetime('now', '-{} days') > timestamp
                AND access_count < 5
            """.format(days_threshold))
            await conn.commit()
            return cursor.rowcount
    
    async def archive_old_memories(self, days_threshold: int = 90) -> int:
        """Archive memories older than threshold (async).
        
        Args:
            days_threshold: Age threshold in days
            
        Returns:
            Number of archived memories
        """
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute("""
                UPDATE memories 
                SET archived = TRUE
                WHERE archived = FALSE 
                AND datetime('now', '-{} days') > timestamp
                AND access_count < 2
            """.format(days_threshold))
            await conn.commit()
            return cursor.rowcount
    
    async def get_memory_stats(self, user_id: str) -> Dict[str, int]:
        """Get memory statistics for a user (async).
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary with memory statistics
        """
        await self.initialize_database()
        
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            
            # Total memories
            await cursor.execute("SELECT COUNT(*) FROM memories WHERE user_id = ?", (user_id,))
            total = (await cursor.fetchone())[0]
            
            # Active memories (not archived)
            await cursor.execute("SELECT COUNT(*) FROM memories WHERE user_id = ? AND archived = FALSE", (user_id,))
            active = (await cursor.fetchone())[0]
            
            # Compressed memories
            await cursor.execute("SELECT COUNT(*) FROM memories WHERE user_id = ? AND compressed = TRUE", (user_id,))
            compressed = (await cursor.fetchone())[0]
            
            # Archived memories
            await cursor.execute("SELECT COUNT(*) FROM memories WHERE user_id = ? AND archived = TRUE", (user_id,))
            archived = (await cursor.fetchone())[0]
            
            return {
                'total': total,
                'active': active,
                'compressed': compressed,
                'archived': archived
            }
