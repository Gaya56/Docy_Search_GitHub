"""
Tool recommendation system with integrated MCP tools.

This package provides AI-powered tool discovery, analysis, and installation
guidance for developers, cybersecurity professionals, and CTF participants.
It includes web search, GitHub integration, Python tools, and activity tracking.
"""

from .models import (
    ToolRecommendation,
    SearchQuery,
    RecommendationResponse,
    ToolCategory,
    Platform,
    InstallationMethod,
    InstallationGuide
)

# Activity tracker is available for import by other tools
from .activity_tracker import ActivityTracker, activity_tracker

# Import MCP tools
try:
    from .perplexity_search import mcp as perplexity_mcp
    PERPLEXITY_AVAILABLE = True
except ImportError:
    PERPLEXITY_AVAILABLE = False
    perplexity_mcp = None

try:
    from .sql_tools import mcp as sql_mcp
    SQL_TOOLS_AVAILABLE = True
except ImportError:
    SQL_TOOLS_AVAILABLE = False
    sql_mcp = None

try:
    from .code_analyzer import mcp as code_analyzer_mcp
    CODE_ANALYZER_AVAILABLE = True
except ImportError:
    CODE_ANALYZER_AVAILABLE = False
    code_analyzer_mcp = None

try:
    from .brave_search import mcp as brave_mcp
    BRAVE_SEARCH_AVAILABLE = True
except ImportError:
    BRAVE_SEARCH_AVAILABLE = False
    brave_mcp = None

__version__ = "1.0.0"
__author__ = "AI Tool Recommendation System"

__all__ = [
    # Data models
    "ToolRecommendation",
    "SearchQuery",
    "RecommendationResponse",
    "ToolCategory",
    "Platform",
    "InstallationMethod",
    "InstallationGuide",
    # Activity tracking
    "ActivityTracker",
    "activity_tracker",
    # MCP tools
    "perplexity_mcp",
    "sql_mcp",
    "code_analyzer_mcp",
    "brave_mcp",
    # Availability flags
    "PERPLEXITY_AVAILABLE",
    "SQL_TOOLS_AVAILABLE",
    "CODE_ANALYZER_AVAILABLE",
    "BRAVE_SEARCH_AVAILABLE"
]
