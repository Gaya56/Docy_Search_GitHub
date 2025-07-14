#!/usr/bin/env python3
"""
Test script for Notion MCP Server integration
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, '/workspaces/Docy_Search_GitHub')

# Load environment variables
load_dotenv()

async def test_notion_tools():
    """Test the Notion MCP tools"""
    print("🔧 Testing Notion MCP Server Integration")
    print("=" * 50)
    
    try:
        # Import the Notion tools
        from tool_recommendation.notion_mcp_server import (
            read_notion_page, 
            search_notion_page, 
            add_to_notion_page
        )
        
        print("✅ Notion MCP server imported successfully")
        
        # Check environment variables
        notion_token = os.getenv("NOTION_API_KEY")
        notion_page_id = os.getenv("NOTION_PAGE_ID")
        
        print(f"🔑 Notion API Key: {'✅ Present' if notion_token else '❌ Missing'}")
        print(f"📄 Notion Page ID: {'✅ Present' if notion_page_id else '❌ Missing'}")
        
        if not notion_token or not notion_page_id:
            print("\n⚠️ Cannot run tests without API key and page ID")
            return
        
        print(f"\n📋 Testing with Page ID: {notion_page_id}")
        
        # Test 1: Read page
        print("\n🔍 Test 1: Reading Notion page...")
        try:
            result = await read_notion_page()
            print("✅ Read page successful")
            print(f"📄 Result preview: {result[:200]}...")
        except Exception as e:
            print(f"❌ Read page failed: {e}")
        
        # Test 2: Search page
        print("\n🔍 Test 2: Searching Notion page...")
        try:
            result = await search_notion_page("test")
            print("✅ Search page successful")
            print(f"📄 Result preview: {result[:200]}...")
        except Exception as e:
            print(f"❌ Search page failed: {e}")
        
        # Test 3: Add content (optional - commented out to avoid modifying page)
        print("\n📝 Test 3: Add content test...")
        print("⚠️ Skipping add content test to avoid modifying your page")
        print("   To test, uncomment the lines in the test script")
        
        # Uncomment to test adding content:
        # try:
        #     result = await add_to_notion_page("Test content from integration", "", "paragraph")
        #     print("✅ Add content successful")
        #     print(f"📄 Result preview: {result[:200]}...")
        # except Exception as e:
        #     print(f"❌ Add content failed: {e}")
        
        print("\n✅ Notion MCP Server integration tests completed!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

async def main():
    """Main test function"""
    await test_notion_tools()

if __name__ == "__main__":
    asyncio.run(main())
