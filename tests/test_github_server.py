#!/usr/bin/env python3
"""
Test script for GitHub MCP Server functionality
"""

import asyncio
import json
from github_mcp_server import github_client

async def test_github_server():
    print("🔍 Testing GitHub MCP Server...\n")
    
    try:
        # Test 1: Search for React repositories
        print("1. Testing repository search...")
        repos = await github_client.search_repositories("react component library", "javascript", limit=3)
        print(f"   ✅ Found {len(repos)} React repositories")
        for repo in repos[:2]:
            print(f"   - {repo.full_name} ({repo.stars} stars)")
        
        # Test 2: Get repository structure
        if repos:
            print(f"\n2. Testing repository structure for {repos[0].full_name}...")
            try:
                files = await github_client.get_repository_files(repos[0].full_name)
                print(f"   ✅ Found {len(files)} files/directories in root")
                for file in files[:5]:
                    print(f"   - {file['name']} ({file['type']})")
            except Exception as e:
                print(f"   ⚠️ Could not access repository structure: {e}")
        
        # Test 3: Search for a popular tool
        print(f"\n3. Testing search for a popular tool (Express.js)...")
        express_repos = await github_client.search_repositories("expressjs", "javascript", limit=2)
        print(f"   ✅ Found {len(express_repos)} Express.js repositories")
        for repo in express_repos:
            print(f"   - {repo.full_name} ({repo.stars} stars)")
        
        print(f"\n✅ GitHub MCP Server is working correctly!")
        print(f"🔑 GitHub token is {'configured' if github_client.token else 'NOT configured'}")
        
    except Exception as e:
        print(f"❌ Error testing GitHub server: {e}")
        print("Make sure your GITHUB_TOKEN is set in .env file")

if __name__ == "__main__":
    asyncio.run(test_github_server())
