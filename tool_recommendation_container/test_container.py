#!/usr/bin/env python3
"""
Simple test script for the Tool Recommendation Container
"""

import sys
import time
from client import ToolRecommendationClient

def test_container():
    """Test the container functionality."""
    print("🧪 Testing Tool Recommendation Container...")
    
    # Initialize client
    client = ToolRecommendationClient("http://localhost:8000")
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(30):
        if client.health_check():
            print("✅ Server is healthy!")
            break
        time.sleep(1)
        print(f"   Waiting... ({i+1}/30)")
    else:
        print("❌ Server failed to start")
        return False
    
    # Test basic functionality
    print("\n🔍 Testing tool search...")
    result = client.search_tools("python web framework")
    if result and "error" not in result.lower():
        print("✅ Tool search works!")
        print(f"   Result preview: {result[:100]}...")
    else:
        print(f"❌ Tool search failed: {result}")
        return False
    
    # Test web search
    print("\n🌐 Testing web search...")
    result = client.search_web("streamlit tutorial")
    if result and "error" not in result.lower():
        print("✅ Web search works!")
        print(f"   Result preview: {result[:100]}...")
    else:
        print(f"❌ Web search failed: {result}")
    
    # Test GitHub search
    print("\n🐙 Testing GitHub search...")
    result = client.search_github("streamlit components")
    if result and "error" not in result.lower():
        print("✅ GitHub search works!")
        print(f"   Result preview: {result[:100]}...")
    else:
        print(f"❌ GitHub search failed: {result}")
    
    # Test Python execution
    print("\n🐍 Testing Python execution...")
    result = client.execute_python("print('Hello from container!')")
    if result and "Hello from container!" in result:
        print("✅ Python execution works!")
        print(f"   Result: {result.strip()}")
    else:
        print(f"❌ Python execution failed: {result}")
    
    print("\n🎉 Container test completed!")
    return True

if __name__ == "__main__":
    success = test_container()
    sys.exit(0 if success else 1)
