#!/usr/bin/env python3
"""Test the MCP servers to see if they can run properly"""

def test_mcp_imports():
    """Test importing MCP server modules"""
    print("🧪 Testing MCP Server Imports...")
    print("=" * 50)
    
    modules_to_test = [
        "docy_search.tool_recommendation.brave_search",
        "docy_search.tool_recommendation.python_tools", 
        "docy_search.tool_recommendation.mcp_server",
        "docy_search.tool_recommendation.github_mcp_server"
    ]
    
    results = {}
    
    for module_name in modules_to_test:
        try:
            __import__(module_name)
            results[module_name] = "✅ SUCCESS"
            print(f"✅ {module_name}")
        except Exception as e:
            results[module_name] = f"❌ ERROR: {e}"
            print(f"❌ {module_name}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    for module, result in results.items():
        print(f"{module}: {result}")
    
    # Count successes
    successes = sum(1 for r in results.values() if "SUCCESS" in r)
    total = len(results)
    print(f"\n🎯 {successes}/{total} modules imported successfully")
    
    return successes == total

if __name__ == "__main__":
    success = test_mcp_imports()
    exit(0 if success else 1)
