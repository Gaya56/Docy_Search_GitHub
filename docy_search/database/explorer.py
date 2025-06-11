#!/usr/bin/env python3
"""
Database Explorer for Docy Search
Access and view your chat history, memory entries, and activity logs
Can be run standalone or imported as a module
"""

import sqlite3
import json
import argparse
import sys
from datetime import datetime
from pathlib import Path


def get_db_paths():
    """Get all possible database paths"""
    project_root = Path(__file__).parent.parent.parent
    return {
        'main': project_root / "docy_search.db",
        'memory': project_root / "data" / "memories.db"
    }


def get_active_db_path():
    """Get the active database path - auto-detect which exists and has data"""
    paths = get_db_paths()
    
    # Prefer main database if it exists and has data
    if paths['main'].exists():
        try:
            with sqlite3.connect(paths['main']) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                if cursor.fetchone()[0] > 0:
                    return paths['main']
        except sqlite3.Error:
            pass
    
    # Fall back to memory database
    if paths['memory'].exists():
        return paths['memory']
    
    # Default fallback
    return paths['main']


def show_quick_stats():
    """Show quick database statistics"""
    db_path = get_active_db_path()
    
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        return
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Get table info
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            print(f"📊 Database Statistics:")
            print(f"  📁 Database: {db_path}")
            print(f"  📏 Size: {db_path.stat().st_size:,} bytes")
            
            # Count records in each table
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    icon = {"chat_history": "💬", "memory_entries": "🧠", "activity_log": "📈"}.get(table, "📋")
                    print(f"  {icon} {table}: {count:,} records")
                except sqlite3.Error:
                    print(f"  ❌ {table}: Error reading")
                    
    except Exception as e:
        print(f"❌ Error accessing database: {e}")


def display_table_info():
    """Display comprehensive information about database tables"""
    db_path = get_active_db_path()
    
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
    db_path = get_active_db_path()
    
    print(f"💬 Recent Chat History (Last {limit} entries)")
    print("=" * 60)
    
    try:
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
                chat_dict = dict(chat)
                print(f"\n🔹 Chat {i} - {chat_dict['timestamp']}")
                
                user_id = chat_dict.get('user_id', 'Unknown')
                print(f"User ID: {str(user_id)[:12]}...")
                print(f"Model: {chat_dict.get('model_used', 'Unknown')}")
                
                # Display tools used
                tools = chat_dict.get('tools_used')
                if tools:
                    try:
                        tools_list = json.loads(tools) if isinstance(tools, str) else tools
                        print(f"Tools: {', '.join(tools_list) if tools_list else 'None'}")
                    except Exception:
                        print(f"Tools: {tools}")
                else:
                    print("Tools: None")
                
                cost = chat_dict.get('cost', 0)
                if cost:
                    print(f"Cost: ${cost:.4f}")
                
                print()
                print("🤔 PROMPT:")
                prompt = chat_dict.get('prompt', '')
                print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
                print()
                print("🤖 RESPONSE:")
                response = chat_dict.get('response', '')
                print(response[:300] + "..." if len(response) > 300 else response)
                print("-" * 60)
                
    except Exception as e:
        print(f"❌ Error viewing chat history: {e}")


def view_memory_entries(limit=10, user_id=None):
    """View memory entries"""
    db_path = get_active_db_path()
    
    print(f"🧠 Memory Entries (Last {limit} entries)")
    print("=" * 60)
    
    try:
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
                print(f"User ID: {memory.get('user_id', 'Unknown')[:12]}...")
                print(f"Memory ID: {memory.get('memory_id', 'Unknown')}")
                print(f"Status: {memory.get('status', 'Unknown')}")
                print()
                print("CONTENT:")
                content = memory.get('content', '')
                print(content[:400] + "..." if len(content) > 400 else content)
                print("-" * 60)
                
    except Exception as e:
        print(f"❌ Error viewing memory entries: {e}")


def view_activity_logs(limit=20, user_id=None):
    """View activity logs"""
    db_path = get_active_db_path()
    
    print(f"📊 Activity Logs (Last {limit} entries)")
    print("=" * 60)
    
    try:
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
                timestamp = activity.get('timestamp', 'Unknown')
                activity_type = activity.get('activity_type', 'Unknown')
                description = activity.get('description', 'No description')
                print(f"{timestamp} | {activity_type} | {description}")
                
    except Exception as e:
        print(f"❌ Error viewing activity logs: {e}")


def export_data(format='json', output_file=None):
    """Export all data to JSON"""
    db_path = get_active_db_path()
    
    if not output_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"docy_search_export_{timestamp}.{format}"
    
    print(f"📤 Exporting data to {output_file}...")
    
    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Get all data
            data = {}
            
            # Get table names
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            for table in tables:
                try:
                    cursor.execute(f"SELECT * FROM {table} ORDER BY rowid DESC")
                    data[table] = [dict(row) for row in cursor.fetchall()]
                except sqlite3.Error as e:
                    print(f"⚠️  Warning: Could not export table {table}: {e}")
                    data[table] = []
            
            # Export metadata
            data['export_info'] = {
                'exported_at': datetime.now().isoformat(),
                'database_path': str(db_path),
                'total_records': {table: len(records) for table, records in data.items() if table != 'export_info'}
            }
        
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"✅ Data exported to {output_file}")
        print(f"File size: {Path(output_file).stat().st_size:,} bytes")
        
    except Exception as e:
        print(f"❌ Error exporting data: {e}")


def search_chat_history(search_term):
    """Search chat history for specific terms"""
    db_path = get_active_db_path()
    
    print(f"🔍 Searching for: '{search_term}'")
    print("=" * 60)
    
    try:
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
                prompt = chat.get('prompt', '')
                if search_term.lower() in prompt.lower():
                    print("🤔 PROMPT (contains search term):")
                    print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
                
                # Highlight the search term in response
                response = chat.get('response', '')
                if search_term.lower() in response.lower():
                    print("🤖 RESPONSE (contains search term):")
                    print(response[:300] + "..." if len(response) > 300 else response)
                
                print("-" * 40)
                
    except Exception as e:
        print(f"❌ Error searching chat history: {e}")


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
        print("7. 📋 Quick Stats")
        print("0. ❌ Exit")
        print("="*60)
        
        choice = input("Enter your choice (0-7): ").strip()
        
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
        elif choice == '7':
            show_quick_stats()
        else:
            print("❌ Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


def main():
    """Main function with command-line argument support"""
    parser = argparse.ArgumentParser(
        description='Docy Search Database Explorer - View and analyze your AI conversation data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python database_explorer.py                    # Interactive mode
  python database_explorer.py --stats            # Quick statistics
  python database_explorer.py --recent 5         # Show 5 recent chats
  python database_explorer.py --export backup.json  # Export all data
  python database_explorer.py --search "error"   # Search for term
        """
    )
    
    parser.add_argument('--stats', action='store_true', 
                       help='Show quick database statistics')
    parser.add_argument('--recent', type=int, metavar='N', 
                       help='Show N recent chat conversations')
    parser.add_argument('--export', metavar='FILE', 
                       help='Export all data to JSON file')
    parser.add_argument('--search', metavar='TERM', 
                       help='Search chat history for specific term')
    parser.add_argument('--memory', type=int, metavar='N',
                       help='Show N recent memory entries')
    parser.add_argument('--activity', type=int, metavar='N',
                       help='Show N recent activity log entries')
    
    args = parser.parse_args()
    
    # Check if database exists
    db_path = get_active_db_path()
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        print("Make sure you've run the Docy Search application first.")
        return 1
    
    # Handle command-line arguments
    if args.stats:
        show_quick_stats()
    elif args.recent is not None:
        view_chat_history(args.recent)
    elif args.memory is not None:
        view_memory_entries(args.memory)
    elif args.activity is not None:
        view_activity_logs(args.activity)
    elif args.export:
        export_data('json', args.export)
    elif args.search:
        search_chat_history(args.search)
    else:
        # Default to interactive mode
        print("🗄️  Welcome to Docy Search Database Explorer!")
        interactive_menu()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
