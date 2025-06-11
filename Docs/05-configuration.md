# Configuration Guide

This guide covers all configuration options, environment variables, and customization settings for Docy Search.

## 🔧 Environment Variables

### Required API Keys

#### OpenAI (Required for embeddings and default model)
```env
OPENAI_API_KEY=sk-your-openai-key-here
```
- **Purpose**: AI model access and semantic embeddings
- **Get Key**: [OpenAI Platform](https://platform.openai.com/)
- **Usage**: GPT-4o Mini model and text embeddings for memory
- **Cost**: Pay-per-token, see [OpenAI Pricing](https://openai.com/pricing)

#### Brave Search (Required for web search)
```env
BRAVE_API_KEY=your-brave-search-key
```
- **Purpose**: Live web search for tool discovery
- **Get Key**: [Brave Search API](https://brave.com/search/api/)
- **Usage**: Web search with 2000 free queries/month
- **Cost**: Free tier available, paid plans for higher usage

### Optional API Keys

#### Anthropic (Claude Models)
```env
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
```
- **Purpose**: Access to Claude 3 Opus model
- **Get Key**: [Anthropic Console](https://console.anthropic.com/)
- **Usage**: Alternative AI model with excellent reasoning
- **Cost**: Pay-per-token, typically higher than OpenAI

#### Google (Gemini Models)
```env
GOOGLE_API_KEY=your-google-api-key
```
- **Purpose**: Access to Gemini 1.5 Flash model
- **Get Key**: [Google AI Studio](https://aistudio.google.com/)
- **Usage**: Fast AI model with code generation capabilities
- **Cost**: Generous free tier, competitive paid pricing

#### GitHub (Enhanced API limits)
```env
GITHUB_TOKEN=ghp_your-github-token
```
- **Purpose**: Higher rate limits for GitHub API
- **Get Token**: [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
- **Usage**: Repository search and file access
- **Cost**: Free with GitHub account
- **Required Scopes**: `public_repo` (for public repositories)

#### DeepSeek (Alternative AI Model)
```env
DEEPSEEK_API_KEY=sk-your-deepseek-key
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```
- **Purpose**: Cost-effective alternative AI model
- **Get Key**: [DeepSeek Platform](https://platform.deepseek.com/)
- **Usage**: Budget-friendly AI model option
- **Cost**: Significantly lower than other providers

### Application Configuration

#### Default AI Model
```env
AI_MODEL=openai  # Options: openai, claude, gemini, deepseek
```
- **Default**: `openai` (GPT-4o Mini)
- **Purpose**: Sets the default AI model for new sessions
- **Changeable**: Can be switched in the UI sidebar

#### Database Configuration
```env
DATABASE_PATH=docy_search.db
```
- **Default**: `docy_search.db` in project root
- **Purpose**: SQLite database file location
- **Note**: Database is created automatically if it doesn't exist

#### Memory Database Path
```env
MEMORY_DB_PATH=data/memories.db
```
- **Default**: `data/memories.db`
- **Purpose**: Separate SQLite database for memory storage
- **Note**: Created in `data/` directory automatically

---

## 📁 Configuration Files

### `.env` File Template
Create a `.env` file in the project root:

```env
# Required for full functionality
OPENAI_API_KEY=sk-your-openai-key-here
BRAVE_API_KEY=your-brave-search-key

# Optional AI models
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-api-key
DEEPSEEK_API_KEY=sk-your-deepseek-key

# Optional integrations
GITHUB_TOKEN=ghp_your-github-token

# Application settings
AI_MODEL=openai
DATABASE_PATH=docy_search.db
MEMORY_DB_PATH=data/memories.db

# DeepSeek configuration (if using)
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1

# Optional: Custom model endpoints
# OPENAI_BASE_URL=https://api.openai.com/v1
# ANTHROPIC_BASE_URL=https://api.anthropic.com
```

### `project_context.md` (Optional)
Create this file in the project root for personalized recommendations:

```markdown
# My Development Project

## Project Type
React-based web application with Node.js backend

## Tech Stack
- Frontend: React 18, TypeScript, Tailwind CSS
- Backend: Node.js, Express, PostgreSQL
- Deployment: Docker, AWS

## Team Size
Small team (2-3 developers)

## Experience Level
Intermediate to advanced developers

## Constraints
- Budget-conscious (prefer free/open-source tools)
- Fast development cycle
- Performance is critical
- Must support mobile devices

## Current Tools
- IDE: VS Code
- Version Control: Git/GitHub
- CI/CD: GitHub Actions
- Testing: Jest, React Testing Library

## Goals
Looking for tools to improve:
- Code quality and linting
- Performance monitoring
- UI component development
- API testing and documentation
```

---

## ⚙️ Configuration Classes

### `config/settings.py` - Pydantic Settings

#### APISettings
```python
class APISettings(BaseSettings):
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    brave_api_key: Optional[str] = None
    github_token: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    deepseek_base_url: str = "https://api.deepseek.com/v1"
```

#### DatabaseSettings
```python
class DatabaseSettings(BaseSettings):
    database_path: str = "docy_search.db"
    memory_db_path: str = "data/memories.db"
    backup_enabled: bool = True
    backup_interval_hours: int = 24
    max_backup_files: int = 7
```

#### UISettings
```python
class UISettings(BaseSettings):
    default_theme: str = "light"
    page_title: str = "Docy Search Assistant"
    page_icon: str = "🔧"
    layout: str = "wide"
    sidebar_state: str = "expanded"
    auto_refresh_interval: int = 5
```

#### ToolSettings
```python
class ToolSettings(BaseSettings):
    default_tools: List[str] = [
        "web_search", "tool_recommend", "github_search"
    ]
    max_search_results: int = 10
    github_api_timeout: int = 30
    python_execution_timeout: int = 60
    enable_activity_tracking: bool = True
```

#### MemorySettings
```python
class MemorySettings(BaseSettings):
    embedding_model: str = "text-embedding-ada-002"
    max_memory_entries: int = 1000
    memory_compression_threshold: int = 100
    semantic_search_limit: int = 5
    enable_memory_compression: bool = True
```

---

## 🎛 Runtime Configuration

### Tool Selection
Configure tools in the UI sidebar or programmatically:

```python
# Available tools
AVAILABLE_TOOLS = {
    "web_search": "🔍 Web Search",
    "github_search": "🐙 GitHub Integration", 
    "python_tools": "🐍 Python Tools",
    "tool_recommend": "🎯 Tool Recommendation",
    "data_viz": "📊 Data Visualization",
    "sql_database": "🗄️ SQL Database"
}

# Default enabled tools
DEFAULT_TOOLS = ["web_search", "tool_recommend", "github_search"]
```

### AI Model Configuration
Switch models in the UI or set defaults:

```python
# Available models
AI_MODELS = {
    "openai": {
        "name": "OpenAI GPT-4o Mini",
        "cost": "Low",
        "speed": "Fast"
    },
    "claude": {
        "name": "Claude 3 Opus", 
        "cost": "High",
        "speed": "Medium"
    },
    "gemini": {
        "name": "Google Gemini 1.5 Flash",
        "cost": "Medium", 
        "speed": "Fast"
    },
    "deepseek": {
        "name": "DeepSeek Chat",
        "cost": "Very Low",
        "speed": "Medium"
    }
}
```

### Memory Configuration
Adjust memory behavior:

```python
# Memory settings
MEMORY_CONFIG = {
    "min_content_length": 100,  # Minimum content length to save
    "max_memories_per_user": 1000,  # Per-user memory limit
    "compression_threshold": 100,  # Compress after N memories
    "archival_age_days": 30,  # Archive memories older than N days
    "similarity_threshold": 0.7  # Semantic similarity threshold
}
```

---

## 🏗 Advanced Configuration

### Custom Model Endpoints

#### OpenAI-Compatible APIs
```env
OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
OPENAI_API_KEY=your-custom-api-key
```

#### Anthropic Proxy
```env
ANTHROPIC_BASE_URL=https://your-proxy.com/anthropic
ANTHROPIC_API_KEY=your-proxy-key
```

### Database Optimization

#### SQLite Settings
```python
# In database configuration
SQLITE_CONFIG = {
    "journal_mode": "WAL",  # Write-Ahead Logging
    "synchronous": "NORMAL",  # Balance speed vs safety
    "cache_size": 64000,  # 64MB cache
    "temp_store": "MEMORY",  # Temporary tables in memory
    "mmap_size": 268435456  # 256MB memory mapping
}
```

#### Connection Pooling
```python
# Database connection settings
CONNECTION_CONFIG = {
    "max_connections": 10,
    "connection_timeout": 30,
    "retry_attempts": 3,
    "retry_delay": 1.0
}
```

### Performance Tuning

#### MCP Server Configuration
```python
# Tool server settings
MCP_CONFIG = {
    "startup_timeout": 30,  # Server startup timeout
    "request_timeout": 60,  # Individual request timeout
    "max_retries": 3,  # Request retry attempts
    "concurrent_requests": 5  # Maximum concurrent requests
}
```

#### Caching Configuration
```python
# Response caching
CACHE_CONFIG = {
    "enable_caching": True,
    "cache_ttl_seconds": 3600,  # 1 hour cache TTL
    "max_cache_size": 100,  # Maximum cached responses
    "cache_expensive_operations": True
}
```

---

## 📊 Monitoring Configuration

### Activity Tracking
```python
# Activity tracking settings
ACTIVITY_CONFIG = {
    "enable_tracking": True,
    "track_api_calls": True,
    "track_file_access": True,
    "track_performance": True,
    "retention_days": 30
}
```

### Cost Tracking
```python
# Cost monitoring settings
COST_CONFIG = {
    "enable_cost_tracking": True,
    "cost_alerts": True,
    "daily_budget_usd": 10.0,
    "monthly_budget_usd": 100.0,
    "alert_threshold_percent": 80
}
```

### Logging Configuration
```python
# Logging settings
LOGGING_CONFIG = {
    "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "file_logging": True,
    "log_file": "docy_search.log",
    "max_log_size_mb": 50,
    "backup_count": 3
}
```

---

## 🚀 Deployment Configuration

### Production Settings
```env
# Production environment
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# Security
SECURE_HEADERS=true
RATE_LIMITING=true

# Performance
ENABLE_CACHING=true
CACHE_TTL=3600
MAX_CONCURRENT_REQUESTS=10

# Database
DATABASE_BACKUP_ENABLED=true
DATABASE_BACKUP_INTERVAL=24
```

### Development Settings
```env
# Development environment
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG

# Development features
AUTO_RELOAD=true
DISABLE_AUTH=true
ENABLE_PROFILING=true

# Testing
USE_MOCK_APIS=false
MOCK_RESPONSES=false
```

### Docker Configuration
```dockerfile
# Environment variables in Dockerfile
ENV OPENAI_API_KEY=""
ENV BRAVE_API_KEY=""
ENV AI_MODEL="openai"
ENV DATABASE_PATH="/app/data/docy_search.db"
ENV LOG_LEVEL="INFO"
```

---

## 🔍 Configuration Validation

### Environment Validation
The application validates configuration on startup:

```python
# Required API keys check
def validate_api_keys():
    warnings = []
    if not os.getenv("OPENAI_API_KEY"):
        warnings.append("OPENAI_API_KEY missing - embeddings disabled")
    if not os.getenv("BRAVE_API_KEY"):
        warnings.append("BRAVE_API_KEY missing - web search disabled")
    return warnings

# Database validation
def validate_database():
    try:
        db_path = Path(settings.database_path)
        db_path.parent.mkdir(exist_ok=True)
        return True
    except Exception as e:
        raise ConfigurationError(f"Database validation failed: {e}")
```

### Configuration Health Check
```python
# Health check endpoint
def config_health_check():
    return {
        "api_keys": {
            "openai": bool(os.getenv("OPENAI_API_KEY")),
            "brave": bool(os.getenv("BRAVE_API_KEY")),
            "anthropic": bool(os.getenv("ANTHROPIC_API_KEY")),
            "google": bool(os.getenv("GOOGLE_API_KEY"))
        },
        "database": {
            "accessible": check_database_access(),
            "size_mb": get_database_size_mb()
        },
        "memory": {
            "enabled": bool(memory_manager),
            "entries": get_memory_count()
        }
    }
```

---

## 🛠 Troubleshooting Configuration

### Common Configuration Issues

#### API Key Problems
```bash
# Check if API keys are loaded
python -c "import os; print('OpenAI:', bool(os.getenv('OPENAI_API_KEY')))"
python -c "import os; print('Brave:', bool(os.getenv('BRAVE_API_KEY')))"
```

#### Database Issues
```bash
# Check database permissions
ls -la docy_search.db
mkdir -p data && chmod 755 data
```

#### Environment Loading
```bash
# Verify .env file loading
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('Loaded:', os.getenv('OPENAI_API_KEY', 'NOT_FOUND')[:10])"
```

### Configuration Reset
```bash
# Reset to default configuration
rm -f docy_search.db data/memories.db
cp .env.example .env
# Edit .env with your API keys
```

### Debug Configuration
```python
# Enable debug mode
import os
os.environ["DEBUG"] = "true"
os.environ["LOG_LEVEL"] = "DEBUG"

# Run with verbose logging
streamlit run docy_search/main_ui.py --logger.level=debug
```

---

This configuration guide covers all aspects of setting up and customizing Docy Search. For specific deployment scenarios or advanced configurations, refer to the deployment documentation or create an issue for support.
