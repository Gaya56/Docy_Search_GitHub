# Tool Recommendation System - Complete Analysis & Containerization

## 🎯 System Overview

The `tool_recommendation` directory contains a sophisticated **AI-powered tool discovery and analysis system** built with the **FastMCP (Model Context Protocol)** framework. It's designed as a collection of microservices that can discover, analyze, and provide installation guidance for development tools.

## 🏗️ Architecture Deep Dive

### Core Components

1. **MCP-Based Microservices**
   - Each file is an independent MCP server
   - Uses FastMCP for standardized tool registration
   - Activity tracking across all operations
   - Graceful error handling and fallbacks

2. **AI Integration**
   - **Google Gemini** for tool analysis and recommendations
   - **OpenAI** for embeddings and memory systems
   - **Perplexity AI** for focused search results

3. **External APIs**
   - **Brave Search** for web search capabilities
   - **GitHub API** for repository analysis
   - **Multiple AI providers** for redundancy

### Data Flow

```
User Query → Tool Search → AI Analysis → Recommendation → Installation Guide
     ↓           ↓            ↓             ↓              ↓
Activity Tracking → Resource Monitoring → Progress Updates → Completion Status
```

### Key Features

| Feature | Description | Files Involved |
|---------|-------------|----------------|
| **Tool Discovery** | Search and rank development tools | `mcp_server.py`, `brave_search.py` |
| **AI Analysis** | Intelligent tool evaluation | `mcp_server.py` (Gemini integration) |
| **GitHub Integration** | Repository search and analysis | `github_mcp_server.py` |
| **Code Analysis** | Repository quality assessment | `code_analyzer.py` |
| **Python REPL** | Code execution and visualization | `python_tools.py` |
| **Database Queries** | Natural language to SQL | `sql_tools.py` |
| **Activity Tracking** | Real-time operation monitoring | `activity_tracker.py` |
| **Web Search** | Brave Search API integration | `brave_search.py` |

## 📦 Containerization Strategy

### Why Docker?

1. **Isolation**: Self-contained environment with all dependencies
2. **Portability**: Runs anywhere Docker is available
3. **Scalability**: Easy to deploy multiple instances
4. **Integration**: Simple API interface for any application

### Container Architecture

```
┌─────────────────────────────────────────┐
│           Docker Container             │
├─────────────────────────────────────────┤
│  FastAPI Server (Port 8000)           │
│  ├── Unified MCP Endpoint             │
│  ├── Health Check Endpoint            │
│  ├── Activity Monitoring              │
│  └── Tool Execution Engine            │
├─────────────────────────────────────────┤
│  Tool Recommendation System           │
│  ├── search_tools                     │
│  ├── analyze_tools                    │
│  ├── github_repositories              │
│  ├── code_analyzer                    │
│  ├── python_repl                      │
│  └── sql_tools                        │
├─────────────────────────────────────────┤
│  External API Integrations            │
│  ├── Brave Search API                 │
│  ├── Google Gemini API                │
│  ├── GitHub API                       │
│  ├── OpenAI API                       │
│  └── Perplexity API                   │
└─────────────────────────────────────────┘
```

## 🚀 Implementation Details

### Files Created for Containerization

1. **`Dockerfile`** - Multi-stage container build
2. **`docker-compose.yml`** - Container orchestration
3. **`server.py`** - Unified FastAPI server
4. **`client.py`** - Python client library
5. **`requirements.txt`** - Python dependencies
6. **`.env.example`** - Environment configuration
7. **`setup.sh`** - Automated setup script
8. **`Makefile`** - Development commands
9. **`streamlit_example.py`** - Complete integration example
10. **`README.md`** - Comprehensive documentation

### API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Service info and status |
| `/health` | GET | Container health check |
| `/tools` | GET | List available tools |
| `/execute` | POST | Execute any tool |
| `/activity` | GET | Monitor operations |
| `/streamlit-integration` | POST | Optimized for Streamlit |

### Environment Variables

Required for full functionality:
- `BRAVE_API_KEY` - Web search (required)
- `GOOGLE_API_KEY` - AI analysis (required)
- `GITHUB_TOKEN` - Repository access (recommended)
- `OPENAI_API_KEY` - Embeddings (optional)
- `PERPLEXITY_API_KEY` - Enhanced search (optional)

## 🔌 Integration with Streamlit

### Simple Integration (5 minutes)

```python
from client import ToolRecommendationClient

client = ToolRecommendationClient("http://localhost:8000")
result = client.search_tools("python web frameworks")
st.write(result)
```

### Advanced Integration (Full Chatbot)

The `streamlit_example.py` provides a complete chatbot with:
- Server connection management
- Real-time activity monitoring
- Tool categorization
- Progress tracking
- Quick action buttons
- Formatted responses

### Integration Features

1. **Health Monitoring** - Automatic server connection checks
2. **Progress Tracking** - Real-time operation status
3. **Error Handling** - Graceful degradation when services unavailable
4. **Activity Logs** - Detailed operation monitoring
5. **Quick Actions** - Pre-built common queries
6. **Responsive UI** - Clean, professional interface

## 🛠️ Setup Instructions

### 1. Quick Start (Using Setup Script)

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Build and run
make build
make run

# Test functionality
make test
```

### 2. Manual Setup

```bash
# Copy tool recommendation files
cp -r ../docy_search/tool_recommendation/ ./tool_recommendation/
cp -r ../config/ ./config/

# Build container
docker-compose build

# Start services
docker-compose up -d

# Verify health
curl http://localhost:8000/health
```

### 3. Integration with Your Streamlit App

```bash
# Install client dependencies
pip install requests streamlit

# Copy client files
cp client.py /path/to/your/streamlit/app/
cp streamlit_example.py /path/to/your/streamlit/app/

# In your Streamlit app
from client import StreamlitToolClient
client = StreamlitToolClient("http://localhost:8000")
```

## 🔒 Production Considerations

### Security
- API keys stored in environment variables
- SQL injection protection (read-only queries)
- Container network isolation
- Resource limits in production

### Performance
- Response caching for repeated queries
- Async operations where possible
- Resource monitoring and limits
- Health checks for auto-recovery

### Monitoring
- Real-time activity tracking
- API usage monitoring
- Error logging and alerting
- Performance metrics

### Scaling
- Horizontal scaling with load balancer
- Database persistence for memory
- API rate limiting
- Container orchestration (K8s)

## 🎉 Benefits of This Approach

### For You
1. **Plug & Play** - Drop into any Python application
2. **Zero Setup** - Everything containerized and ready
3. **Powerful Features** - Full AI-powered tool discovery
4. **Easy Integration** - Simple REST API
5. **Scalable** - Run multiple instances

### For Users
1. **Intelligent Recommendations** - AI-powered analysis
2. **Comprehensive Search** - Web + GitHub + AI search
3. **Installation Guides** - Step-by-step instructions
4. **Code Execution** - Test tools directly
5. **Real-time Feedback** - Progress tracking

### Technical Advantages
1. **Microservices Architecture** - Modular and maintainable
2. **Standardized Protocol** - MCP for tool communication
3. **Fault Tolerance** - Graceful fallbacks
4. **Monitoring** - Complete activity tracking
5. **Documentation** - Comprehensive guides and examples

## 🚀 Next Steps

1. **Set up the container** using the provided setup script
2. **Configure your API keys** in the `.env` file
3. **Test the functionality** with the provided test scripts
4. **Integrate with your Streamlit app** using the example code
5. **Customize as needed** for your specific use case

The system is designed to be production-ready out of the box while remaining flexible for customization and extension.
