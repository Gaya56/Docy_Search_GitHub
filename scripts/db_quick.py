#!/usr/bin/env python3
"""
Quick database access commands for Docy Search
"""

import sqlite3
import json
import sys
from pathlib import Path


def get_db_path():
    project_root = Path(__file__).parent
    return project_root / "docy_search.db"


def show_stats():
    """Show quick database statistics"""
    db_path = get_db_path()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Get counts
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        chat_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM memory_entries")
        memory_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM activity_log")
        activity_count = cursor.fetchone()[0]
        
        print(f"📊 Database Statistics:")
        print(f"  💬 Chat Records: {chat_count}")
        print(f"  🧠 Memory Entries: {memory_count}")
        print(f"  📈 Activity Logs: {activity_count}")
        print(f"  📁 Database: {db_path}")


def show_recent_chats(limit=5):
    """Show recent chat conversations"""
    db_path = get_db_path()
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT prompt, response, timestamp, model_used 
            FROM chat_history 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (limit,))
        
        chats = cursor.fetchall()
        
        print(f"💬 Last {limit} Chat Conversations:")
        print("=" * 50)
        
        for i, chat in enumerate(chats, 1):
            print(f"\n{i}. {chat['timestamp']} ({chat['model_used']})")
            print(f"Q: {chat['prompt'][:100]}...")
            print(f"A: {chat['response'][:100]}...")


def export_chats():
    """Export all chats to JSON"""
    db_path = get_db_path()
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC")
        chats = [dict(row) for row in cursor.fetchall()]
    
    output_file = "chat_export.json"
    with open(output_file, 'w') as f:
        json.dump(chats, f, indent=2, default=str)
    
    print(f"✅ Exported {len(chats)} chats to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python db_quick.py stats       - Show database statistics")
        print("  python db_quick.py recent [N]  - Show recent N chats (default 5)")
        print("  python db_quick.py export      - Export all chats to JSON")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "stats":
        show_stats()
    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        show_recent_chats(limit)
    elif command == "export":
        export_chats()
    else:
        print(f"Unknown command: {command}")
