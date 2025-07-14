#!/usr/bin/env python3
"""
Unified MCP Server for Tool Recommendation System

This server aggregates all MCP tools into a single endpoint
that can be easily integrated into any chatbot or application.
"""

import asyncio
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

# Import all MCP servers
try:
    from tool_recommendation.mcp_server import mcp as main_mcp
    from tool_recommendation.brave_search import mcp as brave_mcp
    from tool_recommendation.github_mcp_server import mcp as github_mcp
    from tool_recommendation.code_analyzer import mcp as code_analyzer_mcp
    from tool_recommendation.python_tools import mcp as python_mcp
    from tool_recommendation.sql_tools import mcp as sql_mcp
    from tool_recommendation.perplexity_search import mcp as perplexity_mcp
    from tool_recommendation.activity_tracker import activity_tracker
except ImportError as e:
    print(f"Error importing MCP servers: {e}")
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
    "search_tools": main_mcp,
    "analyze_tools": main_mcp,
    "get_installation_guide": main_mcp,
    "compare_tools": main_mcp,
    
    # Web search tools
    "search_web": brave_mcp,
    
    # GitHub tools
    "search_github_repositories": github_mcp,
    "get_repository_structure": github_mcp,
    "get_file_from_repository": github_mcp,
    
    # Code analysis tools
    "analyze_repository": code_analyzer_mcp,
    "get_code_quality_metrics": code_analyzer_mcp,
    
    # Python tools
    "python_repl": python_mcp,
    "data_visualization": python_mcp,
    
    # SQL tools
    "natural_language_query": sql_mcp,
    "execute_sql_query": sql_mcp,
    
    # Perplexity search
    "perplexity_search": perplexity_mcp,
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
    """Execute a tool with given parameters."""
    try:
        tool_name = request.tool_name
        parameters = request.parameters
        
        if tool_name not in AVAILABLE_TOOLS:
            raise HTTPException(
                status_code=400, 
                detail=f"Tool '{tool_name}' not found. Available tools: {list(AVAILABLE_TOOLS.keys())}"
            )
        
        mcp_server = AVAILABLE_TOOLS[tool_name]
        
        # Get the tool function from the MCP server
        tool_func = None
        if hasattr(mcp_server, '_tools') and tool_name in mcp_server._tools:
            tool_func = mcp_server._tools[tool_name]
        elif hasattr(mcp_server, 'tools') and tool_name in mcp_server.tools:
            tool_func = mcp_server.tools[tool_name]
        else:
            # Try to find the function by name
            tool_func = getattr(mcp_server, tool_name, None)
        
        if not tool_func:
            raise HTTPException(
                status_code=500,
                detail=f"Tool function '{tool_name}' not found in server"
            )
        
        # Execute the tool
        if asyncio.iscoroutinefunction(tool_func):
            result = await tool_func(**parameters)
        else:
            result = tool_func(**parameters)
        
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
    # Ensure data directory exists
    os.makedirs("/app/data", exist_ok=True)
    
    # Start the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
