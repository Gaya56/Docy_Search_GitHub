#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

try:
    print("Testing Notion function access...")
    from tool_recommendation.notion_mcp_server import read_notion_page, search_notion_page, add_to_notion_page
    
    # Access the underlying functions
    read_fn = read_notion_page.fn
    search_fn = search_notion_page.fn
    add_fn = add_to_notion_page.fn
    
    print(f"read_fn: {read_fn}")
    print(f"search_fn: {search_fn}")
    print(f"add_fn: {add_fn}")
    
    print(f"read_fn callable: {callable(read_fn)}")
    print(f"search_fn callable: {callable(search_fn)}")
    print(f"add_fn callable: {callable(add_fn)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
