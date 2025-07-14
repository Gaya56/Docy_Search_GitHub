# 🚀 Quick Setup Guide

## 📋 System Overview

An AI-powered tool recommendation system with Notion integration, featuring:
- **OpenAI GPT-4** for intelligent tool selection
- **Notion Integration** for document management
- **GitHub, Web Search, and Database tools**
- **Streamlit UI** with Docker backend

---

## ⚡ Quick Start (5 minutes)

### 1. Prerequisites
```bash
# Check requirements
docker --version
python --version  # 3.8+
```

### 2. Setup
```bash
# Clone and setup environment
git clone https://github.com/Gaya56/Docy_Search_GitHub.git
cd Docy_Search_GitHub
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your OpenAI API key (required)
```

### 3. Start Services
```bash
# Terminal 1: Start Docker backend
make build && make run

# Terminal 2: Start Streamlit UI
source .venv/bin/activate
streamlit run app.py
```

### 4. Access
- **Web UI**: http://localhost:8501
- **API**: http://localhost:8947

---

## � Essential Commands

### Docker Management
```bash
# Build and start
make build && make run

# Alternative Docker commands
docker-compose build
docker-compose up -d

# Check status
make health
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
make stop
docker-compose down
```

### Development
```bash
# Activate environment
source .venv/bin/activate

# Start Streamlit
streamlit run app.py

# Test API
curl http://localhost:8947/health
```

---

## 🔑 Required Configuration

### Minimal Setup (OpenAI only)
```bash
# .env file
OPENAI_API_KEY=your_openai_key_here
```

### Full Features (Optional)
```bash
# .env file
OPENAI_API_KEY=your_openai_key_here
BRAVE_API_KEY=your_brave_key
PERPLEXITY_API_KEY=your_perplexity_key
GITHUB_TOKEN=your_github_token
NOTION_API_KEY=your_notion_key
NOTION_PAGE_ID=your_default_page_id
```

---

## 🛠️ Available Tools

| Tool | Description |
|------|-------------|
| `search_tools` | Find development tools |
| `search_github_repositories` | Search GitHub repos |
| `search_web` | Web search via Brave |
| `perplexity_search` | AI-powered search |
| `read_notion_page` | Read Notion content |
| `search_notion_page` | Search Notion docs |
| `add_to_notion_page` | Add to Notion |

---

## 🐛 Troubleshooting

### Common Issues
```bash
# Port conflicts
netstat -tulpn | grep 8947
netstat -tulpn | grep 8501

# Docker issues
docker system prune -f
docker-compose down --volumes

# Python environment
pip install -r requirements.txt --force-reinstall
```

### Health Checks
```bash
# Container status
docker-compose ps

# API health
curl http://localhost:8947/health

# Available tools
curl http://localhost:8947/tools
```

---

## 📁 Project Structure

```
├── app.py                 # Streamlit UI
├── server.py              # FastAPI backend
├── tool_recommendation/   # MCP tools
├── docker-compose.yml     # Docker config
├── Makefile              # Commands
└── requirements.txt       # Dependencies
```

---

## ✅ Success Checklist

- [ ] Docker container running on port 8947
- [ ] Streamlit UI accessible on port 8501
- [ ] OpenAI API key configured
- [ ] Health check returns `{"status":"healthy"}`
- [ ] Tools list shows available functions

**🎉 You're ready to start using the AI tool assistant!**
