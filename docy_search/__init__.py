"""
Docy Search - Intelligent Tool Recommendation System
"""

__version__ = "2.0.0"
__author__ = "Docy Search Team"

# Package-level imports for convenience
from .app import create_agent_with_context, load_project_context
from .memory.memory_manager import MemoryManager

__all__ = [
    "create_agent_with_context",
    "load_project_context", 
    "MemoryManager",
]