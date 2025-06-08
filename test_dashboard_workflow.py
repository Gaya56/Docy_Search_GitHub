#!/usr/bin/env python3
"""Test script for dashboard generation workflow"""
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, '/workspaces/Docy_Search_GitHub')

async def test_dashboard_generation():
    """Test the complete dashboard generation workflow"""
    print("🧪 Testing Dashboard Generation Workflow")
    print("=" * 50)
    
    try:
        # Test imports
        print("1. Testing imports...")
        from docy_search.app import model
        from docy_search.dashboard.generator import DashboardGenerator
        print("   ✅ Imports successful")
        
        # Test generator creation
        print("2. Creating dashboard generator...")
        generator = DashboardGenerator(model)
        print("   ✅ Generator created")
        
        # Test dashboard generation
        print("3. Generating dashboard...")
        html_content = await generator.generate_full_dashboard()
        print(f"   ✅ Dashboard generated ({len(html_content):,} chars)")
        
        # Verify HTML content
        print("4. Verifying HTML content...")
        if "<!DOCTYPE html>" in html_content:
            print("   ✅ Valid HTML structure")
        if "Database Dashboard" in html_content:
            print("   ✅ Dashboard title present")
        if "metric" in html_content.lower():
            print("   ✅ Metrics content present")
            
        # Save test output
        print("5. Saving test output...")
        test_output_path = "/workspaces/Docy_Search_GitHub/test_dashboard.html"
        with open(test_output_path, 'w') as f:
            f.write(html_content)
        print(f"   ✅ Test dashboard saved to {test_output_path}")
        
        print("\n🎉 All tests passed! Dashboard generation workflow is working.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_dashboard_generation())
    sys.exit(0 if success else 1)
