# docy_search/database/db_manager.py
"""
Simple SQLite database manager for Docy Search
No credentials, no external dependencies, just works!
"""

import sqlite3
import json
from typing import Dict, List, Optional, Any
from pathlib import Path


class DatabaseManager:
    """Simple SQLite database manager"""

    def __init__(self):
        project_root = Path(__file__).parent.parent.parent
        self.db_path = project_root / "docy_search.db"
        self.init_database()

    def init_database(self):
        """Initialize database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Chat history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    prompt TEXT NOT NULL,
                    response TEXT NOT NULL,
                    model_used TEXT,
                    tools_used TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    memory_id TEXT,
                    cost REAL DEFAULT 0.0
                )
            """)

            # Memory entries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id TEXT UNIQUE NOT NULL,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    metadata TEXT,
                    status TEXT DEFAULT 'active',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Activity log table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    description TEXT,
                    metadata TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    def save_chat_interaction(self, user_id: str, prompt: str, response: str,                              model_used: Optional[str] = None,
                              tools_used: Optional[List[str]] = None,
                              memory_id: Optional[str] = None,
                              cost: float = 0.0) -> int:
        """Save chat interaction to database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_history
                (user_id, prompt, response, model_used, tools_used, memory_id, cost)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id, prompt, response, model_used,
                json.dumps(tools_used) if tools_used else None,
                memory_id, cost
            ))
            return cursor.lastrowid or 0

    def save_chat(self, user_id: str, prompt: str, response: str,
                  model_used: Optional[str] = None,
                  tools_used: Optional[List[str]] = None,
                  memory_id: Optional[str] = None,
                  cost: float = 0.0) -> int:
        """Alias for save_chat_interaction for compatibility"""
        return self.save_chat_interaction(
            user_id, prompt, response, model_used, tools_used, memory_id, cost
        )

    def get_chat_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get chat history for user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM chat_history 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (user_id, limit))
            return [dict(row) for row in cursor.fetchall()]

    def save_memory_entry(self, memory_id: str, user_id: str,
                          content: str, metadata: Optional[Dict] = None) -> bool:
        """Save memory entry"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO memory_entries
                    (memory_id, user_id, content, metadata, updated_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (
                    memory_id, user_id, content,
                    json.dumps(metadata) if metadata else None
                ))
                return True
        except Exception:
            return False

    def get_memory_stats(self, user_id: Optional[str] = None) -> Dict[str, int]:
        """Get memory statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            where_clause = "WHERE user_id = ?" if user_id else ""
            params = (user_id,) if user_id else ()

            cursor.execute(f"""
                SELECT status, COUNT(*) as count
                FROM memory_entries
                {where_clause}
                GROUP BY status
            """, params)

            stats = {'total': 0, 'active': 0, 'compressed': 0, 'archived': 0}
            for row in cursor.fetchall():
                status, count = row
                stats[status] = count
                stats['total'] += count

            return stats

    def log_activity(self, user_id: str, activity_type: str,
                     description: Optional[str] = None, 
                     metadata: Optional[Dict] = None):
        """Log user activity"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activity_log
                (user_id, activity_type, description, metadata)
                VALUES (?, ?, ?, ?)
            """, (
                user_id, activity_type, description,
                json.dumps(metadata) if metadata else None
            ))

    def get_database_stats(self) -> Dict[str, Any]:
        """Get overall database statistics"""
        stats = {}
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total records per table
            tables = ['chat_history', 'memory_entries', 'activity_log']
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                stats[f"{table}_count"] = cursor.fetchone()[0]

            # Recent activity
            cursor.execute("""
                SELECT COUNT(*) FROM activity_log
                WHERE timestamp > datetime('now', '-24 hours')
            """)
            stats['recent_activity_24h'] = cursor.fetchone()[0]

            return stats


# Global database instance
_db_manager = None


def get_db_manager() -> DatabaseManager:
    """Get or create database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
