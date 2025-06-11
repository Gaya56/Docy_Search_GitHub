# API Reference

This document provides detailed information about all functions, classes, and methods in the Docy Search application.

## 📦 Core Modules

### `docy_search.app`

#### Functions

##### `load_project_context() -> str`
Loads project context from `project_context.md` file.

**Returns**: Project context string or empty string if file not found.

##### `get_model_from_name(model_name: str) -> Model`
Creates AI model instance based on model name.

**Parameters**:
- `model_name`: One of "openai", "claude", "gemini", "deepseek"

**Returns**: Configured model instance.

##### `create_agent_with_context(project_context="", user_id=None, model_name=None, selected_tools=None) -> Agent`
Creates Pydantic AI agent with context and selected tools.

**Parameters**:
- `project_context`: Project-specific context string
- `user_id`: User identifier for memory isolation
- `model_name`: AI model to use ("openai", "claude", "gemini", "deepseek")
- `selected_tools`: List of tool keys to enable

**Returns**: Configured Pydantic AI Agent instance.

#### Classes

##### `TOOL_SERVER_MAP: Dict[str, Callable]`
Mapping of tool keys to MCP server factory functions.

**Available Tools**:
- `"websearch"` / `"web_search"`: Brave Search integration
- `"python_tools"`: Python code execution
- `"tool_recommendation"` / `"tool_recommend"`: AI tool analysis
- `"github_search"`: GitHub repository search
- `"data_viz"`: Data visualization tools

---

### `docy_search.main_ui`

#### Functions

##### `initialize_session_state() -> None`
Initializes all Streamlit session state variables.

##### `get_project_context() -> str`
Cached function to load project context.

##### `display_sidebar() -> None`
Renders sidebar with configuration controls.

##### `log_chat_to_database(prompt: str, response: str, model_used=None, tools_used=None, memory_id=None) -> None`
Logs chat interaction to SQLite database.

**Parameters**:
- `prompt`: User input message
- `response`: AI assistant response
- `model_used`: AI model name used for response
- `tools_used`: List of tools used during processing
- `memory_id`: Memory entry ID if conversation was saved

---

## 🛠 Tool Recommendation System

### `docy_search.tool_recommendation.mcp_server`

#### MCP Tools

##### `@mcp.tool() async def search_tools(query: str, category: str = "general") -> str`
Search for development tools using Brave Search API.

**Parameters**:
- `query`: Search query for tools
- `category`: Tool category ("web", "mobile", "desktop", "database", etc.)

**Returns**: Formatted search results with tool information.

##### `@mcp.tool() async def analyze_tools(search_results: str, requirements: str = "") -> str`
AI-powered analysis and ranking of tool search results.

**Parameters**:
- `search_results`: Raw search results to analyze
- `requirements`: User requirements and constraints

**Returns**: AI analysis with tool rankings and recommendations.

##### `@mcp.tool() async def recommend_tools_for_task(task_description: str, skill_level: str = "intermediate") -> str`
Get comprehensive tool recommendations for specific tasks.

**Parameters**:
- `task_description`: Description of the development task
- `skill_level`: User skill level ("beginner", "intermediate", "advanced")

**Returns**: Structured recommendations with essential and specialized tools.

##### `@mcp.tool() async def compare_tools(tool_names: str) -> str`
Compare multiple tools side-by-side with detailed analysis.

**Parameters**:
- `tool_names`: Comma-separated list of tool names to compare

**Returns**: Detailed comparison including pros, cons, and use cases.

##### `@mcp.tool() async def get_installation_guide(tool_name: str, os_type: str = "linux") -> str`
Generate step-by-step installation instructions.

**Parameters**:
- `tool_name`: Name of the tool to install
- `os_type`: Operating system ("linux", "windows", "macos")

**Returns**: Comprehensive installation guide with troubleshooting tips.

### `docy_search.tool_recommendation.github_mcp_server`

#### MCP Tools

##### `@mcp.tool() async def search_github_repositories(query: str, language: str = "", limit: int = 5) -> str`
Search GitHub repositories for tools and projects.

**Parameters**:
- `query`: Search query (e.g., "react components", "python web framework")
- `language`: Programming language filter (optional)
- `limit`: Maximum number of results (default: 5, max: 10)

**Returns**: JSON string with repository information including links, descriptions, and stats.

##### `@mcp.tool() async def get_repository_structure(repo_full_name: str) -> str`
Get the file and folder structure of a GitHub repository.

**Parameters**:
- `repo_full_name`: Repository name in format "owner/repo"

**Returns**: JSON structure with files, folders, and key files identified.

##### `@mcp.tool() async def get_file_from_repository(repo_full_name: str, file_path: str) -> str`
Retrieve specific file content from a GitHub repository.

**Parameters**:
- `repo_full_name`: Repository name in format "owner/repo"
- `file_path`: Path to the file within the repository

**Returns**: JSON with file metadata and content (truncated if large).

### `docy_search.tool_recommendation.brave_search`

#### MCP Tools

##### `@mcp.tool() async def search_web(query: str, num_results: int = None) -> str`
Search the web using Brave Search API.

**Parameters**:
- `query`: Search query string
- `num_results`: Number of results to return (default from config)

**Returns**: Markdown-formatted search results with titles, URLs, and descriptions.

### `docy_search.tool_recommendation.python_tools`

#### Classes

##### `PythonREPL`
Python code execution environment with state persistence.

#### MCP Tools

##### `@mcp.tool() async def python_repl(code: str) -> str`
Execute Python code in a persistent environment.

**Parameters**:
- `code`: Python code to execute

**Returns**: Execution output or error messages.

##### `@mcp.tool() async def data_visualization(code: str) -> str`
Execute Python code with matplotlib for data visualization.

**Parameters**:
- `code`: Python code that generates visualizations

**Returns**: Base64-encoded image data or execution output.

---

## 🧠 Memory System

### `docy_search.memory.memory_manager`

#### Classes

##### `MemoryManager`
Main memory management class with sync and async operations.

**Constructor**:
```python
MemoryManager(db_path: str = "data/memories.db", model: Optional[Model] = None)
```

##### Methods

###### `save_memory(user_id: str, content: str, metadata: Dict = None, category: str = "general") -> str`
Save content to memory with semantic embedding.

**Parameters**:
- `user_id`: User identifier for isolation
- `content`: Content to save in memory
- `metadata`: Additional metadata dictionary
- `category`: Memory category for organization

**Returns**: Memory ID string.

###### `retrieve_memories(user_id: str, query: str = "", limit: int = 5, category: str = None) -> str`
Retrieve relevant memories using semantic search.

**Parameters**:
- `user_id`: User identifier
- `query`: Search query for semantic matching
- `limit`: Maximum number of memories to return
- `category`: Filter by memory category

**Returns**: Formatted string with relevant memories.

###### `get_user_memory_stats(user_id: str) -> Dict[str, int]`
Get memory statistics for a user.

**Parameters**:
- `user_id`: User identifier

**Returns**: Dictionary with memory counts by status.

### `docy_search.memory.cost_tracker`

#### Classes

##### `CostTracker`
Tracks API usage costs across different models.

##### Methods

###### `track_cost(model_name: str, input_tokens: int, output_tokens: int, user_id: str = None) -> float`
Track API usage and calculate cost.

**Parameters**:
- `model_name`: AI model used
- `input_tokens`: Number of input tokens
- `output_tokens`: Number of output tokens
- `user_id`: User identifier

**Returns**: Cost for this API call.

###### `get_daily_cost(user_id: str = None) -> float`
Get total cost for today.

###### `get_monthly_cost(user_id: str = None) -> float`
Get total cost for current month.

---

## 🗄 Database System

### `docy_search.database.db_manager`

#### Classes

##### `DatabaseManager`
Main database management class for SQLite operations.

##### Methods

###### `save_chat_interaction(user_id: str, prompt: str, response: str, model_used: str = None, tools_used: List[str] = None, memory_id: str = None, cost: float = 0.0) -> int`
Save chat interaction to database.

**Returns**: Chat record ID.

###### `get_chat_history(user_id: str, limit: int = 50) -> List[Dict]`
Retrieve chat history for a user.

**Returns**: List of chat records.

###### `save_memory_entry(memory_id: str, user_id: str, content: str, metadata: Dict = None) -> bool`
Save memory entry to database.

**Returns**: Success status.

###### `log_activity(user_id: str, activity_type: str, description: str = None, metadata: Dict = None) -> None`
Log user activity for analytics.

###### `get_database_stats() -> Dict[str, Any]`
Get overall database statistics.

**Returns**: Dictionary with table counts and metrics.

#### Functions

##### `get_db_manager() -> DatabaseManager`
Get or create database manager singleton instance.

### `docy_search.database.connection_manager`

#### Classes

##### `MCPSQLiteConnection`
Manages MCP SQLite server connections.

##### Static Methods

###### `get_sqlite_db_path() -> str`
Get path to SQLite database file.

###### `initialize_database() -> None`
Initialize database with required tables.

###### `async create_session()`
Create MCP client session context manager.

---

## 🎨 UI Components

### `docy_search.ui.components.chat`

#### Classes

##### `ChatComponent`
Handles chat interface and message management.

**Constructor**:
```python
ChatComponent(agent_getter: Callable)
```

##### Methods

###### `render() -> Optional[Tuple[str, str]]`
Render chat interface.

**Returns**: Tuple of (prompt, response) if new message, None otherwise.

###### `add_assistant_message(content: str, memory_saved: bool = False, memory_id: int = None) -> None`
Add assistant message to chat history.

### `docy_search.ui.components.sidebar`

#### Classes

##### `SidebarComponent`
Handles all sidebar functionality including tool selection and model configuration.

**Constructor**:
```python
SidebarComponent(memory_manager=None, model=None)
```

##### Methods

###### `render() -> Dict[str, Any]`
Render sidebar and return configuration changes.

**Returns**: Dictionary with 'tools_changed' and 'model_changed' flags.

### `docy_search.ui.components.dashboard`

#### Classes

##### `DashboardComponent`
Dashboard generation and database viewing component.

##### Methods

###### `render() -> None`
Render dashboard interface with tabs for dashboard generation and database viewing.

### `docy_search.ui.components.memory`

#### Classes

##### `MemoryComponent`
Handles memory operations in the UI.

##### Methods

###### `save_memory(prompt: str, response: str) -> Tuple[bool, Optional[int]]`
Save interaction to memory.

**Returns**: Tuple of (success, memory_id).

###### `render_memory_status(memory_saved: bool, memory_id: int = None) -> None`
Render memory status indicator.

---

## ⚙️ Configuration

### `config.settings`

#### Classes

##### `APISettings`
API keys and endpoints configuration using Pydantic settings.

##### Fields
- `openai_api_key`: OpenAI API key
- `anthropic_api_key`: Anthropic (Claude) API key
- `google_api_key`: Google (Gemini) API key
- `brave_api_key`: Brave Search API key
- `github_token`: GitHub personal access token
- `deepseek_api_key`: DeepSeek API key
- `deepseek_base_url`: DeepSeek API endpoint

##### `DatabaseSettings`
Database configuration settings.

##### `UISettings`  
User interface configuration settings.

##### `AppSettings`
Main application settings combining all configuration sections.

---

## 🔄 Activity Tracking

### `docy_search.tool_recommendation.activity_tracker`

#### Classes

##### `ActivityTracker`
Tracks tool usage and operations in real-time.

##### Methods

###### `async start_activity(tool_name: str, params: Dict = None) -> str`
Start tracking a new activity.

**Returns**: Activity ID for tracking.

###### `async update_activity(activity_id: str, progress: int, details: Dict = None) -> None`
Update activity progress and details.

###### `async complete_activity(activity_id: str, result: str = None) -> None`
Mark activity as completed.

###### `get_activity_summary() -> Dict[str, Any]`
Get summary of current and recent activities.

**Returns**: Dictionary with current activity, recent activities, and resource usage.

---

## 🧩 Models and Schemas

### `docy_search.tool_recommendation.models`

#### Classes

##### `ToolRecommendation`
Pydantic model for tool recommendations.

##### Fields
- `name`: Tool name
- `description`: Tool description
- `url`: Official website URL
- `github_url`: GitHub repository URL
- `category`: Tool category
- `platforms`: Supported platforms
- `installation_methods`: Available installation methods
- `relevance_score`: Relevance score (0-10)
- `reliability_score`: Reliability score (0-10)
- `ease_of_use_score`: Ease of use score (0-10)
- `overall_score`: Overall score (0-10)

##### `SearchQuery`
Search query configuration.

##### `RecommendationResponse`
Complete response with recommendations and metadata.

##### `ToolCategory`
Enum of available tool categories.

##### `Platform`
Enum of supported platforms.

##### `InstallationMethod`
Enum of installation methods.

---

## 🚀 Dashboard Generation

### `docy_search.dashboard.generator`

#### Classes

##### `DashboardGenerator`
Generates AI-powered analytics dashboards.

##### Methods

###### `async generate_dashboard(db_path: str = None) -> Dict[str, Any]`
Generate complete dashboard with charts and insights.

**Returns**: Dictionary with HTML content and metadata.

###### `generate_charts(data: Dict) -> str`
Generate chart visualizations from data.

### `docy_search.dashboard.validators`

#### Functions

##### `validate_database_path(path: str) -> bool`
Validate database file exists and is accessible.

##### `validate_chart_data(data: Dict) -> bool`
Validate data structure for chart generation.

---

## 🛡 Error Handling

### Common Exceptions

#### `DatabaseError`
Raised when database operations fail.

#### `APIKeyError`
Raised when required API keys are missing or invalid.

#### `ToolExecutionError`
Raised when MCP tool execution fails.

#### `MemoryError`
Raised when memory operations fail.

---

## 📝 Usage Examples

### Basic Agent Creation
```python
from docy_search.app import create_agent_with_context

agent = create_agent_with_context(
    project_context="React development project",
    user_id="user123",
    model_name="openai",
    selected_tools=["web_search", "github_search"]
)
```

### Memory Operations
```python
from docy_search.memory.memory_manager import MemoryManager

memory = MemoryManager()
memory_id = memory.save_memory(
    user_id="user123",
    content="User prefers React over Vue",
    category="preferences"
)

memories = memory.retrieve_memories(
    user_id="user123",
    query="frontend framework preferences"
)
```

### Database Operations
```python
from docy_search.database.db_manager import get_db_manager

db = get_db_manager()
chat_id = db.save_chat_interaction(
    user_id="user123",
    prompt="Best React components library?",
    response="I recommend Material-UI for React...",
    model_used="openai",
    tools_used=["web_search", "github_search"]
)
```

---

This API reference covers all major functions, classes, and methods in the Docy Search application. For implementation details and examples, see the source code and other documentation files.
