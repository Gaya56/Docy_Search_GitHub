#!/usr/bin/env python3
"""
GitHub MCP Tools Usage Guide

This script demonstrates how to use the GitHub MCP tools in your app to analyze 
repositories, get code examples, and understand project structures.
"""

import asyncio
import json
from typing import Dict, List, Any

# Example prompts that will trigger GitHub MCP usage in your app
GITHUB_PROMPTS = {
    "repository_search": [
        "I need to find React component libraries on GitHub",
        "Search for Python web frameworks on GitHub",
        "Find GitHub repositories for machine learning tools",
        "Look for Vue.js UI component libraries",
        "Search GitHub for Node.js testing frameworks",
        "Find TypeScript utility libraries on GitHub"
    ],
    
    "code_analysis": [
        "Show me the structure of the React repository",
        "What's in the main files of the FastAPI repository?",
        "Analyze the architecture of the Next.js codebase",
        "Get the package.json from the Express.js repository",
        "Show me the main components in the Material-UI repository"
    ],
    
    "implementation_examples": [
        "How does React implement hooks? Show me the code",
        "Get implementation examples from the Django repository",
        "Show me how FastAPI handles dependency injection",
        "Find code examples for authentication in the Auth0 repository",
        "Get the main configuration files from the Webpack repository"
    ]
}

# Available GitHub MCP Tools
GITHUB_TOOLS = {
    "search_github_repositories": {
        "description": "Search for repositories on GitHub",
        "parameters": {
            "query": "Search query (e.g., 'react components')",
            "language": "Programming language filter (optional)",
            "limit": "Number of results (default: 5, max: 10)"
        },
        "example": "search_github_repositories('react hooks', language='javascript', limit=3)"
    },
    
    "get_repository_structure": {
        "description": "Get the file structure of a GitHub repository",
        "parameters": {
            "owner": "Repository owner (e.g., 'facebook')",
            "repo": "Repository name (e.g., 'react')",
            "path": "Specific path to explore (optional, defaults to root)"
        },
        "example": "get_repository_structure('facebook', 'react', 'packages/react/src')"
    },
    
    "get_file_from_repository": {
        "description": "Get the content of a specific file from a repository",
        "parameters": {
            "owner": "Repository owner",
            "repo": "Repository name", 
            "file_path": "Path to the file"
        },
        "example": "get_file_from_repository('facebook', 'react', 'package.json')"
    }
}

async def demonstrate_usage():
    """Demonstrate how the GitHub MCP tools work in practice"""
    
    print("🔍 GitHub MCP Tools Usage Guide")
    print("=" * 50)
    
    print("\n📋 Available Tools:")
    for tool_name, tool_info in GITHUB_TOOLS.items():
        print(f"\n🔧 {tool_name}")
        print(f"   Description: {tool_info['description']}")
        print(f"   Example: {tool_info['example']}")
    
    print("\n💬 Example Prompts That Trigger GitHub Tools:")
    
    for category, prompts in GITHUB_PROMPTS.items():
        print(f"\n📂 {category.replace('_', ' ').title()}:")
        for prompt in prompts:
            print(f"   • \"{prompt}\"")
    
    print("\n🚀 How It Works in Your App:")
    print("""
1. User asks a question about tools or repositories
2. Your agent determines if GitHub search would be helpful
3. Agent asks for permission: "I can search GitHub repositories for [purpose]. Continue? (y/n)"
4. If user agrees, agent uses GitHub MCP tools:
   - Searches repositories with search_github_repositories()
   - Analyzes structure with get_repository_structure()
   - Gets specific files with get_file_from_repository()
5. Agent provides comprehensive analysis with links and code examples
6. All activity is tracked in real-time via the Streamlit UI
    """)
    
    print("\n📊 Activity Tracking Integration:")
    print("""
When GitHub tools are used, you'll see in the Streamlit UI:
- Live progress updates during repository searches
- Real-time status of file retrievals
- Cost tracking for API calls
- Resource usage metrics
- Complete activity history with expandable details
    """)

if __name__ == "__main__":
    asyncio.run(demonstrate_usage())
