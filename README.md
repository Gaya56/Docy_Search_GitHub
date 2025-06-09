# 🔧 Intelligent Tool Recommendation System with Advanced Memory
**A production-ready AI assistant with persistent memory, semantic search, and dual interfaces (CLI + Web UI)**

## ✅ **Status: FULLY OPERATIONAL with Phase 1 Memory Hardening Complete**

Enterprise-grade memory capabilities with async operations, database migrations, and multi-user support - ready for production deployment and future multi-agent expansion.

## 🚀 **Key Features**

### 🧠 **Advanced Memory System (Phase 1 Complete)**
- ✅ **Async Memory Operations** - Non-blocking saves with `aiosqlite` and `aiofiles`
- ✅ **Database Migration Support** - Automatic schema updates for existing installations
- ✅ **Multi-User Isolation** - Proper user_id indexing and session management
- ✅ **Memory Lifecycle Management** - Compression, archival, and cleanup capabilities
- ✅ **Real OpenAI Embeddings** - Semantic search with `text-embedding-3-small`
- ✅ **Graceful Degradation** - Works perfectly with or without embedding API
- ✅ **Production Error Handling** - Comprehensive retry mechanisms and fallbacks
### 🔧 **Tool Recommendation Engine**
- ✅ **Live Web Search** - Real-time tool discovery via Brave Search API
- ✅ **GitHub Integration** - Official repository access and code examples
- ✅ **AI-Powered Analysis** - Quality scoring and suitability assessment
- ✅ **Installation Guides** - Step-by-step setup instructions
- ✅ **Multi-Category Support** - Web, mobile, desktop, database, DevOps, AI/ML, and more

### 🖥️ **Dual Interface Options**
- ✅ **Command Line Interface** - Fast, lightweight terminal interaction
- ✅ **Streamlit Web UI** - Beautiful, responsive web interface with memory management
- ✅ **Session Persistence** - Conversations continue across restarts
- ✅ **Memory Explorer** - Visual interface for conversation history
- ✅ **Tool Selection Dashboard** - Choose which tools to enable for conversations
- ✅ **AI Model Selection** - Switch between OpenAI, Claude, Gemini, and DeepSeek models

### 📊 **AI-Powered Dashboard Generator (NEW)**
- ✅ **Database Schema Analysis** - Automatic database structure discovery
- ✅ **Intelligent Metrics Generation** - AI-driven KPI and metric identification
- ✅ **Interactive HTML Dashboards** - Beautiful, responsive dashboard creation
- ✅ **Retry Logic & Error Recovery** - Robust handling of network and API failures
- ✅ **Export Functionality** - Download dashboards as standalone HTML files
- ✅ **Real-time Progress Tracking** - Visual feedback during generation process
- ✅ **Multi-User Support** - User-specific dashboard generation and storage

## 🏗️ **Architecture Overview**

```
Docy_Search_GitHub/
├── 🎯 Core Applications
│   ├── docy_search/app.py           # CLI interface with async memory
│   └── docy_search/main_ui.py       # Streamlit web interface
├── 🧠 Memory System (Phase 1 Complete)
│   ├── docy_search/memory/
│   │   ├── sqlite_memory.py         # Async + Sync SQLite operations
│   │   ├── memory_manager.py        # Async memory with OpenAI embeddings
│   │   └── README.md               # Memory system documentation
├── 📊 Dashboard System (NEW)
│   ├── docy_search/dashboard/
│   │   ├── generator.py             # AI-powered dashboard orchestration
│   │   ├── validators.py            # Data validation and schema checking
│   │   └── prompts.py              # AI prompts for dashboard generation
│   └── docy_search/database/
│       ├── sql_agent.py            # Natural language SQL queries
│       └── connection_manager.py   # Database connection with timeout handling
├── 🔧 Tool Recommendation
│   ├── docy_search/tool_recommendation/ # MCP server for tool analysis
│   ├── docy_search/brave_search.py     # Live web search integration
│   ├── docy_search/github_mcp_server.py # GitHub repository access
│   └── docy_search/python_tools.py     # Python-specific tooling
├── 🖥️ User Interface
│   ├── docy_search/ui/components/      # Modular UI components
│   │   ├── dashboard.py            # Dashboard generation interface
│   │   ├── chat.py                 # Chat interface with memory
│   │   ├── memory.py               # Memory management UI
│   │   └── tabs.py                 # Navigation system
├── 📚 Configuration
│   ├── config/                     # Application configuration
│   └── project_context.md          # Project-specific context
└── 🗃️ Data & Storage
    ├── data/memories.db            # SQLite database with async support
    ├── .user_session              # Persistent session tracking
    └── requirements.txt            # Python dependencies
```

## 🚀 **Quick Start**

### Prerequisites
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your API keys: OPENAI_API_KEY, ANTHROPIC_API_KEY, BRAVE_API_KEY, etc.
```

### Option 1: Command Line Interface
```bash
# Activate environment
source .venv/bin/activate

# Run CLI with async memory
python3 docy_search/app.py
```

### Option 2: Web Interface (Recommended)
```bash
# Activate environment
source .venv/bin/activate

# Launch Streamlit UI with memory management
streamlit run docy_search/main_ui.py --server.port 8555
```

### First Time Setup
```bash
# Create project context (optional but recommended)
echo "I'm building a React web application with TypeScript" > project_context.md

# The system will automatically:
# ✅ Initialize async SQLite database with proper schema
# ✅ Create user session with UUID
# ✅ Set up OpenAI embeddings (if API key provided)
# ✅ Apply any necessary database migrations
```

## 🎉 Implementation Success Story

### ✅ Memory System: From Concept to Reality

The intelligent memory system has been **successfully implemented and integrated** with the following achievements:

**🏗️ Complete 3-Layer Architecture:**
- **SQLiteMemory**: Production-ready database layer with JSON serialization and proper indexing
- **MemoryManager**: AI-powered memory management with real OpenAI `text-embedding-3-small` embeddings  
- **Integration**: Seamless app.py integration with comprehensive error handling

**🧠 Real AI Features Working:**
- ✅ **Semantic Search**: Live OpenAI embeddings with cosine similarity calculations
- ✅ **Persistent Sessions**: User sessions survive app restarts via `.user_session` file
- ✅ **Context Loading**: Previous memories automatically loaded into agent context
- ✅ **Smart Saving**: Significant interactions (>100 chars) automatically stored

**🛡️ Production-Grade Safety:**
- ✅ **Zero Breaking Changes**: Existing functionality unchanged and fully backward compatible
- ✅ **Graceful Degradation**: App works perfectly with or without memory/embeddings
- ✅ **Error Isolation**: All memory operations wrapped in try/catch with silent fallbacks
- ✅ **Privacy First**: All data stored locally in SQLite, never shared externally

**📊 Real Testing Results:**
- ✅ Successfully tested with actual OpenAI API integration
- ✅ Memory save/retrieve cycle working with real embeddings
- ✅ Session persistence confirmed across app restarts
- ✅ Error handling validated for all failure scenarios

**The memory system transforms conversations from stateless interactions into intelligent, contextual dialogues that improve over time.**

## 💡 Usage Examples

### 🌐 **Web Interface (Streamlit)**

1. **Start the Web UI:**
   ```bash
   streamlit run docy_search/main_ui.py --server.port 8555
   ```

2. **Access in Browser:**
   - Open: `http://localhost:8555`
   - Beautiful chat interface with real-time responses
   - Memory status indicators in sidebar
   - Session persistence across browser sessions
   - **Tool Selection Dashboard** - Choose which tools to enable
   - **AI Model Selection** - Switch between different AI models
   - **Live Activity Tracking** - Monitor tool usage and API costs

### 🖥️ **Command Line Interface**

1. **Start Terminal Chat:**
   ```bash
   python docy_search/app.py
   ```

### 🧠 Memory-Enhanced Interactions (Both Interfaces)

```text
# First conversation
User: "I need tools for React development"
Bot: I'll search for React development tools and analyze the best options...
     💾 Memory saved (ID: 1)

# Later conversation (same session or after restart)
User: "What about state management?"
Bot: ✅ I remember you're working with React! Based on our previous discussion...
     [Provides Redux, Zustand, Context API recommendations specific to React]
     💾 Memory saved (ID: 2)

# Even later
User: "Now I need testing tools"
Bot: Given your React project with Redux (from our earlier conversations)...
     [Suggests Jest, React Testing Library, Cypress for React/Redux stack]
```

### Tool Discovery & Recommendations

```text
User: "I need tools for React web development"
Bot: I'll search for React development tools and analyze the best options...

User: "Compare Vue.js vs Angular"
Bot: I'll provide a detailed comparison of these JavaScript frameworks...

User: "How do I set up a Django project?"
Bot: I'll generate step-by-step setup instructions for Django development...
```

### GitHub Integration

```text
User: "Find the official React repository and show me setup examples"
Bot: I can search GitHub repositories for React setup examples. This will access public GitHub data to find official repositories and code examples. Continue? (y/n)

User: "y"
Bot: [Shows React repository details, stars, and relevant setup files]
```

### Development Workflows

```text
User: "What's the best database for a Node.js project?"
Bot: I'll recommend databases that work well with Node.js and provide setup guides...

User: "Set up a complete full-stack development environment"
Bot: I'll suggest tools and provide setup instructions for frontend, backend, and database tools...
```

### Project Context-Aware Recommendations

```text
User: "What tools would be best for this project?"
Bot: ✅ I have your project context loaded and ready to help!
     Based on your task management app with React + Node.js + PostgreSQL...
     [Provides targeted recommendations for your specific stack and challenges]
```

## 🔧 Advanced Features

### Tool Selection Dashboard

The Streamlit interface includes an interactive tool selection dashboard where you can:

- **🔍 Web Search** - Enable/disable live web search for development tools
- **🐙 GitHub Integration** - Toggle GitHub repository access and code examples  
- **🐍 Python Tools** - Control Python-specific development utilities
- **🎯 Tool Recommendation** - Enable AI-powered tool analysis and recommendations
- **📊 Data Visualization** - Toggle chart and visualization capabilities

**Quick Presets:**
- **🚀 All Tools** - Enable all available tools for maximum capability
- **⚡ Essential Only** - Enable only web search and tool recommendations for faster responses

### AI Model Selection

Choose your preferred AI model based on your needs:

- **OpenAI GPT-4o Mini** - Fast and efficient for general tasks (Low cost, Fast speed)
- **Claude 3 Opus** - Excellent for complex reasoning (High cost, Medium speed)
- **Google Gemini 1.5 Flash** - Great for analysis and code generation (Medium cost, Fast speed)
- **DeepSeek Chat** - Cost-effective alternative (Very low cost, Medium speed)

The interface shows real-time cost and speed information to help you make the best choice for your use case.

### Tool Categories

- **Web Development**: React, Vue.js, Angular, Django, Flask, Express.js
- **Mobile Development**: React Native, Flutter, Xamarin, Ionic
- **Desktop Applications**: Electron, Tauri, Qt, .NET
- **Databases**: PostgreSQL, MongoDB, Redis, MySQL, SQLite
- **DevOps**: Docker, Kubernetes, Jenkins, GitLab CI, Terraform
- **Testing**: Jest, Pytest, Selenium, Cypress, Postman
- **Design**: Figma, Sketch, Adobe XD, Canva, GIMP
- **Data Science**: Pandas, NumPy, Jupyter, Tableau, Power BI
- **AI/ML**: TensorFlow, PyTorch, Scikit-learn, Keras
- **Game Development**: Unity, Unreal Engine, Godot, Phaser
- **Security**: OWASP tools, security scanners, encryption libraries
- **Productivity**: VS Code, Git, Slack, Notion, Trello

### AI-Powered Analysis

Each tool recommendation includes:

- **Relevance Score** (1-10)
- **Reliability Assessment**
- **Installation Complexity** (Easy/Medium/Hard)
- **Community Support Rating**
- **Security & Trust Evaluation**
- **Use Case Scenarios**

### Integration Benefits

- **Live Data**: Always current tool information via Brave Search
- **Smart Analysis**: AI evaluates beyond simple search results
- **Practical Focus**: Real installation guides and usage tips
- **Skill-Adaptive**: Recommendations match user experience level
- **Development-Focused**: Tailored for software development workflows

## 📁 File Structure

```text
Docy_Search/
├── docy_search/
│   ├── app.py                              # Main application with memory integration (CLI)
│   ├── main_ui.py                          # 🆕 Streamlit Web UI for the assistant
│   ├── activity_tracker.py                 # 🆕 Real-time activity and cost tracking
│   ├── memory/                             # 🆕 Intelligent Memory System
│   │   ├── memory_manager.py              # 🆕 AI-powered memory operations with embeddings
│   │   ├── sqlite_memory.py               # 🆕 SQLite database operations for persistence
│   │   ├── cost_tracker.py                # 🆕 API cost tracking and optimization
│   │   ├── __init__.py                    # 🆕 Memory system exports
│   │   └── README.md                      # 🆕 Complete memory system documentation
│   ├── dashboard/                          # 🆕 AI-Powered Dashboard System
│   │   ├── generator.py                   # 🆕 Dashboard orchestration and generation
│   │   ├── validators.py                  # 🆕 Data validation and schema checking
│   │   └── prompts.py                     # 🆕 AI prompts for dashboard generation
│   ├── database/                          # 🆕 Database Integration
│   │   ├── sql_agent.py                   # 🆕 Natural language SQL queries
│   │   ├── sql_agent_simple.py           # 🆕 Simplified SQL operations
│   │   └── connection_manager.py          # 🆕 Database connection management
│   ├── tool_recommendation/               # 🆕 Tool Analysis Engine
│   │   ├── mcp_server.py                  # Core recommendation engine
│   │   ├── search_engine.py               # Search functionality
│   │   ├── analyzer.py                    # AI analysis tools
│   │   ├── installer.py                   # Installation guides
│   │   ├── core.py                        # Core logic
│   │   └── models.py                      # Data models
│   ├── ui/                                # 🆕 Streamlit UI Components
│   │   ├── components/                    # Modular UI components
│   │   │   ├── chat.py                    # Chat interface with memory
│   │   │   ├── dashboard.py               # Dashboard generation interface
│   │   │   ├── memory.py                  # Memory management UI
│   │   │   ├── sidebar.py                 # Navigation sidebar
│   │   │   └── tabs.py                    # Tab navigation system
│   │   └── utils/                         # UI utilities
│   │       └── styles.py                  # Styling and theming
│   ├── github_mcp_server.py               # GitHub repository integration
│   ├── brave_search.py                    # Search API integration
│   └── python_tools.py                    # Utility functions
├── config/                                # 🆕 Application Configuration
│   ├── __init__.py                        # Configuration exports
│   └── settings.py                        # Application settings
├── data/                                  # 🆕 Data storage
│   └── memories.db                        # 🆕 SQLite database for conversation history
├── .user_session                          # 🆕 Persistent user session ID
├── project_context.md                     # Your project details (auto-loaded)
├── requirements.txt                       # Dependencies (including memory system + Streamlit)
├── pyproject.toml                         # 🆕 Modern Python project configuration
├── uv.lock                               # 🆕 Dependency lock file
└── .env                                  # API keys (create this)
```

## 🤝 Contributing

This project uses a modular MCP (Model Context Protocol) architecture. To add new functionality:

1. Create new MCP server in `docy_search/` directory
2. Follow the existing pattern (see `docy_search/tool_recommendation/mcp_server.py` or `docy_search/github_mcp_server.py`)
3. Add server to `docy_search/app.py`
4. Update system prompt if needed

### Key Components:

- **MCP Servers**: Modular tools for specific functionality (tool search, GitHub integration, etc.)
- **Project Context**: Automatic loading of user project details for targeted recommendations
- **Permission System**: User consent required for external API calls (GitHub, web search)
- **Multi-AI Support**: Flexible AI model selection for different use cases

For detailed implementation information, explore the codebase in the `docy_search/` directory.

## 🎯 System Capabilities

### ✅ Fully Implemented Features

- **🧠 Intelligent Memory**: ✅ **OPERATIONAL** - Persistent conversation history with semantic search using OpenAI embeddings
- **🌐 Web Interface**: ✅ **OPERATIONAL** - Beautiful Streamlit UI with real-time chat and memory indicators
- **🔧 Tool Selection Dashboard**: ✅ **OPERATIONAL** - Interactive tool selection with quick presets and live configuration
- **🤖 AI Model Selection**: ✅ **OPERATIONAL** - Dynamic model switching with cost/speed information
- **📊 Live Activity Tracking**: ✅ **OPERATIONAL** - Real-time monitoring of tool usage and API costs
- **🖥️ CLI Interface**: ✅ **OPERATIONAL** - Command line interface for terminal users
- **🔍 Tool Discovery**: ✅ **OPERATIONAL** - Live web search with AI-powered analysis
- **📊 Smart Rankings**: ✅ **OPERATIONAL** - Multi-criteria tool evaluation and comparison
- **📚 Installation Guides**: ✅ **OPERATIONAL** - Automatic generation of setup instructions
- **🐙 GitHub Integration**: ✅ **OPERATIONAL** - Repository search, code examples, and project analysis
- **🎯 Context Awareness**: ✅ **OPERATIONAL** - Project-specific recommendations based on your details
- **🔐 Permission System**: ✅ **OPERATIONAL** - Secure API access with user consent
- **🤖 Multi-AI Support**: ✅ **OPERATIONAL** - OpenAI, Claude, Gemini, and DeepSeek compatibility
- **📱 Category Support**: ✅ **OPERATIONAL** - Web, mobile, desktop, database, DevOps, testing, design, data science, AI/ML, game development, security, productivity

### 🚀 Ready to Use - Enhanced Web Interface with Tool & Model Selection!

Your intelligent development assistant now features a **fully customizable interface** with:

- **🔧 Tool Selection Dashboard** - Choose exactly which tools to enable for each conversation
- **🤖 Dynamic AI Model Selection** - Switch between OpenAI, Claude, Gemini, and DeepSeek in real-time
- **📊 Live Activity & Cost Tracking** - Monitor tool usage and API costs with automatic refresh
- **🧠 Persistent Memory** - All conversations saved with semantic search using OpenAI embeddings
- **🌐 Beautiful Web Interface** - Responsive Streamlit UI with real-time configuration

Choose your experience:

- **🌐 Web Interface**: Run `streamlit run main_ui.py --server.port 8555` for the enhanced browser experience with tool selection
- **🖥️ Command Line**: Run `python app.py` for traditional terminal-based interaction

The web interface lets you customize your AI assistant on-the-fly - select only the tools you need, choose the AI model that fits your budget and speed requirements, and watch real-time activity as your assistant works. Every conversation builds your personalized knowledge base that makes each interaction smarter than the last!

