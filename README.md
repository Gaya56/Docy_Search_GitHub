# Docy Search GitHub - AI Tool Assistant

An intelligent chatbot that uses OpenAI to understand user queries and execute tools from different MCP servers.

## Features

- 🖥️ **MCP Server Selection**: Choose from GitHub, Notion, Tool Recommendation, Web Search, and SQL Database servers
- 🛠️ **Tool Selection**: Pick specific tools from each server via dropdown interface
- 🤖 **AI-Powered**: Uses OpenAI GPT-4 for intelligent parameter parsing
- 💬 **Streamlit UI**: Clean, modern interface for tool interaction
- 🔧 **Multiple Integrations**: GitHub repos, Notion pages, web search, and more

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start the server**:
   ```bash
   python server.py
   ```

4. **Launch the UI**:
   ```bash
   streamlit run app.py
   ```

5. **Use the interface**:
   - Configure OpenAI API key in sidebar
   - Connect to tool server
   - Select MCP server (e.g., GitHub, Notion)
   - Choose specific tool from dropdown
   - Enter parameters and execute

## MCP Servers

- **GitHub**: Repository search, file analysis, code summaries
- **Notion**: Page reading, searching, content creation
- **Tool Recommendation**: Development tool discovery and analysis
- **Web Search**: Brave and Perplexity search integration
- **SQL Database**: Natural language database queries

## Architecture

```
├── app.py              # Streamlit UI
├── server.py           # FastAPI MCP server
├── client.py           # Python client library
└── tool_recommendation/ # MCP server implementations
```

## License

MIT License
