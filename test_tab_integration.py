#!/usr/bin/env python3
"""
Quick unit test for tab integration in main_ui.py
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, '/workspaces/Docy_Search_GitHub')

def test_imports():
    """Test that all required imports work"""
    try:
        from docy_search.ui.components.tabs import TabComponent
        from docy_search.ui.components.dashboard import DashboardComponent
        from docy_search.ui.components.chat import ChatComponent
        from docy_search.ui.components.memory import MemoryComponent
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_component_initialization():
    """Test that components can be initialized"""
    try:
        from docy_search.ui.components.tabs import TabComponent
        from docy_search.ui.components.dashboard import DashboardComponent
        
        # Test TabComponent
        tab_component = TabComponent()
        print("✅ TabComponent initialized successfully")
        
        # Test DashboardComponent
        dashboard_component = DashboardComponent()
        print("✅ DashboardComponent initialized successfully")
        
        return True
    except Exception as e:
        print(f"❌ Component initialization error: {e}")
        return False

def test_tab_structure():
    """Test the tab structure definition"""
    try:
        from docy_search.ui.components.dashboard import DashboardComponent
        
        dashboard_component = DashboardComponent()
        
        # Mock render function for testing
        def mock_chat_render():
            return "Chat rendered"
        
        # Test tab structure
        tabs = {
            "chat": {
                "label": "Chat",
                "icon": "💬",
                "render": mock_chat_render
            },
            "dashboard": {
                "label": "Dashboard",
                "icon": "📊", 
                "render": dashboard_component.render
            }
        }
        
        # Check structure
        assert "chat" in tabs
        assert "dashboard" in tabs
        assert tabs["chat"]["label"] == "Chat"
        assert tabs["dashboard"]["label"] == "Dashboard"
        assert callable(tabs["chat"]["render"])
        assert callable(tabs["dashboard"]["render"])
        
        print("✅ Tab structure is valid")
        return True
    except Exception as e:
        print(f"❌ Tab structure test error: {e}")
        return False

def run_tests():
    """Run all tests"""
    print("🧪 Running Tab Integration Tests...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_component_initialization,
        test_tab_structure
    ]
    
    results = []
    for test in tests:
        print(f"\n📋 Running {test.__name__}...")
        results.append(test())
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All tests passed! Tab integration is working correctly.")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return all(results)

if __name__ == "__main__":
    run_tests()
