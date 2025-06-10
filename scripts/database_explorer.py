#!/usr/bin/env python3
"""
Database Explorer for Docy Search
Access and view your chat history, memory entries, and activity logs
"""

import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path


def get_db_path():
    """Get the path to the SQLite database"""
    project_root = Path(__file__).parent.parent
    return project_root / "docy_search.db"


def display_table_info():
    """Display information about database tables"""
    db_path = get_db_path()
    
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        return
    
    print(f"📊 Database Information")
    print(f"Location: {db_path}")
    print(f"Size: {db_path.stat().st_size:,} bytes")
    print()
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("📋 Tables in database:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"  • {table_name}: {count:,} records")
        print()


def view_chat_history(limit=10, user_id=None):
    """View recent chat history"""
    db_path = get_db_path()
    
    print(f"💬 Recent Chat History (Last {limit} entries)")
    print("=" * 60)
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT * FROM chat_history 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM chat_history 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
        
        chats = cursor.fetchall()
        
        if not chats:
            print("No chat history found")
            return
        
        for i, chat in enumerate(chats, 1):
            print(f"\n🔹 Chat {i} - {chat['timestamp']}")
            print(f"User ID: {chat['user_id'][:12]}...")
            print(f"Model: {chat['model_used'] or 'Unknown'}")
            
            # Display tools used
            tools = chat['tools_used']
            if tools:
                try:
                    tools_list = json.loads(tools) if isinstance(tools, str) else tools
                    print(f"Tools: {', '.join(tools_list) if tools_list else 'None'}")
                except:
                    print(f"Tools: {tools}")
            else:
                print("Tools: None")
            
            print(f"Cost: ${chat['cost']:.4f}")
            print()
            print("🤔 PROMPT:")
            print(chat['prompt'][:200] + "..." if len(chat['prompt']) > 200 else chat['prompt'])
            print()
            print("🤖 RESPONSE:")
            print(chat['response'][:300] + "..." if len(chat['response']) > 300 else chat['response'])
            print("-" * 60)


def view_memory_entries(limit=10, user_id=None):
    """View memory entries"""
    db_path = get_db_path()
    
    print(f"🧠 Memory Entries (Last {limit} entries)")
    print("=" * 60)
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT * FROM memory_entries 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM memory_entries 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (limit,))
        
        memories = cursor.fetchall()
        
        if not memories:
            print("No memory entries found")
            return
        
        for i, memory in enumerate(memories, 1):
            print(f"\n🔹 Memory {i} - {memory['created_at']}")
            print(f"User ID: {memory['user_id'][:12]}...")
            print(f"Memory ID: {memory['memory_id']}")
            print(f"Status: {memory['status']}")
            print()
            print("CONTENT:")
            content = memory['content']
            print(content[:400] + "..." if len(content) > 400 else content)
            print("-" * 60)


def view_activity_logs(limit=20, user_id=None):
    """View activity logs"""
    db_path = get_db_path()
    
    print(f"📊 Activity Logs (Last {limit} entries)")
    print("=" * 60)
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute("""
                SELECT * FROM activity_log 
                WHERE user_id = ? 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (user_id, limit))
        else:
            cursor.execute("""
                SELECT * FROM activity_log 
                ORDER BY timestamp DESC 
                LIMIT ?
            """, (limit,))
        
        activities = cursor.fetchall()
        
        if not activities:
            print("No activity logs found")
            return
        
        for activity in activities:
            print(f"{activity['timestamp']} | {activity['activity_type']} | {activity['description'] or 'No description'}")


def export_data(format='json', output_file=None):
    """Export all data to JSON or CSV"""
    db_path = get_db_path()
    
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"docy_search_export_{timestamp}.{format}"
    
    print(f"📤 Exporting data to {output_file}...")
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get all data
        data = {}
        
        # Chat history
        cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC")
        data['chat_history'] = [dict(row) for row in cursor.fetchall()]
        
        # Memory entries
        cursor.execute("SELECT * FROM memory_entries ORDER BY created_at DESC")
        data['memory_entries'] = [dict(row) for row in cursor.fetchall()]
        
        # Activity logs
        cursor.execute("SELECT * FROM activity_log ORDER BY timestamp DESC")
        data['activity_logs'] = [dict(row) for row in cursor.fetchall()]
        
        # Export metadata
        data['export_info'] = {
            'exported_at': datetime.now().isoformat(),
            'database_path': str(db_path),
            'total_records': {
                'chat_history': len(data['chat_history']),
                'memory_entries': len(data['memory_entries']),
                'activity_logs': len(data['activity_logs'])
            }
        }
    
    if format == 'json':
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    else:
        print(f"Format '{format}' not supported yet. Using JSON.")
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    print(f"✅ Data exported to {output_file}")
    print(f"File size: {Path(output_file).stat().st_size:,} bytes")


def interactive_menu():
    """Interactive menu for database exploration"""
    while True:
        print("\n" + "="*60)
        print("🗄️  DOCY SEARCH DATABASE EXPLORER")
        print("="*60)
        print("1. 📊 Database Info")
        print("2. 💬 View Chat History")
        print("3. 🧠 View Memory Entries")
        print("4. 📈 View Activity Logs")
        print("5. 📤 Export All Data")
        print("6. 🔍 Search Chat History")
        print("0. ❌ Exit")
        print("="*60)
        
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            display_table_info()
        elif choice == '2':
            limit = input("Number of entries to show (default 10): ").strip() or "10"
            user_id = input("Filter by user ID (or press Enter for all): ").strip() or None
            view_chat_history(int(limit), user_id)
        elif choice == '3':
            limit = input("Number of entries to show (default 10): ").strip() or "10"
            user_id = input("Filter by user ID (or press Enter for all): ").strip() or None
            view_memory_entries(int(limit), user_id)
        elif choice == '4':
            limit = input("Number of entries to show (default 20): ").strip() or "20"
            user_id = input("Filter by user ID (or press Enter for all): ").strip() or None
            view_activity_logs(int(limit), user_id)
        elif choice == '5':
            output_file = input("Output filename (or press Enter for auto): ").strip() or None
            export_data('json', output_file)
        elif choice == '6':
            search_term = input("Enter search term: ").strip()
            search_chat_history(search_term)
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


def search_chat_history(search_term):
    """Search chat history for specific terms"""
    db_path = get_db_path()
    
    print(f"🔍 Searching for: '{search_term}'")
    print("=" * 60)
    
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM chat_history 
            WHERE prompt LIKE ? OR response LIKE ?
            ORDER BY timestamp DESC
        """, (f'%{search_term}%', f'%{search_term}%'))
        
        results = cursor.fetchall()
        
        if not results:
            print("No matches found")
            return
        
        print(f"Found {len(results)} matches:")
        
        for i, chat in enumerate(results, 1):
            print(f"\n🔹 Match {i} - {chat['timestamp']}")
            
            # Highlight the search term in prompt
            prompt = chat['prompt']
            if search_term.lower() in prompt.lower():
                print("🤔 PROMPT (contains search term):")
                print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
            
            # Highlight the search term in response
            response = chat['response']
            if search_term.lower() in response.lower():
                print("🤖 RESPONSE (contains search term):")
                print(response[:300] + "..." if len(response) > 300 else response)
            
            print("-" * 40)


if __name__ == "__main__":
    print("🗄️  Welcome to Docy Search Database Explorer!")
    
    # Check if database exists
    db_path = get_db_path()
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        print("Make sure you've run the Docy Search application first.")
        exit(1)
    
    interactive_menu()
