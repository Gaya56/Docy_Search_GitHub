# 🤖 AI Tool Recommendation System with Notion Integration

A comprehensive AI-powered platform that combines intelligent tool discovery with seamless Notion document management. Perfect for developers who want to find the right tools and manage their documentation in one unified interface.

## ✨ Features

### 🔍 Tool Discovery & Analysis
- **Smart Tool Search**: Find development tools using natural language queries
- **AI-Powered Recommendations**: Get personalized tool suggestions based on your needs
- **Detailed Comparisons**: Compare frameworks, libraries, and tools side-by-side
- **Installation Guides**: Step-by-step setup instructions for any platform
- **GitHub Integration**: Explore and analyze repository structures and code quality
- **Code Execution**: Run Python snippets and create data visualizations

### 📝 Notion Document Management
- **Page Reading**: Access and display your Notion page contents
- **Smart Search**: Find information across your Notion workspace
- **Content Analysis**: Get AI insights from your documentation
- **Organization Tips**: Improve your Notion workflow with AI suggestions

### 🌐 Web Search & Analysis
- **Brave Search Integration**: Get real-time web search results
- **Perplexity AI Search**: Access advanced AI-powered search capabilities
- **GitHub Repository Search**: Discover relevant repositories and analyze code

### 💾 Data Management
- **SQL Query Interface**: Natural language to SQL conversion
- **Database Tools**: Manage and query your data with ease
- **Activity Tracking**: Monitor tool usage and API calls

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- Docker & Docker Compose
- UV package manager (recommended) or pip

### 2. Clone & Setup
```bash
git clone https://github.com/Gaya56/Docy_Search_GitHub.git
cd Docy_Search_GitHub

# Create virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file with your API keys:
```bash
# Required for tool recommendations
OPENAI_API_KEY=your_openai_key
BRAVE_API_KEY=your_brave_key
PERPLEXITY_API_KEY=your_perplexity_key
GITHUB_TOKEN=your_github_token
GOOGLE_API_KEY=your_google_key

# Optional for Notion integration
NOTION_API_KEY=your_notion_key
NOTION_PAGE_ID=your_default_page_id
```

### 4. Start the System
```bash
# Start the tool recommendation server
make run

# In another terminal, start the Streamlit app
source .venv/bin/activate
streamlit run app.py
```

### 5. Access the Application
- **Streamlit Web UI**: http://localhost:8501
- **API Server**: http://localhost:8947

## 🎯 Usage Modes

### Tool Discovery Mode
Perfect for finding and analyzing development tools:
- "Find the best Python web frameworks"
- "Compare React vs Vue.js for my project"
- "How do I install Docker on Ubuntu?"
- "Show me popular data science libraries"

### Notion Integration Mode
Ideal for managing your documentation:
- "Read my project planning page"
- "Search for API documentation in my workspace"
- "Analyze my meeting notes from last week"
- "Help me organize my Notion workspace"

### Combined Mode
Get the best of both worlds:
- "Find Python tools and document them in Notion"
- "Read my development notes and suggest missing tools"
- "Compare frameworks and save findings to my page"

## 🛠️ Available Tools

### Search & Analysis
- `search_tools` - Find development tools by category or purpose
- `analyze_tools` - Get detailed tool analysis and comparisons
- `get_installation_guide` - Platform-specific installation instructions

### Web & GitHub
- `search_web` - Real-time web search via Brave API
- `search_github_repositories` - Find and analyze GitHub repos
- `get_repository_structure` - Explore repository contents
- `analyze_repository` - Code quality and structure analysis

### Development
- `python_repl` - Execute Python code snippets
- `data_visualization` - Create charts and graphs
- `sql_tools` - Natural language to SQL queries

### AI Search
- `perplexity_search` - Advanced AI-powered search

### Notion (when configured)
- `read_notion_page` - Access Notion page content
- `search_notion_page` - Search within Notion documents
- `add_to_notion_page` - Add content to Notion pages

## 📁 Project Structure

```
Docy_Search_GitHub/
├── app.py                 # Main Streamlit application
├── client.py              # API client library
├── server.py              # FastAPI server
├── requirements.txt       # Python dependencies
├── Makefile              # Build and run commands
├── docker-compose.yml    # Docker configuration
├── Dockerfile            # Container definition
├── tool_recommendation/  # Core tool modules
│   ├── mcp_server.py     # Main MCP server
│   ├── brave_search.py   # Web search integration
│   ├── github_mcp_server.py # GitHub integration
│   ├── notion_mcp_server.py # Notion integration
│   ├── sql_tools.py      # Database tools
│   └── activity_tracker.py # Usage monitoring
├── notion_mcp_agent/     # Standalone Notion agent
├── config/               # Configuration files
└── data/                 # Database and logs
```

## 🐳 Docker Deployment

### Build and Run
```bash
# Build the container
make build

# Start the service
make run

# Check health
make health

# View logs
make logs

# Stop the service
make stop
```

### Manual Docker Commands
```bash
# Build
docker-compose build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 🔧 Configuration

### Server Settings
- **Port**: 8947 (configurable in docker-compose.yml)
- **Database**: SQLite (persistent volume mounted)
- **Logging**: Available in `./logs/` directory

### API Rate Limits
- Configurable per service in environment variables
- Built-in retry logic and error handling
- Activity tracking for usage monitoring

## 🧪 Testing

```bash
# Test the container
make test

# Test specific tools
python -c "from client import ToolRecommendationClient; print(ToolRecommendationClient().health_check())"
```

## 📖 API Documentation

### Health Check
```bash
curl http://localhost:8947/health
```

### List Available Tools
```bash
curl http://localhost:8947/tools
```

### Execute Tool
```bash
curl -X POST http://localhost:8947/execute \
  -H "Content-Type: application/json" \
  -d '{"tool": "search_tools", "query": "python web frameworks"}'
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m "Add feature"`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastMCP](https://github.com/jlowin/fastmcp) for MCP server functionality
- Powered by OpenAI, Brave Search, Perplexity AI, and GitHub APIs
- Notion integration for seamless documentation management
- Streamlit for the beautiful web interface

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/Gaya56/Docy_Search_GitHub/issues)
- 📖 Documentation: [Wiki](https://github.com/Gaya56/Docy_Search_GitHub/wiki)

---

**Made with ❤️ for developers who love great tools and organized documentation**
