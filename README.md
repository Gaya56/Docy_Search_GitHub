# 🤖 AI Tool Recommendation System with Notion Integration

An intelligent platform combining AI-powered tool discovery with Notion integration, all powered by OpenAI GPT-4.

## ✨ Key Features

- **🤖 Smart AI Assistant**: OpenAI GPT-4 automatically selects and executes the best tools for your queries
- **📝 Notion Integration**: Read, search, and add content to your Notion pages
- **🔍 Tool Discovery**: Find and analyze development tools, frameworks, and libraries
- **🐙 GitHub Integration**: Search repositories and analyze code structure
- **🌐 Web Search**: Real-time search via Brave and Perplexity APIs
- **💾 Database Tools**: Natural language to SQL conversion

## 🚀 Quick Start

### Prerequisites
```bash
# Ensure you have Docker and Python 3.8+
docker --version
python --version
```

### Setup & Run
```bash
# 1. Clone and setup
git clone https://github.com/Gaya56/Docy_Search_GitHub.git
cd Docy_Search_GitHub
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Configure environment (copy and edit with your API keys)
cp .env.example .env

# 3. Start the tool server
make build && make run

# 4. Start the Streamlit UI (in a new terminal)
source .venv/bin/activate
streamlit run app.py
```

### Access Points
- **Streamlit Web UI**: http://localhost:8501
- **Tool API Server**: http://localhost:8947

## 🔧 Configuration

Add your API keys to `.env`:
```bash
# Required
OPENAI_API_KEY=your_openai_key_here

# Optional (for enhanced functionality)
BRAVE_API_KEY=your_brave_key
PERPLEXITY_API_KEY=your_perplexity_key
GITHUB_TOKEN=your_github_token
NOTION_API_KEY=your_notion_key
NOTION_PAGE_ID=your_default_page_id
```

## 💬 How to Use

1. **Configure API Keys**: Enter your OpenAI key in the sidebar
2. **Connect to Server**: Click "Connect to Tool Server" 
3. **Optional Notion Setup**: Add Notion API key and page ID for document integration
4. **Start Chatting**: Ask questions like:
   - "Find the best Python web frameworks"
   - "Search GitHub for React components"
   - "Read my Notion project notes"
   - "Compare Docker vs Podman"

## 🛠️ Available Tools

- **search_tools** - Discover development tools and frameworks
- **search_github_repositories** - Find GitHub repositories
- **analyze_repository** - Analyze code structure and quality
- **search_web** - Web search via Brave API
- **perplexity_search** - AI-powered search results
- **read_notion_page** - Access Notion page content
- **search_notion_page** - Search within Notion documents
- **add_to_notion_page** - Add content to Notion pages

## � Docker Commands

```bash
# Build and run
make build && make run

# Manual Docker commands
docker-compose build
docker-compose up -d

# Check status
docker-compose ps
make health

# View logs
docker-compose logs -f

# Stop services
make stop
docker-compose down
```

## � Project Structure

```
├── app.py                 # Main Streamlit application
├── server.py              # FastAPI tool server
├── tool_recommendation/   # Core MCP tools
├── docker-compose.yml     # Docker configuration
├── Makefile              # Build commands
└── requirements.txt       # Dependencies
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test
4. Submit pull request

---

**Built with OpenAI GPT-4, FastMCP, and Streamlit for an intelligent development experience** 🚀
