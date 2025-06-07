"""
Data models for the tool recommendation system using Pydantic.
"""
from pydantic import BaseModel, field_validator
from typing import List, Optional, Dict, Any
from enum import Enum


class ToolCategory(str, Enum):
    """Categories of tools that can be recommended."""
    CYBERSECURITY = "cybersecurity"
    DEVELOPMENT = "development"
    NETWORKING = "networking"
    FORENSICS = "forensics"
    REVERSE_ENGINEERING = "reverse_engineering"
    WEB_SECURITY = "web_security"
    MOBILE_SECURITY = "mobile_security"
    CLOUD_SECURITY = "cloud_security"
    CTF = "ctf"
    OSINT = "osint"
    GENERAL = "general"


class Platform(str, Enum):
    """Supported platforms for tool installation."""
    LINUX = "linux"
    WINDOWS = "windows" 
    MACOS = "macos"
    DOCKER = "docker"
    PYTHON = "python"
    WEB = "web"
    CROSS_PLATFORM = "cross_platform"


class InstallationMethod(str, Enum):
    """Different ways a tool can be installed."""
    APT = "apt"
    YUM = "yum"
    BREW = "brew"
    PIP = "pip"
    NPM = "npm"
    DOCKER = "docker"
    SNAP = "snap"
    FLATPAK = "flatpak"
    BINARY = "binary"
    SOURCE = "source"
    WEB = "web"
    PACKAGE_MANAGER = "package_manager"


class ToolRecommendation(BaseModel):
    """A single tool recommendation with all relevant information."""
    name: str
    description: str
    category: ToolCategory
    url: str
    github_url: Optional[str] = None
    documentation_url: Optional[str] = None
    
    # Scoring metrics
    relevance_score: float  # 0-10 based on query match
    reliability_score: float  # 0-10 based on maintenance, stars, etc.
    ease_of_use_score: float  # 0-10 based on installation and usage complexity
    overall_score: float  # Weighted combination of above scores
    
    # Installation information
    supported_platforms: List[Platform]
    installation_methods: Dict[Platform, List[InstallationMethod]]
    installation_commands: Dict[str, str]  # platform/method -> command
    
    # Additional metadata
    last_updated: Optional[str] = None
    stars: Optional[int] = None
    language: Optional[str] = None
    license: Optional[str] = None
    tags: List[str] = []
    
    @field_validator('relevance_score', 'reliability_score', 'ease_of_use_score', 'overall_score')
    @classmethod
    def validate_scores(cls, v):
        if not 0 <= v <= 10:
            raise ValueError('Score must be between 0 and 10')
        return v


class SearchQuery(BaseModel):
    """Represents a user's search query for tool recommendations."""
    query: str
    category: Optional[ToolCategory] = None
    platform: Optional[Platform] = None
    max_results: int = 10
    include_beta: bool = False
    difficulty_level: Optional[str] = None  # "beginner", "intermediate", "advanced"
    
    @field_validator('max_results')
    @classmethod
    def validate_max_results(cls, v):
        if not 1 <= v <= 50:
            raise ValueError('max_results must be between 1 and 50')
        return v


class RecommendationResponse(BaseModel):
    """Complete response containing tool recommendations and metadata."""
    query: SearchQuery
    recommendations: List[ToolRecommendation]
    search_metadata: Dict[str, Any]
    processing_time: float
    total_found: int
    
    class Config:
        json_encoders = {
            ToolCategory: lambda v: v.value,
            Platform: lambda v: v.value,
            InstallationMethod: lambda v: v.value
        }


class AnalysisPrompt(BaseModel):
    """Structured prompt for AI analysis of search results."""
    search_results: List[Dict[str, Any]]
    query: SearchQuery
    context: Optional[str] = None


class InstallationGuide(BaseModel):
    """Detailed installation guide for a specific tool."""
    tool_name: str
    platform: Platform
    method: InstallationMethod
    steps: List[str]
    prerequisites: List[str] = []
    post_install_notes: List[str] = []
    troubleshooting: Dict[str, str] = {}
    verification_command: Optional[str] = None
