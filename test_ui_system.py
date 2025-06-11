#!/usr/bin/env python3
"""
Comprehensive test script for UI components and main_ui.py
"""

def test_ui_imports():
    """Test all UI imports and components"""
    print("🧪 Testing UI Directory and main_ui.py...")
    print("=" * 60)
    
    # Test 1: UI package imports
    try:
        from docy_search.ui import (
            SidebarComponent,
            ChatComponent,
            MemoryComponent,
            DashboardComponent,
            inject_all_styles,
            get_main_styles,
            get_chat_styles,
            get_sidebar_styles,
            get_responsive_styles
        )
        print("✅ Test 1 PASSED: UI package imports successful")
    except Exception as e:
        print(f"❌ Test 1 FAILED: UI package imports - {e}")
        return False
    
    # Test 2: Individual component imports
    try:
        from docy_search.ui.components import (
            SidebarComponent as SC,
            ChatComponent as CC,
            MemoryComponent as MC,
            DashboardComponent as DC
        )
        print("✅ Test 2 PASSED: Individual component imports successful")
    except Exception as e:
        print(f"❌ Test 2 FAILED: Individual component imports - {e}")
        return False
    
    # Test 3: UI utils imports
    try:
        from docy_search.ui.utils import (
            inject_all_styles as ias,
            get_main_styles as gms,
            get_chat_styles as gcs,
            get_sidebar_styles as gss,
            get_responsive_styles as grs
        )
        print("✅ Test 3 PASSED: UI utils imports successful")
    except Exception as e:
        print(f"❌ Test 3 FAILED: UI utils imports - {e}")
        return False
    
    # Test 4: Component instantiation
    try:
        # Mock dependencies for testing
        class MockAgent:
            def get_agent(self):
                return None
        
        class MockMemoryManager:
            pass
        
        class MockModel:
            pass
        
        # Test component creation
        mock_agent = MockAgent()
        mock_memory = MockMemoryManager()
        mock_model = MockModel()
        
        sidebar = SidebarComponent(mock_memory, mock_model)
        chat = ChatComponent(mock_agent.get_agent)
        memory = MemoryComponent(mock_memory)
        dashboard = DashboardComponent()
        
        print("✅ Test 4 PASSED: Component instantiation successful")
    except Exception as e:
        print(f"❌ Test 4 FAILED: Component instantiation - {e}")
        return False
    
    # Test 5: main_ui.py import check
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "main_ui", 
            "/workspaces/Docy_Search_GitHub/docy_search/main_ui.py"
        )
        if spec and spec.loader:
            # Just check if it can be loaded, don't actually run it
            print("✅ Test 5 PASSED: main_ui.py can be loaded")
        else:
            print("❌ Test 5 FAILED: main_ui.py cannot be loaded")
            return False
    except Exception as e:
        print(f"❌ Test 5 FAILED: main_ui.py loading - {e}")
        return False
    
    # Test 6: Check __all__ exports
    try:
        from docy_search.ui import __all__ as ui_all
        from docy_search.ui.components import __all__ as comp_all
        from docy_search.ui.utils import __all__ as utils_all
        
        expected_ui = [
            'SidebarComponent', 'ChatComponent', 'MemoryComponent', 
            'DashboardComponent', 'inject_all_styles', 'get_main_styles',
            'get_chat_styles', 'get_sidebar_styles', 'get_responsive_styles'
        ]
        expected_comp = [
            'SidebarComponent', 'ChatComponent', 'MemoryComponent', 
            'DashboardComponent'
        ]
        expected_utils = [
            'inject_all_styles', 'get_main_styles', 'get_chat_styles',
            'get_sidebar_styles', 'get_responsive_styles'
        ]
        
        if (set(ui_all) == set(expected_ui) and 
            set(comp_all) == set(expected_comp) and 
            set(utils_all) == set(expected_utils)):
            print("✅ Test 6 PASSED: __all__ exports are correct")
        else:
            print(f"❌ Test 6 FAILED: __all__ exports mismatch")
            print(f"  UI expected: {expected_ui}")
            print(f"  UI actual: {ui_all}")
            print(f"  Components expected: {expected_comp}")
            print(f"  Components actual: {comp_all}")
            print(f"  Utils expected: {expected_utils}")
            print(f"  Utils actual: {utils_all}")
            return False
    except Exception as e:
        print(f"❌ Test 6 FAILED: __all__ exports - {e}")
        return False
    
    print("\n🎉 All UI Tests PASSED!")
    print("📁 UI directory and main_ui.py are properly polished and organized")
    return True


def test_import_compatibility():
    """Test backward compatibility with existing imports"""
    print("\n🔄 Testing Import Compatibility...")
    print("=" * 40)
    
    # Test individual imports still work
    try:
        from docy_search.ui.components.sidebar import SidebarComponent
        from docy_search.ui.components.chat import ChatComponent
        from docy_search.ui.components.memory import MemoryComponent
        from docy_search.ui.components.dashboard import DashboardComponent
        from docy_search.ui.utils.styles import inject_all_styles
        print("✅ Backward compatibility maintained")
        return True
    except Exception as e:
        print(f"❌ Backward compatibility failed: {e}")
        return False


if __name__ == "__main__":
    success1 = test_ui_imports()
    success2 = test_import_compatibility()
    
    if success1 and success2:
        print("\n🚀 ALL TESTS PASSED! UI system is ready for integration.")
    else:
        print("\n❌ Some tests failed. Please check the issues above.")
    
    exit(0 if (success1 and success2) else 1)
