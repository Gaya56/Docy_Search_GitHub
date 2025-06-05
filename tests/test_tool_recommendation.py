#!/usr/bin/env python3
"""
Test script for the Tool Recommendation System
Run this to verify the MCP server is working correctly
"""

import asyncio
import os
from dotenv import load_dotenv
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()

async def test_tool_recommendation():
    """Test the tool recommendation MCP server"""
    
    print("🔧 Testing Tool Recommendation System...")
    
    # Check environment variables
    required_vars = ['BRAVE_API_KEY', 'GOOGLE_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please add them to your .env file")
        return False
    
    print("✅ Environment variables found")
    
    # Test MCP server startup
    try:
        server = MCPServerStdio(
            'python',
            ['tool_recommendation/mcp_server.py']
        )
        
        print("✅ MCP server initialized successfully")
        
        # Test server connection (basic)
        async with server:
            print("✅ MCP server connection test passed")
            
        print("\n🎉 Tool Recommendation System is ready!")
        print("\nYou can now use the following commands in the chat:")
        print("- 'I need tools for web development'")
        print("- 'Compare React vs Angular vs Vue.js'")
        print("- 'How do I install Docker on Ubuntu?'")
        print("- 'What tools should I use for mobile app development?'")
        print("- 'Best data analysis tools for Python'")
        print("- 'Setup a complete DevOps toolchain'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing MCP server: {str(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_tool_recommendation())
    exit(0 if success else 1)
