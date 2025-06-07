#!/usr/bin/env python3
"""
Test script to verify modular components work together
"""
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all components can be imported successfully"""
    print("Testing imports...")
    
    try:
        # Test UI component imports
        from ui.components.sidebar import SidebarComponent
        print("✅ SidebarComponent imported successfully")
        
        from ui.components.chat import ChatComponent  
        print("✅ ChatComponent imported successfully")
        
        from ui.components.memory import MemoryComponent
        print("✅ MemoryComponent imported successfully")
        
        from ui.utils.styles import inject_all_styles
        print("✅ Styles module imported successfully")
        
        # Test that styles functions work
        from ui.utils.styles import get_main_styles, get_chat_styles, get_sidebar_styles, get_responsive_styles
        print("✅ All style functions imported successfully")
        
        # Test styles generation
        main_styles = get_main_styles()
        chat_styles = get_chat_styles() 
        sidebar_styles = get_sidebar_styles()
        responsive_styles = get_responsive_styles()
        
        assert isinstance(main_styles, str) and len(main_styles) > 100
        assert isinstance(chat_styles, str) and len(chat_styles) > 100
        assert isinstance(sidebar_styles, str) and len(sidebar_styles) > 100
        assert isinstance(responsive_styles, str) and len(responsive_styles) > 100
        print("✅ All style functions return valid CSS")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_component_instantiation():
    """Test that components can be instantiated"""
    print("\nTesting component instantiation...")
    
    try:
        from ui.components.sidebar import SidebarComponent
        from ui.components.chat import ChatComponent
        from ui.components.memory import MemoryComponent
        
        # Test SidebarComponent
        sidebar = SidebarComponent()
        print("✅ SidebarComponent instantiated successfully")
        
        # Test ChatComponent  
        def dummy_agent_getter():
            return None
        chat = ChatComponent(dummy_agent_getter)
        print("✅ ChatComponent instantiated successfully")
        
        # Test MemoryComponent
        memory = MemoryComponent()
        print("✅ MemoryComponent instantiated successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Component instantiation failed: {e}")
        return False

def test_main_ui_structure():
    """Test that main_ui.py has proper structure"""
    print("\nTesting main_ui.py structure...")
    
    try:
        import main_ui
        
        # Check that key functions exist
        assert hasattr(main_ui, 'initialize_session_state')
        assert hasattr(main_ui, 'display_sidebar') 
        assert hasattr(main_ui, 'display_configuration_banner')
        assert hasattr(main_ui, 'main')
        print("✅ All required functions exist in main_ui.py")
        
        return True
        
    except Exception as e:
        print(f"❌ main_ui.py structure test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Modular Component Structure")
    print("=" * 50)
    
    success = True
    success &= test_imports()
    success &= test_component_instantiation()
    success &= test_main_ui_structure()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Modular refactor successful!")
        print("\n📊 Summary:")
        print("- ✅ All components import correctly")
        print("- ✅ Components can be instantiated")
        print("- ✅ Styles are properly modularized")  
        print("- ✅ main_ui.py structure is correct")
        print("\n🚀 Ready to run: uv run streamlit run main_ui.py")
    else:
        print("❌ Some tests failed. Check the errors above.")
        sys.exit(1)
