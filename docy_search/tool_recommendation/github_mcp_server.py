#!/usr/bin/env python3
"""
GitHub MCP Server for repository discovery and code analysis.
Provides tools to search GitHub repositories, get file contents, and analyze project structures.
"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import json
import asyncio
import aiohttp
import base64
from typing import Dict, List, Optional, Any

# Import activity tracking with graceful fallback
try:
    from .activity_tracker import activity_tracker
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    print("Activity tracking not available - running without tracking")

load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP(
    name="github", 
    version="1.0.0",
    description="GitHub repository search and analysis"
)

# Initialize GitHub API configuration
github_token = os.getenv("GITHUB_TOKEN", "")
github_base_url = "https://api.github.com"
github_headers = {
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "Tool-Recommendation-System"
}
if github_token:
    github_headers["Authorization"] = f"token {github_token}"

@mcp.tool()
async def search_github_repositories(query: str, language: str = "", limit: int = 5) -> str:
    """
    Search GitHub repositories for tools and projects.
    
    Args:
        query: Search query (e.g., "react components", "python web framework")
        language: Filter by programming language (optional)
        limit: Maximum number of results (default: 5, max: 10)
    
    Returns:
        JSON string with repository information including links, descriptions, and stats
    """
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="search_github_repositories",
                params={
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "language": language,
                    "limit": limit
                }
            )
            await activity_tracker.update_activity(activity_id, progress=20, details={"status": "Preparing GitHub search"})
        
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        params = {
            "q": search_query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 10)
        }
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=40, details={"status": "Sending GitHub API request"})
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{github_base_url}/search/repositories",
                headers=github_headers,
                params=params
            ) as response:
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Processing repository results"})
                
                if response.status == 200:
                    data = await response.json()
                    
                    result = {
                        "search_query": query,
                        "total_found": len(data.get("items", [])),
                        "repositories": []
                    }
                    
                    for item in data.get("items", []):
                        result["repositories"].append({
                            "name": item["name"],
                            "full_name": item["full_name"],
                            "description": item.get("description", ""),
                            "url": item["html_url"],
                            "stars": item["stargazers_count"],
                            "language": item.get("language", ""),
                            "topics": item.get("topics", []),
                            "last_updated": item["updated_at"]
                        })
                    
                    # Complete activity tracking with success
                    if TRACKING_AVAILABLE and activity_id:
                        result_preview = f"Found {len(result['repositories'])} repositories for: {query[:50]}{'...' if len(query) > 50 else ''}"
                        await activity_tracker.complete_activity(activity_id, result=result_preview)
                    
                    return json.dumps(result, indent=2)
                else:
                    error_msg = f"Error searching GitHub repositories: HTTP {response.status}"
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=f"GitHub search failed: HTTP {response.status}")
                    return error_msg
    
    except Exception as e:
        error_msg = f"Error searching GitHub repositories: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"GitHub search error: {str(e)[:100]}")
        return error_msg

@mcp.tool()
async def get_repository_structure(repo_full_name: str) -> str:
    """
    Get the file structure of a GitHub repository.
    
    Args:
        repo_full_name: Repository name in format "owner/repo"
    
    Returns:
        JSON string with repository structure and key files
    """
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="get_repository_structure",
                params={"repo_full_name": repo_full_name}
            )
            await activity_tracker.update_activity(activity_id, progress=30, details={"status": "Fetching repository structure"})
        
        url = f"{github_base_url}/repos/{repo_full_name}/contents/"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=github_headers) as response:
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Processing repository structure"})
                
                if response.status == 200:
                    files = await response.json()
                    
                    # Identify key files
                    key_files = []
                    important_files = [
                        "README.md", "package.json", "requirements.txt", "Cargo.toml",
                        "pom.xml", "build.gradle", "Dockerfile", "docker-compose.yml",
                        "main.py", "index.js", "App.js", "main.go", "main.rs"
                    ]
                    
                    structure = []
                    for file in files:
                        item = {
                            "name": file["name"],
                            "path": file["path"],
                            "type": file["type"],
                            "size": file.get("size", 0)
                        }
                        structure.append(item)
                        
                        if file["name"] in important_files:
                            key_files.append(item)
                    
                    result = {
                        "repository": repo_full_name,
                        "structure": structure,
                        "key_files": key_files
                    }
                    
                    # Complete activity tracking with success
                    if TRACKING_AVAILABLE and activity_id:
                        result_preview = f"Analyzed {len(structure)} files/folders in {repo_full_name}, found {len(key_files)} key files"
                        await activity_tracker.complete_activity(activity_id, result=result_preview)
                    
                    return json.dumps(result, indent=2)
                else:
                    error_msg = f"Error getting repository structure: HTTP {response.status}"
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=f"Repository structure error: HTTP {response.status}")
                    return error_msg
    
    except Exception as e:
        error_msg = f"Error getting repository structure: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"Repository structure error: {str(e)[:100]}")
        return error_msg

@mcp.tool()
async def get_file_from_repository(repo_full_name: str, file_path: str) -> str:
    """
    Get the content of a specific file from a GitHub repository.
    
    Args:
        repo_full_name: Repository name in format "owner/repo"
        file_path: Path to the file in the repository
    
    Returns:
        JSON string with file content and metadata
    """
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="get_file_from_repository",
                params={"repo_full_name": repo_full_name, "file_path": file_path}
            )
            await activity_tracker.update_activity(activity_id, progress=30, details={"status": "Fetching file content"})
        
        url = f"{github_base_url}/repos/{repo_full_name}/contents/{file_path}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=github_headers) as response:
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Processing file content"})
                
                if response.status == 200:
                    data = await response.json()
                    if data["type"] == "file":
                        # Decode base64 content
                        content = base64.b64decode(data["content"]).decode('utf-8')
                        
                        # Truncate very large files
                        if len(content) > 10000:
                            content = content[:10000] + "\n\n... (file truncated, showing first 10000 characters)"
                        
                        result = {
                            "repository": repo_full_name,
                            "file_path": file_path,
                            "file_name": data["name"],
                            "size": data["size"],
                            "download_url": data["download_url"],
                            "content": content
                        }
                        
                        # Complete activity tracking with success
                        if TRACKING_AVAILABLE and activity_id:
                            result_preview = f"Retrieved {data['name']} ({data['size']} bytes) from {repo_full_name}"
                            await activity_tracker.complete_activity(activity_id, result=result_preview)
                        
                        return json.dumps(result, indent=2)
                    else:
                        error_msg = f"Error: {file_path} is not a file"
                        if TRACKING_AVAILABLE and activity_id:
                            await activity_tracker.complete_activity(activity_id, result=error_msg)
                        return error_msg
                else:
                    error_msg = f"Error getting file content: HTTP {response.status}"
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=f"File retrieval error: HTTP {response.status}")
                    return error_msg
    
    except Exception as e:
        error_msg = f"Error getting file content: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"File retrieval error: {str(e)[:100]}")
        return error_msg

if __name__ == "__main__":
    mcp.run()
