# Database Schema Documentation

This document describes the SQLite database schema, operations, and data management in Docy Search.

## 📊 Database Overview

Docy Search uses SQLite for zero-configuration data persistence with two main databases:

1. **Main Database** (`docy_search.db`) - Chat history, activity logs, and application data
2. **Memory Database** (`data/memories.db`) - Semantic memory storage with embeddings

## 🗄 Main Database Schema

### `chat_history` Table
Stores all chat interactions between users and the AI assistant.

```sql
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    model_used TEXT,
    tools_used TEXT,  -- JSON array of tool names
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    memory_id TEXT,   -- Reference to memory entry
    cost REAL DEFAULT 0.0
);

-- Indexes for performance
CREATE INDEX idx_chat_user_id ON chat_history(user_id);
CREATE INDEX idx_chat_timestamp ON chat_history(timestamp);
CREATE INDEX idx_chat_model ON chat_history(model_used);
```

**Field Descriptions**:
- `id`: Unique chat record identifier
- `user_id`: User session identifier (UUID)
- `prompt`: User's input message
- `response`: AI assistant's response
- `model_used`: AI model name ("openai", "claude", "gemini", "deepseek")
- `tools_used`: JSON array of tools used (e.g., `["web_search", "github_search"]`)
- `timestamp`: When the interaction occurred
- `memory_id`: Link to saved memory entry (if applicable)
- `cost`: API cost for this interaction (in USD)

### `activity_log` Table
Tracks all tool usage and system activities for analytics.

```sql
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    description TEXT,
    metadata TEXT,  -- JSON object with activity details
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_activity_user_id ON activity_log(user_id);
CREATE INDEX idx_activity_type ON activity_log(activity_type);
CREATE INDEX idx_activity_timestamp ON activity_log(timestamp);
```

**Field Descriptions**:
- `id`: Unique activity record identifier
- `user_id`: User session identifier
- `activity_type`: Type of activity ("tool_search", "github_access", "memory_save", etc.)
- `description`: Human-readable activity description
- `metadata`: JSON object with detailed activity information
- `timestamp`: When the activity occurred

**Common Activity Types**:
- `tool_search`: Web search operations
- `github_search`: GitHub repository searches
- `github_file_access`: GitHub file retrieval
- `python_execution`: Python code execution
- `memory_save`: Memory storage operations
- `memory_retrieve`: Memory retrieval operations
- `ai_analysis`: AI-powered tool analysis
- `dashboard_generation`: Dashboard creation

### `memory_entries` Table (Main Database)
References to memory entries stored in the memory database.

```sql
CREATE TABLE memory_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT,  -- JSON object
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_memory_user_id ON memory_entries(user_id);
CREATE INDEX idx_memory_status ON memory_entries(status);
CREATE INDEX idx_memory_created ON memory_entries(created_at);
```

**Field Descriptions**:
- `id`: Unique memory reference identifier
- `memory_id`: UUID linking to memory database
- `user_id`: User session identifier
- `content`: Memory content preview (first 500 chars)
- `metadata`: JSON object with memory metadata
- `status`: Memory status ("active", "compressed", "archived")
- `created_at`: When memory was created
- `updated_at`: Last modification time

**Memory Status Values**:
- `active`: Currently accessible memory
- `compressed`: Compressed for space efficiency
- `archived`: Long-term storage, slower access

---

## 🧠 Memory Database Schema

### `memories` Table
Stores detailed memory entries with embeddings for semantic search.

```sql
CREATE TABLE memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    embedding TEXT,  -- Base64 encoded embedding vector
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata TEXT,   -- JSON object
    category TEXT DEFAULT 'general',
    compressed BOOLEAN DEFAULT FALSE,
    archived BOOLEAN DEFAULT FALSE,
    access_count INTEGER DEFAULT 0,
    last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_memories_user_id ON memories(user_id);
CREATE INDEX idx_memories_timestamp ON memories(timestamp);
CREATE INDEX idx_memories_category ON memories(category);
CREATE INDEX idx_memories_compressed ON memories(compressed);
CREATE INDEX idx_memories_archived ON memories(archived);
CREATE INDEX idx_memories_access_count ON memories(access_count);
```

**Field Descriptions**:
- `id`: Unique memory identifier
- `user_id`: User session identifier
- `content`: Full memory content
- `embedding`: OpenAI embedding vector (base64 encoded)
- `timestamp`: When memory was created
- `metadata`: JSON object with additional information
- `category`: Memory category ("tool_recommendation", "preferences", "project", etc.)
- `compressed`: Whether content is compressed
- `archived`: Whether memory is archived
- `access_count`: Number of times memory was retrieved
- `last_accessed`: Last time memory was accessed

**Memory Categories**:
- `tool_recommendation`: Tool-related conversations
- `preferences`: User preferences and choices
- `project`: Project-specific information
- `general`: Uncategorized memories
- `error`: Error-related interactions
- `tutorial`: Learning and tutorial content

---

## 🔄 Database Operations

### Chat History Operations

#### Save Chat Interaction
```python
def save_chat_interaction(user_id: str, prompt: str, response: str, 
                         model_used: str = None, tools_used: List[str] = None,
                         memory_id: str = None, cost: float = 0.0) -> int:
    """Save chat interaction to database."""
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
        return cursor.lastrowid
```

#### Retrieve Chat History
```python
def get_chat_history(user_id: str, limit: int = 50) -> List[Dict]:
    """Get chat history for user."""
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
```

### Activity Logging

#### Log Activity
```python
def log_activity(user_id: str, activity_type: str, 
                description: str = None, metadata: Dict = None):
    """Log user activity."""
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
```

### Memory Operations

#### Save Memory Entry
```python
def save_memory_entry(memory_id: str, user_id: str, 
                     content: str, metadata: Dict = None) -> bool:
    """Save memory entry reference."""
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
```

### Statistics and Analytics

#### Get Database Statistics
```python
def get_database_stats() -> Dict[str, Any]:
    """Get overall database statistics."""
    stats = {}
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()
        
        # Total records per table
        tables = ['chat_history', 'memory_entries', 'activity_log']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[f"{table}_count"] = cursor.fetchone()[0]
        
        # Recent activity (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) FROM activity_log
            WHERE timestamp > datetime('now', '-24 hours')
        """)
        stats['recent_activity_24h'] = cursor.fetchone()[0]
        
        # Most used AI model
        cursor.execute("""
            SELECT model_used, COUNT(*) as count
            FROM chat_history
            WHERE model_used IS NOT NULL
            GROUP BY model_used
            ORDER BY count DESC
            LIMIT 1
        """)
        result = cursor.fetchone()
        stats['most_used_model'] = result[0] if result else 'None'
        
        # Total API cost
        cursor.execute("SELECT SUM(cost) FROM chat_history")
        total_cost = cursor.fetchone()[0]
        stats['total_api_cost'] = total_cost or 0.0
        
        return stats
```

#### Get Memory Statistics
```python
def get_memory_stats(user_id: str = None) -> Dict[str, int]:
    """Get memory statistics."""
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
```

---

## 📈 Database Analytics

### Usage Analytics Queries

#### Most Active Users
```sql
SELECT 
    user_id,
    COUNT(*) as interaction_count,
    SUM(cost) as total_cost,
    MAX(timestamp) as last_active
FROM chat_history
GROUP BY user_id
ORDER BY interaction_count DESC
LIMIT 10;
```

#### Tool Usage Statistics
```sql
SELECT 
    json_extract(tools_used, '$') as tool,
    COUNT(*) as usage_count
FROM chat_history
WHERE tools_used IS NOT NULL
GROUP BY tool
ORDER BY usage_count DESC;
```

#### Model Performance
```sql
SELECT 
    model_used,
    COUNT(*) as usage_count,
    AVG(cost) as avg_cost,
    AVG(LENGTH(response)) as avg_response_length
FROM chat_history
WHERE model_used IS NOT NULL
GROUP BY model_used;
```

#### Activity Trends
```sql
SELECT 
    DATE(timestamp) as date,
    activity_type,
    COUNT(*) as activity_count
FROM activity_log
WHERE timestamp >= date('now', '-30 days')
GROUP BY DATE(timestamp), activity_type
ORDER BY date DESC, activity_count DESC;
```

### Memory Analytics

#### Memory Usage by Category
```sql
SELECT 
    category,
    COUNT(*) as memory_count,
    AVG(access_count) as avg_access_count,
    AVG(LENGTH(content)) as avg_content_length
FROM memories
GROUP BY category
ORDER BY memory_count DESC;
```

#### Memory Access Patterns
```sql
SELECT 
    user_id,
    COUNT(*) as total_memories,
    SUM(access_count) as total_accesses,
    AVG(access_count) as avg_access_per_memory
FROM memories
GROUP BY user_id
HAVING total_memories > 5
ORDER BY avg_access_per_memory DESC;
```

---

## 🔧 Database Maintenance

### Regular Maintenance Tasks

#### Memory Compression
```python
async def perform_memory_maintenance():
    """Compress and archive old memories."""
    results = {'compressed': 0, 'archived': 0}
    
    # Compress memories with low access count
    compressed = await compress_low_access_memories()
    results['compressed'] = compressed
    
    # Archive very old memories
    archived = await archive_old_memories()
    results['archived'] = archived
    
    return results
```

#### Database Optimization
```sql
-- Analyze tables for query optimization
ANALYZE;

-- Rebuild indexes
REINDEX;

-- Vacuum to reclaim space
VACUUM;

-- Update statistics
UPDATE sqlite_master SET sql = sql WHERE type = 'table';
```

#### Cleanup Old Data
```python
def cleanup_old_data(days_to_keep: int = 90):
    """Remove old activity logs and archived memories."""
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()
        
        # Remove old activity logs
        cursor.execute("""
            DELETE FROM activity_log
            WHERE timestamp < datetime('now', '-{} days')
        """.format(days_to_keep))
        
        # Remove archived memories older than threshold
        cursor.execute("""
            DELETE FROM memory_entries
            WHERE status = 'archived'
            AND created_at < datetime('now', '-{} days')
        """.format(days_to_keep * 2))
```

### Backup and Export

#### Database Backup
```python
def backup_database(backup_path: str):
    """Create a backup of the database."""
    import shutil
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"{backup_path}/docy_search_backup_{timestamp}.db"
    
    shutil.copy2(self.db_path, backup_file)
    return backup_file
```

#### Export Chat History
```python
def export_chat_history(user_id: str, format: str = 'json') -> str:
    """Export user's chat history."""
    chat_history = self.get_chat_history(user_id, limit=None)
    
    if format == 'json':
        return json.dumps(chat_history, indent=2, default=str)
    elif format == 'csv':
        import pandas as pd
        df = pd.DataFrame(chat_history)
        return df.to_csv(index=False)
```

---

## 🔍 Database Exploration

### Interactive Database Browser
Use the built-in database explorer:

```bash
python scripts/database_explorer.py
```

Features:
- Browse all tables and their data
- Execute custom SQL queries
- View table schemas and indexes
- Export data in various formats
- Real-time statistics dashboard

### Common Queries for Exploration

#### Recent Conversations
```sql
SELECT 
    substr(user_id, 1, 8) as user,
    substr(prompt, 1, 50) as question,
    substr(response, 1, 100) as answer,
    model_used,
    timestamp
FROM chat_history
ORDER BY timestamp DESC
LIMIT 20;
```

#### Tool Usage Summary
```sql
SELECT 
    activity_type,
    COUNT(*) as count,
    COUNT(DISTINCT user_id) as unique_users
FROM activity_log
GROUP BY activity_type
ORDER BY count DESC;
```

#### Memory Health Check
```sql
SELECT 
    category,
    status,
    COUNT(*) as count,
    AVG(access_count) as avg_access
FROM memories m
JOIN memory_entries me ON m.id = me.memory_id
GROUP BY category, status;
```

---

## 🛡 Data Privacy and Security

### User Data Isolation
- Each user has a unique UUID session identifier
- Memories are isolated per user
- No cross-user data access in queries
- Session data is not persistent across browser sessions

### Data Retention
- Chat history: Retained indefinitely (user can clear)
- Activity logs: 90 days default retention
- Memories: User-controlled with compression/archival
- Backups: 7 days of daily backups retained

### Data Export and Deletion
- Users can export their data via the UI
- Users can clear their conversation history
- Admins can remove user data via database operations
- Memory data can be selectively deleted by category

### API Key Security
- API keys are stored only in environment variables
- Database does not store API keys
- Costs are tracked but not linked to specific API keys
- Response content is stored but not API request details

---

This database documentation provides a complete reference for understanding and working with the Docy Search data layer. For database administration tasks, use the provided scripts and UI tools for safe operations.
