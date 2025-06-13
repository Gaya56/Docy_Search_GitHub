# Docy Search Repository Analysis

## 🏗️ **Architecture Overview**

**Docy Search** is a comprehensive AI-powered tool recommendation assistant with a modular architecture built around MCP (Model Context Protocol) servers, semantic memory, and a modern web interface.

### Core Components

- **CLI/Web Interface**: `app.py` and `main_ui.py`
- **Tool Recommendation Engine**: `tool_recommendation/` with multiple MCP servers
- **Memory System**: `memory/` with OpenAI embeddings and SQLite storage
- **Database Layer**: `database/` for chat history and activity tracking
- **UI Components**: `ui/` with modular Streamlit components
- **Dashboard System**: `dashboard/` for analytics and reporting

### Key Strengths

✅ **Zero-configuration SQLite database** with automatic schema management  
✅ **Multi-model AI support** (OpenAI, Claude, Gemini, DeepSeek)  
✅ **Semantic memory system** with conversation persistence  
✅ **Modern web interface** with real-time activity tracking  
✅ **Comprehensive documentation** with detailed API reference  
✅ **Modular MCP architecture** for easy extension  

### Repository Structure Analysis

```text
docy_search/
├── __init__.py
├── app.py                     # Main CLI application
├── main_ui.py                 # Streamlit web interface
├── dashboard/                 # Analytics and reporting
│   ├── generator.py
│   └── validators.py
├── database/                  # Data persistence layer
│   ├── connection_manager.py
│   ├── db_manager.py
│   └── explorer.py
├── memory/                    # Semantic memory system
│   ├── cost_tracker.py
│   ├── memory_manager.py
│   └── sqlite_memory.py
├── tool_recommendation/       # MCP servers and tool logic
│   ├── activity_tracker.py
│   ├── brave_search.py
│   ├── github_mcp_server.py
│   ├── mcp_server.py
│   ├── models.py
│   └── python_tools.py
└── ui/                        # Web interface components
    ├── components/
    └── utils/
```

### Technology Stack

- **Backend**: Python 3.12+, SQLite, OpenAI API
- **Frontend**: Streamlit with custom components
- **AI/ML**: OpenAI Embeddings, Multiple LLM providers
- **Data**: SQLite with automatic schema management
- **Architecture**: MCP (Model Context Protocol) servers
