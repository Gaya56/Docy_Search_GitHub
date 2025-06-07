#!/usr/bin/env python3
"""
Reorganize project structure for proper packaging.
Run this script to move files into the docy_search package.
"""

import os
import shutil
from pathlib import Path

def reorganize_project():
    """Move files into proper package structure."""
    
    # Define file moves (source -> destination)
    moves = {
        # Core application files
        'app.py': 'docy_search/app.py',
        'main_ui.py': 'docy_search/main_ui.py',
        'activity_tracker.py': 'docy_search/activity_tracker.py',
        'brave_search.py': 'docy_search/brave_search.py',
        'github_mcp_server.py': 'docy_search/github_mcp_server.py',
        'python_tools.py': 'docy_search/python_tools.py',
        
        # Memory system (keep structure)
        'memory': 'docy_search/memory',
        
        # Tool recommendation (keep structure)
        'tool_recommendation': 'docy_search/tool_recommendation',
        
        # UI components (keep structure)
        'ui': 'docy_search/ui',
    }
    
    # Create docy_search directory if it doesn't exist
    Path('docy_search').mkdir(exist_ok=True)
    
    # Perform moves
    for src, dst in moves.items():
        if os.path.exists(src):
            print(f"Moving {src} -> {dst}")
            try:
                if os.path.isdir(src):
                    # For directories, use copytree then remove
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    shutil.rmtree(src)
                else:
                    # For files
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.move(src, dst)
                print(f"  ✓ Moved successfully")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        else:
            print(f"Skipping {src} (not found)")
    
    print("\n✅ Reorganization complete!")
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Update imports in all files (see update_imports.py)")
    print("3. Run: pip install -e .")
    print("4. Test the installation")

if __name__ == "__main__":
    print("🔧 Reorganizing project structure...")
    reorganize_project()