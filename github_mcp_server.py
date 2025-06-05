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
    try:
        search_query = query
        if language:
            search_query += f" language:{language}"
        
        params = {
            "q": search_query,
            "sort": "stars",
            "order": "desc",
            "per_page": min(limit, 10)
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{github_base_url}/search/repositories",
                headers=github_headers,
                params=params
            ) as response:
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
                    
                    return json.dumps(result, indent=2)
                else:
                    return f"Error searching GitHub repositories: HTTP {response.status}"
    
    except Exception as e:
        return f"Error searching GitHub repositories: {str(e)}"

@mcp.tool()
async def get_repository_structure(repo_full_name: str) -> str:
    """
    Get the file structure of a GitHub repository.
    
    Args:
        repo_full_name: Repository name in format "owner/repo"
    
    Returns:
        JSON string with repository structure and key files
    """
    try:
        url = f"{github_base_url}/repos/{repo_full_name}/contents/"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=github_headers) as response:
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
                    
                    return json.dumps(result, indent=2)
                else:
                    return f"Error getting repository structure: HTTP {response.status}"
    
    except Exception as e:
        return f"Error getting repository structure: {str(e)}"

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
    try:
        url = f"{github_base_url}/repos/{repo_full_name}/contents/{file_path}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=github_headers) as response:
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
                        
                        return json.dumps(result, indent=2)
                    else:
                        return f"Error: {file_path} is not a file"
                else:
                    return f"Error getting file content: HTTP {response.status}"
    
    except Exception as e:
        return f"Error getting file content: {str(e)}"

if __name__ == "__main__":
    mcp.run()
