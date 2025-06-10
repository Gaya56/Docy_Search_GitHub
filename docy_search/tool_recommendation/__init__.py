"""
Modular, intelligent tool recommendation system.

This package provides AI-powered tool discovery, analysis, and installation
guidance for developers, cybersecurity professionals, and CTF participants.
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

from .search_engine import BraveSearchEngine, SearchResultEnhancer
from .analyzer import GeminiToolAnalyzer
from .installer import InstallationGuideGenerator
from .core import ToolRecommendationSystem

__version__ = "1.0.0"
__author__ = "AI Tool Recommendation System"

__all__ = [
    # Models
    "ToolRecommendation",
    "SearchQuery", 
    "RecommendationResponse",
    "ToolCategory",
    "Platform",
    "InstallationMethod",
    "InstallationGuide",
    
    # Core components
    "BraveSearchEngine",
    "SearchResultEnhancer", 
    "GeminiToolAnalyzer",
    "InstallationGuideGenerator",
    "ToolRecommendationSystem"
]
