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
    "activity_tracker"
]
