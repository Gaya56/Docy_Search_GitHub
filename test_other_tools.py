#!/usr/bin/env python3

import sys
sys.path.insert(0, '.')

try:
    print("Testing other tool imports...")
    from tool_recommendation.brave_search import search_web
    
    print(f"search_web: {search_web}")
    print(f"search_web callable: {callable(search_web)}")
    
    if hasattr(search_web, 'fn'):
        print(f"search_web.fn: {search_web.fn}")
        print(f"search_web.fn callable: {callable(search_web.fn)}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
