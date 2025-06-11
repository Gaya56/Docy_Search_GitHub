# Docy Search Documentation

Welcome to the comprehensive documentation for Docy Search - an AI-powered tool recommendation assistant.

## 📚 Documentation Structure

### Quick Reference
- **[Overview](./01-overview.md)** - Application purpose, features, and architecture
- **[Installation & Setup](./02-installation.md)** - Getting started guide
- **[API Reference](./03-api-reference.md)** - Functions, classes, and methods
- **[Components Guide](./04-components.md)** - Core modules and their responsibilities
- **[Configuration](./05-configuration.md)** - Settings, environment variables, and customization
- **[Database Schema](./06-database.md)** - SQLite database structure and operations
- **[Development Guide](./07-development.md)** - Contributing and extending the application

## 🚀 Quick Start

1. **Web Interface** (Recommended):
   ```bash
   streamlit run docy_search/main_ui.py
   ```

2. **Command Line Interface**:
   ```bash
   python docy_search/app.py
   ```

3. **Access**: Open http://localhost:8501 for the web interface

## 📖 What is Docy Search?

Docy Search is an intelligent AI assistant that helps developers discover, analyze, and implement the best tools for their projects. It combines:

- **AI-Powered Analysis** using OpenAI, Claude, Gemini, and DeepSeek models
- **Live Web Search** via Brave Search API
- **GitHub Integration** for repository access and code examples  
- **Semantic Memory** to remember your preferences and conversations
- **SQLite Database** for zero-configuration data persistence
- **Modern Web UI** built with Streamlit

## 🎯 Key Features

- **Tool Recommendation Engine**: Find and analyze development tools
- **Multi-Model AI Support**: Choose from 4 different AI models
- **Memory System**: Conversations are remembered across sessions
- **Activity Tracking**: Live monitoring of tool usage and API calls
- **Database Viewer**: Browse chat history and system data
- **Dashboard Generation**: AI-powered analytics dashboards
- **Cost Monitoring**: Track API usage and costs

## 📁 Project Structure

```
docy_search/
├── app.py                    # Main CLI application
├── main_ui.py               # Streamlit web interface
├── tool_recommendation/     # Tool discovery and analysis
├── memory/                  # Semantic memory system
├── database/               # SQLite data management
├── ui/                     # Web UI components
└── dashboard/              # Analytics and reporting
```

## 🔧 Technology Stack

- **Backend**: Python 3.11+, Pydantic AI, AsyncIO
- **AI Models**: OpenAI GPT-4, Claude 3, Gemini 1.5, DeepSeek
- **Database**: SQLite with async support
- **Frontend**: Streamlit with custom components
- **APIs**: Brave Search, GitHub, OpenAI Embeddings
- **Protocols**: MCP (Model Context Protocol) for tool integration

---

For detailed information, see the individual documentation files linked above.
