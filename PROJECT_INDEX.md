# 📋 Docy Search Project Index

**Complete navigation guide for the intelligent tool recommendation system with modular Streamlit UI**

## 🎯 **Main Applications**

### **main_ui.py** - *Streamlit Web Interface (209 lines)*
- `initialize_session_state()` - Initialize all session state variables and user sessions
- `get_project_context()` - Load and cache project context (decorated with @st.cache_data)
- `display_sidebar()` - Render enhanced sidebar with live activity tracking
- `display_configuration_banner()` - Show current tool/model configuration status
- `display_footer()` - Render application footer with help captions
- `get_cached_agent()` - Create or retrieve cached AI agent based on current settings
- `main()` - Main Streamlit application entry point with modular component integration

### **app.py** - *CLI Interface with Memory Integration (266 lines)*
- `TOOL_SERVER_MAP` - Maps tool keys to MCP server instances with prefixes
- `create_agent_with_context()` - Create AI agent with project context and selected tools
- `get_model_from_name()` - Get appropriate AI model (OpenAI, Claude, Gemini, DeepSeek)
- `load_project_context()` - Load project-specific context from markdown file
- `handle_conversation()` - Main CLI conversation loop with memory integration
- `main()` - CLI entry point with argument parsing and session management

---

## 🧠 **Memory System** *(Phase 1 Complete - Production Ready)*

### **memory/memory_manager.py** - *AI-Powered Memory with Embeddings*
- `MemoryManager` class - Main memory orchestration with OpenAI embeddings
  - `save_memory()` - Save conversation with metadata and embeddings
  - `search_memories()` - Semantic search using cosine similarity
  - `get_context()` - Retrieve relevant memories for current conversation
  - `cleanup_old_memories()` - Automatic memory lifecycle management

### **memory/sqlite_memory.py** - *Database Layer*
- `SQLiteMemory` class - Production SQLite operations with JSON serialization
  - `save_memory()` - Store memory with proper indexing
  - `search_memories()` - Query memories by user/category/embeddings
  - `get_user_memories()` - Retrieve user-specific memory history
  - `delete_memory()` - Remove specific memories
  - `get_memory_stats()` - Usage statistics and analytics

### **memory/cost_tracker.py** - *API Cost Monitoring*
- `CostTracker` class - Track OpenAI API usage and costs
  - `track_tokens()` - Count tokens using tiktoken
  - `get_daily_cost()` - Calculate daily API expenses
  - `get_monthly_cost()` - Calculate monthly API expenses
  - `estimate_cost()` - Estimate cost before API calls

---

## 🎨 **Modular UI Components**

### **ui/components/sidebar.py** - *Sidebar Management (464 lines)*
- `SidebarComponent` class - Complete sidebar functionality
  - `render()` - Main sidebar rendering with configuration change detection
  - `_render_activity_section()` - Live activity tracking display
  - `_render_resource_access()` - API and resource usage metrics
  - `_render_cost_tracking()` - Real-time cost monitoring (fixed for Streamlit)
  - `_render_session_info()` - Session details and model information
  - `_render_controls()` - Tool selection and model selection controls
  - `_render_memory_management()` - Memory statistics and maintenance
  - `_render_tool_selection()` - Interactive tool enable/disable checkboxes

### **ui/components/chat.py** - *Chat Interface (121 lines)*
- `ChatComponent` class - Chat interaction management
  - `render()` - Main chat interface with history and input
  - `_handle_message()` - Process user messages and get AI responses
  - `_get_response()` - Async AI response generation
  - `_build_context()` - Build conversation context with memory
  - `_show_active_tools()` - Display currently enabled tools
  - `_render_welcome()` - Welcome message for new users
  - `add_assistant_message()` - Add AI responses to chat history

### **ui/components/memory.py** - *Memory Operations (111 lines)*
- `MemoryComponent` class - Memory save operations and status
  - `save_memory()` - Save interaction to memory (fixed for Streamlit compatibility)
  - `render_memory_status()` - Display memory save status indicators

### **ui/utils/styles.py** - *CSS Styling System*
- `get_main_styles()` - Core application styles (headers, cards, metrics)
- `get_chat_styles()` - Chat-specific styles (messages, welcome, status)
- `get_sidebar_styles()` - Sidebar styles (metrics, tool selection, model selection)
- `get_responsive_styles()` - Mobile and tablet responsive design
- `inject_all_styles()` - Combine and inject all CSS into Streamlit

---

## 🔧 **Tool Recommendation Engine**

### **tool_recommendation/mcp_server.py** - *MCP Server for Tool Analysis*
- `search_tools()` - Search for development tools using enhanced queries
- `analyze_tools()` - AI-powered tool analysis and ranking
- `get_installation_guide()` - Generate installation instructions
- `compare_tools()` - Side-by-side tool comparisons
- `get_tool_alternatives()` - Find alternative tools for specific use cases

### **tool_recommendation/models.py** - *Data Models*
- `ToolCategory` enum - Tool categories (cybersecurity, development, networking, etc.)
- `Platform` enum - Target platforms (Windows, macOS, Linux, Docker)
- `InstallationMethod` enum - Installation methods (package manager, source, etc.)
- `ToolRecommendation` model - Complete tool information with scoring
- `SearchQuery` model - Enhanced search parameters
- `RecommendationResponse` model - Structured recommendation results

### **tool_recommendation/search_engine.py** - *Enhanced Search*
- `BraveSearchEngine` class - Brave API integration for tool discovery
- `SearchResultEnhancer` class - AI-powered search result improvement

### **tool_recommendation/analyzer.py** - *AI Analysis*
- `GeminiToolAnalyzer` class - Google Gemini API for tool analysis
- `analyze_search_results()` - Analyze and rank search results
- `_create_analysis_request()` - Generate AI analysis prompts

### **tool_recommendation/installer.py** - *Installation Guides*
- `InstallationGuideGenerator` class - Generate platform-specific install guides
- `generate_guide()` - Create detailed installation instructions
- `_determine_best_method()` - Choose optimal installation method

### **tool_recommendation/core.py** - *System Orchestration*
- `ToolRecommendationSystem` class - Main system coordinator
- `get_recommendations()` - End-to-end recommendation pipeline
- `RecommendationFormatter` class - Format results for display

---

## 🌐 **External Integrations**

### **brave_search.py** - *Web Search Integration*
- `search_web()` - Brave Search API integration for real-time tool discovery
- `get_search_results()` - Enhanced search with filtering and ranking

### **github_mcp_server.py** - *GitHub Repository Access*
- `search_repositories()` - Search GitHub for official tool repositories
- `get_repository_info()` - Fetch repository details, stars, and examples
- `get_code_examples()` - Extract relevant code samples and setup files

### **python_tools.py** - *Python Development Utilities*
- `python_repl()` - Interactive Python code execution
- `install_package()` - Dynamic package installation
- `run_script()` - Execute Python scripts and return results

---

## 📊 **Monitoring & Analytics**

### **activity_tracker.py** - *Live Activity Tracking*
- `activity_tracker` singleton - Global activity monitoring
- `track_tool_usage()` - Log tool usage with timestamps
- `track_api_call()` - Monitor API calls and costs
- `get_activity_summary()` - Generate usage statistics
- `get_resource_usage()` - Track files, websites, repos accessed

---

## 🗃️ **Data & Configuration**

### **project_context.md** - *Project-Specific Context*
- User's project description and requirements
- Automatically loaded into AI agent context
- Used for targeted tool recommendations

### **data/memories.db** - *SQLite Database*
- Persistent conversation storage
- User sessions and memory embeddings
- Automated schema migrations

### **.user_session** - *Session Persistence*
- Unique user ID for memory isolation
- Survives application restarts
- Enables cross-session conversation continuity

### **requirements.txt** - *Dependencies*
- Core: `streamlit`, `pydantic-ai`, `asyncio`
- AI Models: `openai`, `anthropic`, `google-generativeai`
- Memory: `aiosqlite`, `numpy`, `tiktoken`
- Search: `aiohttp`, `requests`
- Database: `sqlite3`, `json`

---

## 🧪 **Testing & Development**

### **test_modular.py** - *Modular Component Testing*
- `test_imports()` - Verify all UI components import correctly
- `test_component_instantiation()` - Test component creation
- `test_main_ui_structure()` - Validate main application structure

---

## 🔄 **Key Integration Points**

### **Session State Management**
- **main_ui.py**: Central session state initialization
- **ui/components/**: Component-specific state management
- **memory/**: Persistent session tracking across restarts

### **AI Model Integration**
- **app.py**: `TOOL_SERVER_MAP` with unique prefixes to prevent conflicts
- **ui/components/sidebar.py**: Model selection UI
- **main_ui.py**: Cached agent creation based on current settings

### **Memory Integration Flow**
1. **Chat Component** → User interaction
2. **Memory Component** → Save significant conversations
3. **Memory Manager** → OpenAI embeddings + SQLite storage
4. **Context Loading** → Previous memories loaded into agent context

### **Tool Conflict Resolution**
- **Fixed**: Added `tool_prefix` to all MCP servers in `TOOL_SERVER_MAP`
- **Result**: `py_python_repl`, `viz_python_repl`, `web_search`, `rec_analyze_tools`
- **Benefit**: No more tool name conflicts between servers

### **Async Operation Handling**
- **Fixed**: Simplified memory saving to avoid Streamlit cancel scope conflicts
- **Fixed**: Removed problematic async cost tracking in sidebar
- **Result**: Stable operation without asyncio errors

---

## 🚀 **Quick Navigation Tips**

- **Main Entry Points**: `main_ui.py` (Web) or `app.py` (CLI)
- **UI Customization**: `ui/utils/styles.py` for CSS modifications
- **New Tool Integration**: Add to `TOOL_SERVER_MAP` in `app.py`
- **Memory Debugging**: Check `memory/memory_manager.py` and `data/memories.db`
- **Component Issues**: Individual components in `ui/components/`
- **API Integration**: External services in root-level Python files

---

## 📋 **Development Status**

✅ **Fully Operational Features:**
- Modular Streamlit UI with clean component separation
- Advanced memory system with OpenAI embeddings
- Multi-AI model support (OpenAI, Claude, Gemini, DeepSeek)
- Live tool recommendation with web search
- Session persistence across restarts
- Real-time activity and cost tracking
- Tool conflict resolution with prefixes

🔧 **Fixed Issues:**
- ✅ AsyncIO cancel scope conflicts resolved
- ✅ Tool name conflicts resolved with prefixes
- ✅ Missing dependencies (tiktoken, aiohttp) installed
- ✅ Streamlit-compatible async operations implemented

🎯 **Ready for Production:**
The system is fully functional with comprehensive error handling, modular architecture, and production-ready memory capabilities.
