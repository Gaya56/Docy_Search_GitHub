#!/usr/bin/env python3
"""
Update imports throughout the codebase after reorganization.
"""

import os
import re
from pathlib import Path

# Import replacements
REPLACEMENTS = [
    # Memory imports
    (r'from memory\.', 'from docy_search.memory.'),
    (r'import memory\.', 'import docy_search.memory.'),
    
    # UI imports
    (r'from ui\.', 'from docy_search.ui.'),
    (r'import ui\.', 'import docy_search.ui.'),
    
    # Tool recommendation imports
    (r'from tool_recommendation\.', 'from docy_search.tool_recommendation.'),
    (r'import tool_recommendation\.', 'import docy_search.tool_recommendation.'),
    
    # Direct file imports (from other files in root)
    (r'from activity_tracker import', 'from docy_search.activity_tracker import'),
    (r'from brave_search import', 'from docy_search.brave_search import'),
    (r'from github_mcp_server import', 'from docy_search.github_mcp_server import'),
    (r'from python_tools import', 'from docy_search.python_tools import'),
    (r'from app import', 'from docy_search.app import'),
    (r'from main_ui import', 'from docy_search.main_ui import'),
    
    # Config imports
    (r'from config\.settings import', 'from config.settings import'),  # Keep as is
    
    # Remove sys.path manipulations
    (r'sys\.path\.append\([^)]+\)\s*\n', ''),
    (r'sys\.path\.insert\([^)]+\)\s*\n', ''),
]

def update_file(filepath):
    """Update imports in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Apply replacements
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    
    # Write back if changed
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def update_all_imports():
    """Update imports in all Python files."""
    updated = 0
    
    # Files to update
    patterns = [
        'docy_search/**/*.py',
        'config/**/*.py',
        'tests/**/*.py',
        '*.py'
    ]
    
    for pattern in patterns:
        for filepath in Path('.').glob(pattern):
            if filepath.name == 'update_imports.py':
                continue
            
            print(f"Checking {filepath}...")
            if update_file(filepath):
                print(f"  ✓ Updated imports")
                updated += 1
            else:
                print(f"  - No changes needed")
    
    print(f"\n✅ Updated {updated} files")
    print("\nNext steps:")
    print("1. Review the changes with: git diff")
    print("2. Run: pip install -e .")
    print("3. Test with: python -m docy_search.app")

if __name__ == "__main__":
    print("🔧 Updating imports throughout codebase...")
    update_all_imports()