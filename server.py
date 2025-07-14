#!/usr/bin/env python3
"""
Unified MCP Server for Tool Recommendation System

This server aggregates all MCP tools into a single endpoint
that can be easily integrated into any chatbot or application.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging

# Add the tool_recommendation directory to the path
sys.path.insert(0, str(Path(__file__).parent))

# Import individual tool functions directly
try:
    from tool_recommendation.mcp_server import search_tools, analyze_tools, get_installation_guide, compare_tools
    from tool_recommendation.brave_search import search_web
    from tool_recommendation.github_mcp_server import search_github_repositories, get_repository_structure, get_file_from_repository
    from tool_recommendation.code_analyzer import analyze_repository, quick_repo_summary
    from tool_recommendation.sql_tools import natural_language_query, get_database_schema
    from tool_recommendation.perplexity_search import perplexity_search
    from tool_recommendation.notion_mcp_server import read_notion_page, search_notion_page, add_to_notion_page
    from tool_recommendation.activity_tracker import activity_tracker
except ImportError as e:
    print(f"Error importing tool functions: {e}")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Tool Recommendation MCP Server",
    description="Unified MCP server for AI-powered tool discovery and analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ToolRequest(BaseModel):
    tool_name: str
    parameters: Dict[str, Any]
    notion_api_key: Optional[str] = None
    notion_page_id: Optional[str] = None

class ToolResponse(BaseModel):
    success: bool
    result: Optional[str] = None
    error: Optional[str] = None
    activity_id: Optional[int] = None

class ActivityResponse(BaseModel):
    current_activity: Optional[Dict[str, Any]] = None
    recent_activities: list = []
    resource_usage: Dict[str, Any] = {}
    total_activities: int = 0

# Available tools mapping
AVAILABLE_TOOLS = {
    # Main tool recommendation tools
    "search_tools": search_tools,
    "analyze_tools": analyze_tools,
    "get_installation_guide": get_installation_guide,
    "compare_tools": compare_tools,
    
    # Web search tools
    "search_web": search_web,
    
    # GitHub tools
    "search_github_repositories": search_github_repositories,
    "get_repository_structure": get_repository_structure,
    "get_file_from_repository": get_file_from_repository,
    
    # Code analysis tools
    "analyze_repository": analyze_repository,
    "quick_repo_summary": quick_repo_summary,
    
    # SQL tools
    "natural_language_query": natural_language_query,
    "get_database_schema": get_database_schema,
    
    # Perplexity search
    "perplexity_search": perplexity_search,
    
    # Notion tools
    "read_notion_page": read_notion_page,
    "search_notion_page": search_notion_page,
    "add_to_notion_page": add_to_notion_page,
}

@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "Tool Recommendation MCP Server",
        "version": "1.0.0",
        "status": "running",
        "available_tools": list(AVAILABLE_TOOLS.keys()),
        "activity_tracking": True
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker."""
    return {"status": "healthy", "timestamp": "now"}

@app.get("/tools")
async def list_tools():
    """List all available tools."""
    tools_info = {}
    for tool_name, mcp_server in AVAILABLE_TOOLS.items():
        # Get tool information from MCP server
        tools_info[tool_name] = {
            "name": tool_name,
            "server": mcp_server.name if hasattr(mcp_server, 'name') else "unknown",
            "description": f"Tool for {tool_name.replace('_', ' ')}"
        }
    return {"tools": tools_info}

@app.post("/execute")
async def execute_tool(request: ToolRequest) -> ToolResponse:
    """Execute a tool with the given parameters."""
    try:
        # Set Notion credentials if provided
        if request.notion_api_key:
            os.environ["NOTION_API_KEY"] = request.notion_api_key
        if request.notion_page_id:
            os.environ["NOTION_PAGE_ID"] = request.notion_page_id
        
        # Track the activity
        activity_tracker.start_activity(
            f"execute_{request.tool_name}",
            {"tool": request.tool_name, "parameters": request.parameters}
        )
        
        # Get the tool function
        tool_name = request.tool_name
        parameters = request.parameters or {}
        
        # Import and call the function directly
        if tool_name == "search_tools":
            from tool_recommendation.mcp_server import search_tools
            result = await search_tools.fn(**parameters)
        elif tool_name == "analyze_tools":
            from tool_recommendation.mcp_server import analyze_tools
            result = await analyze_tools.fn(**parameters)
        elif tool_name == "get_installation_guide":
            from tool_recommendation.mcp_server import get_installation_guide
            result = await get_installation_guide.fn(**parameters)
        elif tool_name == "compare_tools":
            from tool_recommendation.mcp_server import compare_tools
            result = await compare_tools.fn(**parameters)
        elif tool_name == "search_web":
            from tool_recommendation.brave_search import search_web
            result = await search_web.fn(**parameters)
        elif tool_name == "search_github_repositories":
            from tool_recommendation.github_mcp_server import search_github_repositories
            result = await search_github_repositories.fn(**parameters)
        elif tool_name == "get_repository_structure":
            from tool_recommendation.github_mcp_server import get_repository_structure
            result = await get_repository_structure.fn(**parameters)
        elif tool_name == "get_file_from_repository":
            from tool_recommendation.github_mcp_server import get_file_from_repository
            result = await get_file_from_repository.fn(**parameters)
        elif tool_name == "analyze_repository":
            from tool_recommendation.code_analyzer import analyze_repository
            result = await analyze_repository.fn(**parameters)
        elif tool_name == "quick_repo_summary":
            from tool_recommendation.code_analyzer import quick_repo_summary
            result = await quick_repo_summary.fn(**parameters)
        elif tool_name == "natural_language_query":
            from tool_recommendation.sql_tools import natural_language_query
            result = await natural_language_query.fn(**parameters)
        elif tool_name == "get_database_schema":
            from tool_recommendation.sql_tools import get_database_schema
            result = await get_database_schema.fn(**parameters)
        elif tool_name == "perplexity_search":
            from tool_recommendation.perplexity_search import perplexity_search
            result = await perplexity_search.fn(**parameters)
        elif tool_name == "read_notion_page":
            from tool_recommendation.notion_mcp_server import read_notion_page
            result = await read_notion_page.fn(**parameters)
        elif tool_name == "search_notion_page":
            from tool_recommendation.notion_mcp_server import search_notion_page
            result = await search_notion_page.fn(**parameters)
        elif tool_name == "add_to_notion_page":
            from tool_recommendation.notion_mcp_server import add_to_notion_page
            result = await add_to_notion_page.fn(**parameters)
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Tool function '{tool_name}' implementation not found"
            )
        
        return ToolResponse(
            success=True,
            result=str(result),
            activity_id=getattr(activity_tracker, '_activity_id', None)
        )
        
    except Exception as e:
        logger.error(f"Error executing tool '{request.tool_name}': {e}")
        return ToolResponse(
            success=False,
            error=str(e)
        )

@app.get("/activity")
async def get_activity_status() -> ActivityResponse:
    """Get current activity status and recent activity log."""
    try:
        summary = activity_tracker.get_activity_summary()
        return ActivityResponse(
            current_activity=summary.get("current"),
            recent_activities=summary.get("recent", []),
            resource_usage=summary.get("resources", {}),
            total_activities=summary.get("total_activities", 0)
        )
    except Exception as e:
        logger.error(f"Error getting activity status: {e}")
        return ActivityResponse()

@app.post("/streamlit-integration")
async def streamlit_integration(request: ToolRequest) -> ToolResponse:
    """
    Special endpoint optimized for Streamlit integration.
    Handles tool execution with proper error handling and progress tracking.
    """
    return await execute_tool(request)

def main():
    """Main entry point for the server."""
    # Ensure data directory exists (use local path when not in container)
    data_dir = "/app/data" if os.path.exists("/app") else "./data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Start the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8947,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
