# Notion MCP Agent (Reference Implementation)

A terminal-based Notion agent for interacting with Notion pages using natural language.

**Status**: Reference implementation for analysis and comparison

## Purpose

This is a standalone terminal-based Notion agent that serves as a reference implementation for understanding how to integrate with the official Notion MCP server. It demonstrates:

- Direct integration with the official `@notionhq/notion-mcp-server` npm package
- Conversational interface with session memory
- Terminal-based interaction patterns
- Different architectural approach compared to our web-based implementation

## Features

- Command-line interface for Notion pages
- Natural language operations (read, search, update)
- Session management and conversation context
- Block operations (create, edit, comment)
- Uses the `agno` framework for agent capabilities

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables:
   ```bash
   export NOTION_API_KEY=your_notion_key
   export OPENAI_API_KEY=your_openai_key
   ```
3. Run: `python notion_mcp_agent.py`

## Usage

- Start the agent and interact with your Notion pages
- Use natural language to describe what you want to do
- Type 'quit' to exit

## Integration Notes

This implementation differs from our main application's Notion integration in several ways:

- **Architecture**: Uses external MCP server vs our FastAPI integration
- **Interface**: Terminal CLI vs web UI
- **Framework**: `agno` framework vs direct API calls
- **Dependencies**: Requires npm package vs Python-only
- **User Experience**: Conversational vs tool selection

## Comparison with Main App

| Feature | This Implementation | Main App Integration |
|---------|-------------------|----------------------|
| Interface | Terminal CLI | Web UI (Streamlit) |
| MCP Server | External npm package | Custom Python implementation |
| User Flow | Conversational | Tool selection dropdown |
| Memory | Session-based | Stateless |
| Dependencies | npm + Python | Python only |

This serves as a valuable reference for understanding different approaches to MCP server integration.
