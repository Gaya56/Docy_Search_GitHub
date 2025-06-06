#!/usr/bin/env python3
"""
Live GitHub MCP Demo

This script demonstrates the GitHub MCP tools with live activity tracking.
Run this alongside the Streamlit UI to see real-time progress updates.
"""

import asyncio
import sys
import os

# Add the current directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def demo_github_search():
    """Demo the GitHub repository search with live tracking"""
    
    print("🚀 Starting GitHub MCP Demo with Live Activity Tracking")
    print("=" * 60)
    print("📌 Make sure your Streamlit UI is running to see live updates!")
    print("   Run: streamlit run main_ui.py")
    print()
    
    try:
        # Import the GitHub MCP server functions
        from github_mcp_server import search_github_repositories, get_repository_structure, get_file_from_repository
        
        print("🔍 Demo 1: Searching for React component libraries...")
        result1 = await search_github_repositories(
            query="react component library",
            language="javascript", 
            limit=3
        )
        print("✅ Search completed! Check Streamlit UI for live progress updates.")
        print(f"📊 Found repositories: {len(result1.split('Repository:')) - 1 if 'Repository:' in result1 else 0}")
        print()
        
        # Small delay to show the tracking
        await asyncio.sleep(2)
        
        print("🏗️ Demo 2: Getting React repository structure...")
        result2 = await get_repository_structure(
            owner="facebook",
            repo="react",
            path="packages/react/src"
        )
        print("✅ Structure analysis completed! Check Streamlit UI for progress.")
        print()
        
        # Small delay to show the tracking
        await asyncio.sleep(2)
        
        print("📄 Demo 3: Getting React package.json file...")
        result3 = await get_file_from_repository(
            owner="facebook",
            repo="react", 
            file_path="package.json"
        )
        print("✅ File retrieval completed! Check Streamlit UI for details.")
        print()
        
        print("🎉 Demo completed successfully!")
        print("📊 Check your Streamlit UI to see:")
        print("   • Live progress bars during operations")
        print("   • Real-time activity status updates")
        print("   • Resource usage metrics")
        print("   • API cost tracking")
        print("   • Complete activity history")
        
    except ImportError as e:
        print(f"❌ Could not import GitHub MCP functions: {e}")
        print("   Make sure github_mcp_server.py is in the current directory")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("   Check your GitHub token configuration")

async def main():
    """Main demo function"""
    print("⚡ Starting Live GitHub MCP Demo...")
    print()
    
    # Check if activity tracker is available
    try:
        from activity_tracker import activity_tracker
        print("✅ Activity tracker is available - live updates will work!")
    except ImportError:
        print("⚠️ Activity tracker not found - demo will run without live tracking")
    
    print()
    await demo_github_search()

if __name__ == "__main__":
    asyncio.run(main())
