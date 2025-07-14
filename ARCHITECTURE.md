# AI Tool Recommendation System Architecture

## 🎯 System Overview

A containerized AI-powered tool discovery platform with OpenAI GPT-4 integration and Notion document management.

## 🏗️ Architecture

### Core Components

```
┌─────────────────────────────────────────┐
│        Streamlit Frontend              │
│        (OpenAI GPT-4 Chatbot)          │
│        Port: 8501                      │
└─────────────────────────────────────────┘
                    │ HTTP API
┌─────────────────────────────────────────┐
│        Docker Container                │
│        FastAPI Server - Port: 8947     │
├─────────────────────────────────────────┤
│  Tool Recommendation System (MCP)      │
│  ├── search_tools                      │
│  ├── github_repositories               │
│  ├── notion_integration               │
│  ├── web_search (Brave)               │
│  ├── perplexity_search                │
│  └── activity_tracker                 │
├─────────────────────────────────────────┤
│  External API Integrations            │
│  ├── OpenAI API (GPT-4)               │
│  ├── Notion API                       │
│  ├── GitHub API                       │
│  ├── Brave Search API                 │
│  └── Perplexity API                   │
└─────────────────────────────────────────┘
```

### Data Flow

```
User Query → OpenAI GPT-4 → Tool Selection → MCP Server → External APIs → Response
```

## 📦 Container Architecture

### Files Structure
```
Docy_Search_GitHub/
├── 🎨 Frontend
│   └── app.py                 # Streamlit UI with OpenAI integration
├── 🐳 Backend Container
│   ├── server.py              # FastAPI server (Port: 8947)
│   ├── Dockerfile             # Container definition
│   └── docker-compose.yml     # Orchestration
├── 🛠️ MCP Tools
│   └── tool_recommendation/
│       ├── mcp_server.py      # Core tool search
│       ├── notion_mcp_server.py # Notion integration
│       ├── github_mcp_server.py # GitHub tools
│       ├── brave_search.py    # Web search
│       ├── perplexity_search.py # AI search
│       └── activity_tracker.py # Usage monitoring
└── 🔧 Configuration
    ├── requirements.txt       # Dependencies
    ├── Makefile              # Build commands
    └── .env.example          # Environment template
```

## 🚀 Deployment Commands

### Quick Start
```bash
# Build and run Docker container
make build && make run

# Start Streamlit UI
source .venv/bin/activate
streamlit run app.py
```

### Manual Docker
```bash
# Build container
docker-compose build

# Start services
docker-compose up -d

# Check health
curl http://localhost:8947/health

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service information |
| `/health` | GET | Health check |
| `/tools` | GET | List available tools |
| `/execute` | POST | Execute tool with parameters |
| `/activity` | GET | Monitor operations |

### Example Usage
```bash
# Test tool execution
curl -X POST http://localhost:8947/execute \
  -H "Content-Type: application/json" \
  -d '{
    "tool_name": "search_tools",
    "parameters": {"query": "python web frameworks"}
  }'
```

## 🧠 OpenAI GPT-4 Integration

### Intelligent Tool Selection
- GPT-4 analyzes user queries
- Automatically selects appropriate tools
- Dynamically passes parameters
- Formats responses for readability

### Function Calling
```python
# GPT-4 decides which tool to use
tools = [
    {
        "name": "search_tools",
        "description": "Search for development tools",
        "parameters": {...}
    },
    {
        "name": "read_notion_page", 
        "description": "Read Notion page content",
        "parameters": {...}
    }
]
```

## � Notion Integration

### Dynamic Credentials
- API keys passed securely per request
- Environment variables set dynamically
- Optional default page ID configuration

### Available Functions
- `read_notion_page` - Access page content
- `search_notion_page` - Search documents  
- `add_to_notion_page` - Add content to pages

## 🔧 Environment Configuration

### Required
```bash
OPENAI_API_KEY=your_openai_key_here
```

### Optional (Enhanced Features)
```bash
BRAVE_API_KEY=your_brave_key
PERPLEXITY_API_KEY=your_perplexity_key
GITHUB_TOKEN=your_github_token
NOTION_API_KEY=your_notion_key
NOTION_PAGE_ID=your_default_page_id
```

## 🎯 Key Benefits

1. **AI-Driven**: OpenAI GPT-4 for intelligent interactions
2. **Containerized**: Easy deployment and scaling
3. **Modular**: MCP-based tool architecture
4. **Integrated**: Seamless Notion document management
5. **Extensible**: Easy to add new tools and APIs

---

**Ready for production deployment with minimal configuration required**
