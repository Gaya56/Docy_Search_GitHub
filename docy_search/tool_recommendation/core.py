"""
Core tool recommendation system that orchestrates all components.
"""
import asyncio
import time
from typing import List, Optional, Dict, Any

from .models import (
    SearchQuery, RecommendationResponse, ToolRecommendation,
    Platform, InstallationGuide
)
from .search_engine import BraveSearchEngine, SearchResultEnhancer
from .analyzer import GeminiToolAnalyzer
from .installer import InstallationGuideGenerator


class ToolRecommendationSystem:
    """
    Main system class that orchestrates tool discovery, analysis, and recommendations.
    """
    
    def __init__(self):
        self.search_engine = BraveSearchEngine()
        self.analyzer = GeminiToolAnalyzer()
        self.installer = InstallationGuideGenerator()
    
    async def get_recommendations(self, query: SearchQuery) -> RecommendationResponse:
        """
        Get tool recommendations based on a search query.
        
        Args:
            query: SearchQuery object containing search parameters
            
        Returns:
            RecommendationResponse with ranked tool recommendations
        """
        start_time = time.time()
        
        try:
            # Step 1: Search for tools using Brave API
            async with self.search_engine as search:
                search_results = await search.search_tools(query)
            
            if not search_results:
                return RecommendationResponse(
                    query=query,
                    recommendations=[],
                    search_metadata={"status": "no_results"},
                    processing_time=time.time() - start_time,
                    total_found=0
                )
            
            # Step 2: Enhance search results with additional metadata
            enhanced_results = await SearchResultEnhancer.enhance_github_results(search_results)
            
            # Step 3: Analyze results with AI and get recommendations
            recommendations = await self.analyzer.analyze_search_results(
                enhanced_results, query
            )
            
            # Step 4: Enrich recommendations with installation info
            for rec in recommendations:
                self._enrich_installation_info(rec)
            
            processing_time = time.time() - start_time
            
            return RecommendationResponse(
                query=query,
                recommendations=recommendations,
                search_metadata={
                    "status": "success",
                    "raw_results_count": len(search_results),
                    "enhanced_results_count": len(enhanced_results),
                    "final_recommendations": len(recommendations)
                },
                processing_time=processing_time,
                total_found=len(search_results)
            )
            
        except Exception as e:
            return RecommendationResponse(
                query=query,
                recommendations=[],
                search_metadata={
                    "status": "error",
                    "error": str(e)
                },
                processing_time=time.time() - start_time,
                total_found=0
            )
    
    def get_installation_guide(
        self, 
        tool: ToolRecommendation, 
        platform: Platform,
        method: Optional[str] = None
    ) -> InstallationGuide:
        """
        Get detailed installation guide for a specific tool and platform.
        
        Args:
            tool: ToolRecommendation object
            platform: Target platform
            method: Optional installation method
            
        Returns:
            InstallationGuide with step-by-step instructions
        """
        return self.installer.generate_guide(tool, platform, method)
    
    def _enrich_installation_info(self, recommendation: ToolRecommendation):
        """
        Enrich recommendation with better installation information.
        """
        # If no installation methods specified, infer from tool properties
        if not recommendation.installation_methods:
            recommendation.installation_methods = self._infer_installation_methods(recommendation)
        
        # If no installation commands specified, generate basic ones
        if not recommendation.installation_commands:
            recommendation.installation_commands = self._generate_basic_commands(recommendation)
    
    def _infer_installation_methods(self, tool: ToolRecommendation) -> Dict[Platform, List[str]]:
        """
        Infer likely installation methods based on tool properties.
        """
        methods = {}
        
        # GitHub tools likely support source installation
        if tool.github_url:
            methods[Platform.LINUX] = ["source", "binary"]
            methods[Platform.MACOS] = ["source", "binary"]
            methods[Platform.WINDOWS] = ["binary", "source"]
        
        # Python tools support pip
        if tool.language and "python" in tool.language.lower():
            for platform in [Platform.LINUX, Platform.MACOS, Platform.WINDOWS]:
                if platform not in methods:
                    methods[platform] = []
                methods[platform].append("pip")
        
        # Security tools often available in Linux repos
        if tool.category.value in ["cybersecurity", "networking", "forensics"]:
            if Platform.LINUX not in methods:
                methods[Platform.LINUX] = []
            methods[Platform.LINUX].extend(["apt", "snap"])
        
        # Default fallbacks
        if not methods:
            methods = {
                Platform.LINUX: ["apt", "source"],
                Platform.MACOS: ["brew", "source"],
                Platform.WINDOWS: ["binary"]
            }
        
        return methods
    
    def _generate_basic_commands(self, tool: ToolRecommendation) -> Dict[str, str]:
        """
        Generate basic installation commands for a tool.
        """
        commands = {}
        tool_name = tool.name.lower().replace(" ", "-")
        
        # Linux commands
        commands["linux_apt"] = f"sudo apt update && sudo apt install -y {tool_name}"
        commands["linux_snap"] = f"sudo snap install {tool_name}"
        
        # macOS commands
        commands["macos_brew"] = f"brew install {tool_name}"
        
        # Python commands
        if tool.language and "python" in tool.language.lower():
            commands["pip"] = f"pip install {tool_name}"
        
        # Docker commands
        commands["docker"] = f"docker pull {tool_name} && docker run -it {tool_name}"
        
        # Source installation
        if tool.github_url:
            commands["source"] = f"git clone {tool.github_url} && cd {tool_name} && make install"
        
        return commands


class RecommendationFormatter:
    """
    Formats recommendations for different output formats.
    """
    
    @staticmethod
    def format_as_markdown(response: RecommendationResponse) -> str:
        """
        Format recommendations as Markdown text.
        """
        if not response.recommendations:
            return f"# No Tools Found\n\nNo tools found for query: '{response.query.query}'"
        
        markdown = f"# Tool Recommendations\n\n"
        markdown += f"**Query:** {response.query.query}\n"
        markdown += f"**Found:** {len(response.recommendations)} tools\n"
        markdown += f"**Processing Time:** {response.processing_time:.2f}s\n\n"
        
        for i, tool in enumerate(response.recommendations, 1):
            markdown += f"## {i}. {tool.name}\n\n"
            markdown += f"**Description:** {tool.description}\n\n"
            markdown += f"**Category:** {tool.category.value}\n"
            markdown += f"**Overall Score:** {tool.overall_score}/10\n"
            markdown += f"- Relevance: {tool.relevance_score}/10\n"
            markdown += f"- Reliability: {tool.reliability_score}/10\n"
            markdown += f"- Ease of Use: {tool.ease_of_use_score}/10\n\n"
            
            if tool.url:
                markdown += f"**Website:** [{tool.url}]({tool.url})\n"
            if tool.github_url:
                markdown += f"**GitHub:** [{tool.github_url}]({tool.github_url})\n"
            if tool.documentation_url:
                markdown += f"**Documentation:** [{tool.documentation_url}]({tool.documentation_url})\n"
            
            markdown += f"**Supported Platforms:** {', '.join([p.value for p in tool.supported_platforms])}\n"
            
            if tool.tags:
                markdown += f"**Tags:** {', '.join(tool.tags)}\n"
            
            markdown += "\n---\n\n"
        
        return markdown
    
    @staticmethod
    def format_installation_guide(guide: InstallationGuide) -> str:
        """
        Format installation guide as Markdown.
        """
        markdown = f"# Installation Guide: {guide.tool_name}\n\n"
        markdown += f"**Platform:** {guide.platform.value}\n"
        markdown += f"**Method:** {guide.method.value}\n\n"
        
        if guide.prerequisites:
            markdown += "## Prerequisites\n\n"
            for prereq in guide.prerequisites:
                markdown += f"- {prereq}\n"
            markdown += "\n"
        
        markdown += "## Installation Steps\n\n"
        for i, step in enumerate(guide.steps, 1):
            if step.startswith(('sudo', 'apt', 'brew', 'pip', 'docker', 'git')):
                markdown += f"{i}. Run: `{step}`\n"
            else:
                markdown += f"{i}. {step}\n"
        
        if guide.verification_command:
            markdown += f"\n## Verification\n\nVerify installation: `{guide.verification_command}`\n"
        
        if guide.post_install_notes:
            markdown += "\n## Notes\n\n"
            for note in guide.post_install_notes:
                markdown += f"- {note}\n"
        
        if guide.troubleshooting:
            markdown += "\n## Troubleshooting\n\n"
            for problem, solution in guide.troubleshooting.items():
                markdown += f"**{problem}:** {solution}\n\n"
        
        return markdown
