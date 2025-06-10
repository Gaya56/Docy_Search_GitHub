# 🔧 Docy Search - AI Tool Recommendation Assistant

**An intelligent AI assistant with SQLite database, semantic memory, and comprehensive web interface**

## ✅ **Status: FULLY OPERATIONAL - Production Ready**

Complete AI assistant with SQLite database integration, chat history tracking, dashboard generation, and multi-model support.

---

## 🚀 **Quick Start**

### Installation
```bash
# 1. Clone repository
git clone https://github.com/yourusername/Docy_Search_GitHub.git
cd Docy_Search_GitHub

# 2. Install dependencies
pip install uv && uv sync

# 3. Set up API keys (optional)
cp .env.example .env
# Edit .env with your API keys
```

### Launch Application
```bash
# Web Interface (Recommended)
uv run streamlit run docy_search/main_ui.py

# Command Line Interface  
uv run python docy_search/app.py

# Database Utilities
uv run python scripts/view_chats.py          # View chat history
uv run python scripts/database_explorer.py  # Interactive database browser
```

---

## 🗄️ **SQLite Database Features (NEW)**

### **Zero Configuration**
- ✅ **No credentials required** - Works out of the box
- ✅ **Auto-created database** - `docy_search.db` generated on first run
- ✅ **Cross-platform** - Works on Windows, macOS, Linux

### **Automatic Data Tracking**
- ✅ **Chat history** - All conversations saved with metadata
- ✅ **Memory persistence** - Semantic search with OpenAI embeddings
- ✅ **Activity logging** - Complete audit trail of operations
- ✅ **Cost tracking** - API usage per model/user

### **Web UI Database Viewer**
- 📊 Browse chat history with full conversation details
- 📈 Real-time database statistics and metrics
- 📤 Export data in CSV/JSON formats
- 🔍 Search and filter conversations

---

## 🧠 **Key Features**

### **AI-Powered Dashboard Generator**
- Automatic SQLite schema analysis
- Interactive HTML dashboards with visualizations
- Real-time database metrics and insights
- Export standalone HTML files

### **Advanced Memory System**
- Semantic search using OpenAI embeddings
- Multi-user session isolation
- Graceful degradation without API keys
- Async operations for performance

### **Tool Recommendation Engine**
- Live web search via Brave Search API
- GitHub integration with repository access
- AI-powered quality scoring and analysis
- Step-by-step installation guides

### **Complete Web Interface**
- Modern Streamlit UI with real-time chat
- Tool selection dashboard (Web Search, GitHub, Python Tools, etc.)
- AI model selection (OpenAI, Claude, Gemini, DeepSeek)
- Live activity tracking and cost monitoring

---

## 📊 **Database Schema**

SQLite tables automatically created:

```sql
-- Chat conversations with metadata
CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    prompt TEXT NOT NULL,
    response TEXT NOT NULL,
    model_used TEXT,
    tools_used TEXT, -- JSON array
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    memory_id TEXT,
    cost REAL DEFAULT 0.0
);

-- Memory entries for semantic search
CREATE TABLE memory_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    memory_id TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    content TEXT NOT NULL,
    metadata TEXT, -- JSON
    status TEXT DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Activity tracking for analytics
CREATE TABLE activity_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    activity_type TEXT NOT NULL,
    description TEXT,
    metadata TEXT, -- JSON
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 💡 **Usage Examples**

### Web Interface
1. Start: `streamlit run docy_search/main_ui.py`
2. Access: `http://localhost:8501`
3. Features: Real-time chat, tool selection, database viewer, dashboard generation

### Memory-Enhanced Conversations
```text
# First conversation
User: "I need React development tools"
Bot: [Provides recommendations] 💾 Memory saved

# Later conversation  
User: "What about state management?"
Bot: ✅ I remember your React project! Here are Redux/Zustand options...
```

### Database Access
- **Web UI**: Dashboard → Database Viewer tab
- **Scripts**: `python scripts/view_chats.py`
- **Direct**: SQLite file at `docy_search.db`
