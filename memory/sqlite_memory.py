"""
SQLite-based memory storage for persistent user interactions.
Handles database operations for storing and retrieving memories with embeddings.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from contextlib import contextmanager


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
        """Create memories table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
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
            # Create indices for efficient queries
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_id ON memories(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON memories(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON memories(category)")
            conn.commit()
    
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
