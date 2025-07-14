#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

try:
    print("Testing Notion imports...")
    from tool_recommendation.notion_mcp_server import read_notion_page, search_notion_page, add_to_notion_page
    print("✅ Notion tools imported successfully")
    print(f"read_notion_page: {read_notion_page}")
    print(f"search_notion_page: {search_notion_page}")
    print(f"add_to_notion_page: {add_to_notion_page}")
    
    # Check if they're callable
    print(f"read_notion_page callable: {callable(read_notion_page)}")
    print(f"search_notion_page callable: {callable(search_notion_page)}")
    print(f"add_to_notion_page callable: {callable(add_to_notion_page)}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
except Exception as e:
    print(f"❌ General error: {e}")
    import traceback
    traceback.print_exc()
