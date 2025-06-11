# Components Guide

This guide explains the core modules and their responsibilities in the Docy Search application.

## 📁 Project Structure

```
docy_search/
├── __init__.py                 # Package initialization
├── app.py                      # Main CLI application
├── main_ui.py                  # Streamlit web interface
├── tool_recommendation/        # Tool discovery and analysis system
│   ├── __init__.py
│   ├── activity_tracker.py     # Real-time activity monitoring
│   ├── analyzer.py             # AI-powered tool analysis
│   ├── brave_search.py         # Web search MCP server
│   ├── core.py                 # Core recommendation logic
│   ├── github_mcp_server.py    # GitHub integration MCP server
│   ├── mcp_server.py           # Main tool recommendation MCP server
│   ├── models.py               # Pydantic data models
│   ├── python_tools.py         # Python execution MCP server
│   └── search_engine.py        # Enhanced search engine
├── memory/                     # Semantic memory system
│   ├── __init__.py
│   ├── cost_tracker.py         # API usage cost tracking
│   ├── memory_manager.py       # Main memory management
│   └── sqlite_memory.py        # SQLite memory storage
├── database/                   # Database management
│   ├── __init__.py
│   ├── connection_manager.py   # MCP SQLite connections
│   ├── db_manager.py           # Database operations
│   └── explorer.py             # Database exploration tools
├── dashboard/                  # Analytics and reporting
│   ├── __init__.py
│   ├── generator.py            # Dashboard generation
│   └── validators.py           # Data validation
└── ui/                        # User interface components
    ├── __init__.py
    ├── components/            # Reusable UI components
    │   ├── __init__.py
    │   ├── chat.py            # Chat interface
    │   ├── dashboard.py       # Dashboard UI
    │   ├── memory.py          # Memory management UI
    │   └── sidebar.py         # Sidebar controls
    └── utils/                 # UI utilities
        ├── __init__.py
        └── styles.py          # CSS styling
```

## 🎯 Core Application

### `app.py` - Main CLI Application
**Purpose**: Command-line interface and core agent management.

**Key Components**:
- **Agent Creation**: `create_agent_with_context()` - Builds Pydantic AI agents with MCP servers
- **Model Management**: `get_model_from_name()` - Creates AI model instances
- **Tool Server Mapping**: `TOOL_SERVER_MAP` - Maps tool names to MCP server factories
- **Project Context**: `load_project_context()` - Loads project-specific context from file

**Responsibilities**:
- Initialize and configure AI models (OpenAI, Claude, Gemini, DeepSeek)
- Set up MCP (Model Context Protocol) servers for tool integration
- Manage tool selection and filtering
- Provide CLI interface for direct interaction
- Handle memory integration and user session management

**Key Features**:
- Dynamic tool selection based on user preferences
- Memory-enhanced conversations with context retrieval
- Graceful error handling for missing API keys
- Support for multiple AI model providers

### `main_ui.py` - Streamlit Web Interface
**Purpose**: Modern web interface for the application.

**Key Components**:
- **Session Management**: User ID generation and persistence
- **UI Coordination**: Manages sidebar, chat, and dashboard components
- **Database Integration**: Logs conversations and tracks activity
- **Configuration Management**: Handles tool selection and model switching

**Responsibilities**:
- Provide intuitive web interface using Streamlit
- Manage user sessions and state persistence
- Coordinate between different UI components
- Handle real-time updates and auto-refresh
- Display configuration status and error messages

---

## 🛠 Tool Recommendation System

### `tool_recommendation/` - Tool Discovery Engine

#### `mcp_server.py` - Main Tool Recommendation Server
**Purpose**: Core MCP server providing tool search and analysis capabilities.

**MCP Tools Provided**:
- `search_tools()`: Search for development tools by category
- `analyze_tools()`: AI-powered analysis and ranking
- `recommend_tools_for_task()`: Task-specific tool recommendations
- `compare_tools()`: Side-by-side tool comparisons
- `get_installation_guide()`: Step-by-step installation instructions

**Features**:
- Category-specific search optimization
- AI-powered quality scoring and analysis
- Real-time web search integration
- Comprehensive installation guides with troubleshooting

#### `github_mcp_server.py` - GitHub Integration
**Purpose**: Provides access to GitHub repositories and code examples.

**MCP Tools Provided**:
- `search_github_repositories()`: Search for repositories by topic and language
- `get_repository_structure()`: Analyze repository file structure
- `get_file_from_repository()`: Retrieve specific file contents

**Features**:
- Official repository discovery
- Code example access
- File structure analysis
- Rate limit management with optional GitHub token

#### `brave_search.py` - Web Search Integration
**Purpose**: Live web search capabilities via Brave Search API.

**MCP Tools Provided**:
- `search_web()`: General web search with filtering

**Features**:
- Real-time web search with relevance filtering
- Configurable result count and freshness
- Formatted output with titles, URLs, and descriptions
- Activity tracking integration

#### `python_tools.py` - Python Code Execution
**Purpose**: Execute Python code and generate visualizations.

**MCP Tools Provided**:
- `python_repl()`: Execute Python code in persistent environment
- `data_visualization()`: Create charts and graphs with matplotlib

**Features**:
- Persistent Python environment with state
- Matplotlib integration for data visualization
- Safe code execution with error handling
- Base64 image encoding for web display

#### `activity_tracker.py` - Real-time Monitoring
**Purpose**: Track tool usage and provide live activity updates.

**Key Components**:
- **Activity Management**: Start, update, and complete activities
- **Progress Tracking**: Real-time progress indicators
- **Resource Monitoring**: Track files, websites, and API calls accessed
- **Performance Metrics**: Duration and success rate tracking

**Features**:
- Live activity updates in the UI
- Resource usage analytics
- Error tracking and reporting
- Activity history and trends

#### `analyzer.py` - AI-Powered Analysis
**Purpose**: Uses Gemini AI to analyze and rank tool search results.

**Key Components**:
- **GeminiToolAnalyzer**: Main analysis engine
- **Quality Scoring**: Relevance, reliability, and ease-of-use scoring
- **Tool Identification**: Distinguish actual tools from articles/tutorials
- **Recommendation Generation**: Structured recommendations with reasoning

#### `models.py` - Data Models
**Purpose**: Pydantic models for type safety and data validation.

**Key Models**:
- `ToolRecommendation`: Complete tool information with scores
- `SearchQuery`: Search parameters and filters
- `RecommendationResponse`: Full response with metadata
- `ToolCategory`: Enum of available categories
- `Platform`: Supported operating systems
- `InstallationMethod`: Available installation approaches

#### `search_engine.py` - Enhanced Search
**Purpose**: Advanced search engine with multi-query optimization.

**Key Components**:
- **BraveSearchEngine**: Main search client with async support
- **Query Enhancement**: Generate multiple targeted search queries
- **Result Filtering**: Remove irrelevant content and duplicates
- **Relevance Scoring**: Extract indicators for tool quality assessment

#### `core.py` - Recommendation Orchestration
**Purpose**: Coordinates the entire recommendation process.

**Key Components**:
- **ToolRecommendationSystem**: Main orchestration class
- **Multi-step Pipeline**: Search → Enhancement → Analysis → Formatting
- **Performance Optimization**: Async operations and caching
- **Error Handling**: Graceful degradation and retry logic

---

## 🧠 Memory System

### `memory/` - Semantic Memory Management

#### `memory_manager.py` - Core Memory Management
**Purpose**: Central memory management with semantic search capabilities.

**Key Components**:
- **MemoryManager**: Main synchronous interface
- **AsyncMemoryManager**: Asynchronous operations for UI
- **Embedding Integration**: OpenAI embeddings for semantic search
- **User Isolation**: Separate memory spaces per user

**Features**:
- Semantic similarity search using embeddings
- Memory compression and archival
- Category-based organization
- User session isolation
- Graceful degradation without API keys

#### `sqlite_memory.py` - Storage Implementation
**Purpose**: SQLite-based memory storage with both sync and async support.

**Key Components**:
- **DatabaseMixin**: Shared functionality
- **SQLiteMemory**: Synchronous operations
- **AsyncSQLiteMemory**: Asynchronous operations
- **Schema Management**: Automatic table creation and indexing

**Features**:
- Automatic database initialization
- Efficient indexing for fast retrieval
- Memory lifecycle management (active, compressed, archived)
- Access pattern tracking
- Connection pooling and optimization

#### `cost_tracker.py` - API Usage Monitoring
**Purpose**: Track and analyze API usage costs across different models.

**Key Components**:
- **CostTracker**: Main cost tracking class
- **Model Pricing**: Per-token pricing for different AI models
- **Usage Analytics**: Daily, monthly, and user-specific tracking
- **Cost Optimization**: Recommendations for cost reduction

**Features**:
- Real-time cost calculation
- Model-specific pricing
- Usage pattern analysis
- Cost alerts and budgeting
- Historical cost tracking

---

## 🗄 Database System

### `database/` - Data Persistence Layer

#### `db_manager.py` - Database Operations
**Purpose**: Main database interface for all data operations.

**Key Components**:
- **DatabaseManager**: Main database class
- **Schema Management**: Automatic table creation and migration
- **Data Access**: CRUD operations for all data types
- **Statistics**: Database analytics and reporting

**Features**:
- Zero-configuration SQLite setup
- Automatic schema creation and updates
- Chat history persistence
- Activity logging
- Memory entry storage
- Export capabilities (CSV, JSON)

#### `connection_manager.py` - MCP SQLite Integration
**Purpose**: Manages MCP server connections for database tools.

**Key Components**:
- **MCPSQLiteConnection**: MCP server connection management
- **Parameter Configuration**: Server setup and configuration
- **Session Management**: Connection lifecycle management

**Features**:
- MCP SQLite server integration
- Automatic database path configuration
- Connection pooling and optimization
- Error handling and recovery

#### `explorer.py` - Database Exploration
**Purpose**: Tools for exploring and analyzing database contents.

**Key Components**:
- **Table Information**: Schema and statistics display
- **Data Browsing**: Interactive data exploration
- **Export Tools**: Data export in various formats

**Features**:
- Interactive database browser
- Table statistics and metadata
- Query execution interface
- Data export and backup

---

## 📊 Dashboard System

### `dashboard/` - Analytics and Reporting

#### `generator.py` - Dashboard Generation
**Purpose**: AI-powered dashboard creation from database data.

**Key Components**:
- **DashboardGenerator**: Main dashboard creation engine
- **Chart Generation**: Interactive visualizations with Plotly
- **Data Analysis**: Statistical analysis of usage patterns
- **Report Generation**: Comprehensive analytics reports

**Features**:
- Automatic chart generation from data
- Interactive visualizations
- Performance metrics and trends
- User behavior analysis
- Exportable HTML dashboards

#### `validators.py` - Data Validation
**Purpose**: Ensure data quality and integrity for dashboard generation.

**Key Components**:
- **Data Validation**: Schema and content validation
- **Quality Checks**: Data completeness and accuracy
- **Error Reporting**: Detailed validation error messages

**Features**:
- Comprehensive data validation
- Quality assurance checks
- Error reporting and logging
- Data cleaning recommendations

---

## 🎨 User Interface System

### `ui/` - Web Interface Components

#### `components/chat.py` - Chat Interface
**Purpose**: Interactive chat interface with AI agent integration.

**Key Components**:
- **ChatComponent**: Main chat interface class
- **Message Management**: Chat history and state management
- **Agent Integration**: Seamless AI agent communication
- **Tool Feedback**: Real-time tool usage indicators

**Features**:
- Real-time chat interface
- Message history persistence
- Tool activity indicators
- Memory status display
- Welcome messages and help text

#### `components/sidebar.py` - Sidebar Controls
**Purpose**: Configuration and control panel for the application.

**Key Components**:
- **SidebarComponent**: Main sidebar management
- **Tool Selection**: Dynamic tool enabling/disabling
- **Model Configuration**: AI model selection and switching
- **Activity Monitoring**: Live activity tracking display
- **Memory Management**: Memory statistics and controls

**Features**:
- Dynamic tool selection
- AI model switching
- Live activity monitoring
- Memory management controls
- Cost tracking display
- Session information
- Development tools

#### `components/dashboard.py` - Dashboard Interface
**Purpose**: Dashboard generation and database viewing interface.

**Key Components**:
- **DashboardComponent**: Main dashboard interface
- **Database Viewer**: Interactive data browsing
- **Export Tools**: Data export functionality
- **Chart Display**: Visualization rendering

**Features**:
- AI-powered dashboard generation
- Interactive database viewer
- Data export capabilities (CSV, JSON)
- Real-time database statistics
- Chart visualization and export

#### `components/memory.py` - Memory Management UI
**Purpose**: User interface for memory operations and management.

**Key Components**:
- **MemoryComponent**: Memory interface management
- **Save Operations**: Memory saving with user feedback
- **Status Display**: Memory operation status indicators

**Features**:
- Automatic memory saving
- User feedback on memory operations
- Memory status indicators
- Error handling and reporting

#### `utils/styles.py` - CSS Styling
**Purpose**: Consistent styling and theming for the web interface.

**Key Components**:
- **Style Injection**: Streamlit CSS customization
- **Responsive Design**: Mobile and desktop optimization
- **Theme Management**: Consistent color schemes and typography
- **Component Styling**: Specific styles for UI components

**Features**:
- Modern, professional styling
- Responsive design for all screen sizes
- Consistent color scheme and typography
- Custom component styling
- Animation and transition effects

---

## 🔧 Configuration System

### `config/` - Application Configuration

#### `settings.py` - Settings Management
**Purpose**: Centralized configuration using Pydantic settings.

**Key Components**:
- **APISettings**: API keys and endpoints
- **DatabaseSettings**: Database configuration
- **UISettings**: User interface preferences
- **AppSettings**: Main application settings

**Features**:
- Environment variable integration
- Validation and type checking
- Default value management
- Settings caching and optimization
- Configuration validation

---

## 🔄 Data Flow

### Request Processing Flow
1. **User Input** → Streamlit UI or CLI
2. **Session Management** → User ID and state tracking
3. **Agent Creation** → Dynamic agent with selected tools
4. **Tool Execution** → MCP servers for specific capabilities
5. **AI Processing** → Model-specific analysis and generation
6. **Memory Integration** → Semantic storage and retrieval
7. **Database Logging** → Persistent storage of interactions
8. **Response Delivery** → Formatted output to user

### Memory Flow
1. **Content Analysis** → Determine if content should be saved
2. **Embedding Generation** → OpenAI embeddings for semantic search
3. **Storage** → SQLite database with metadata
4. **Retrieval** → Semantic similarity search for relevant memories
5. **Context Integration** → Include memories in agent context
6. **Maintenance** → Compression and archival of old memories

### Tool Integration Flow
1. **Tool Selection** → User chooses enabled tools
2. **MCP Server Startup** → Background server initialization
3. **Agent Configuration** → Tools registered with agent
4. **Request Routing** → Agent determines which tools to use
5. **Tool Execution** → Async execution with progress tracking
6. **Result Integration** → Tool outputs combined into response
7. **Activity Logging** → Usage tracking and analytics

---

## 🚀 Extension Points

### Adding New Tools
1. Create new MCP server in `tool_recommendation/`
2. Add tool registration in `TOOL_SERVER_MAP`
3. Update sidebar tool selection options
4. Add activity tracking integration
5. Update documentation

### Adding New AI Models
1. Update `get_model_from_name()` in `app.py`
2. Add model option in sidebar configuration
3. Update cost tracking with model pricing
4. Add model-specific optimizations
5. Update documentation

### Adding New UI Components
1. Create component class in `ui/components/`
2. Implement render method with Streamlit
3. Add component integration in main UI
4. Update styling in `utils/styles.py`
5. Add component documentation

### Extending Memory System
1. Add new memory categories in models
2. Implement category-specific retrieval logic
3. Update UI for category management
4. Add category-specific analytics
5. Update database schema if needed

---

This components guide provides a comprehensive overview of the Docy Search architecture. Each component is designed to be modular, maintainable, and extensible for future development.
