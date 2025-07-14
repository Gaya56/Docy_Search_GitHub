# MCP Integration

This folder contains MCP (Model Context Protocol) servers that we analyze and integrate into our main application.

## Purpose

This directory serves as a staging area where we:

1. **Store original MCP server implementations** for analysis
2. **Compare external MCP servers** with our application structure
3. **Test compatibility** before integration
4. **Document integration process** and findings
5. **Maintain reference implementations** for future updates

## Integration Workflow

### 1. Analysis Phase
- Clone or download the original MCP server code
- Study the server's API, tools, and functionality
- Identify required dependencies and configuration
- Document the server's capabilities and limitations

### 2. Comparison Phase
- Compare the external server structure with our `tool_recommendation/` implementations
- Identify differences in:
  - Tool function signatures
  - Parameter handling
  - Error handling
  - Authentication methods
  - Response formats

### 3. Integration Phase
- Create a new file in `tool_recommendation/` (e.g., `new_mcp_server.py`)
- Implement tools using our FastMCP framework
- Add server configuration to `server.py`
- Update `app.py` with new function definitions
- Test the integration thoroughly

### 4. Documentation Phase
- Update this README with integration notes
- Document any special configuration requirements
- Add usage examples for the new tools

## Current MCP Servers

### ✅ Integrated Servers
- **GitHub MCP Server** → `tool_recommendation/github_mcp_server.py`
- **Notion MCP Server** → `tool_recommendation/notion_mcp_server.py`
- **Tool Recommendation** → `tool_recommendation/mcp_server.py`
- **Web Search** → `tool_recommendation/brave_search.py`, `tool_recommendation/perplexity_search.py`
- **SQL Database** → `tool_recommendation/sql_tools.py`

### 🔄 Analysis/Testing Servers
- **notion_mcp_agent** - Terminal-based Notion agent for reference

## Integration Checklist

When integrating a new MCP server:

- [ ] Analyze original server code and documentation
- [ ] Identify required environment variables and API keys
- [ ] Create implementation file in `tool_recommendation/`
- [ ] Add server to `MCP_SERVERS` dictionary in `server.py`
- [ ] Update tool parameter definitions in `app.py`
- [ ] Test server endpoints (`/mcp-servers`, `/mcp-servers/{name}/tools`)
- [ ] Test tool execution through Streamlit UI
- [ ] Update main README.md with new server information
- [ ] Document any special setup requirements

## File Structure

```
MCP Integration/
├── README.MD                 # This file
├── notion_mcp_agent/        # Reference Notion implementation
│   ├── README.MD
│   ├── notion_mcp_agent.py
│   └── requirements.txt
└── [future_mcp_servers]/    # Additional servers for analysis
```

## Best Practices

1. **Always analyze before integrating** - Understand the original implementation
2. **Maintain consistency** - Follow our existing patterns and conventions
3. **Test thoroughly** - Verify all tools work correctly in both API and UI
4. **Document everything** - Keep clear notes of changes and decisions
5. **Preserve references** - Keep original implementations for future updates

## Adding New MCP Servers

To add a new MCP server for analysis:

1. Create a new folder with the server name
2. Add the original server code
3. Include a README.MD with:
   - Server description
   - Original source/repository
   - Analysis notes
   - Integration status
   - Any special requirements

## Notes

- This folder is for development and analysis purposes
- Production integrations go in `tool_recommendation/`
- Keep original implementations as reference
- Document any modifications or adaptations made during integration
