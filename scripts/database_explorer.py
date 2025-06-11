#!/usr/bin/env python3
"""
Entry point for database explorer - calls the moved explorer module
"""

import sys
from pathlib import Path

# Add the project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

if __name__ == "__main__":
    # Import and run the database explorer
    from docy_search.database.explorer import main
    sys.exit(main())
