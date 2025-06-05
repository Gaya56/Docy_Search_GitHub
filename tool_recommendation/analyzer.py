"""
AI-powered analyzer using Gemini API to analyze and rank tool search results.
"""
import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from dotenv import load_dotenv

from .models import (
    SearchQuery, ToolRecommendation, ToolCategory, Platform, 
    InstallationMethod, AnalysisPrompt
)

load_dotenv()


class GeminiToolAnalyzer:
    """
    AI-powered tool analyzer using Google's Gemini API.
    """
    
    def __init__(self):
        self.model = GoogleModel(model_name="gemini-1.5-flash")
        self.agent = Agent(
            self.model,
            system_prompt=self._get_system_prompt(),
            retries=2
        )
    
    def _get_system_prompt(self) -> str:
        """
        Get the system prompt for the AI analyzer.
        """
        return """You are an expert technical tool analyst specializing in cybersecurity, development, and technical tools. Your role is to analyze search results and provide accurate, detailed tool recommendations.

ANALYSIS CRITERIA:
1. RELEVANCE (0-10): How well the tool matches the user's query and needs
2. RELIABILITY (0-10): Based on maintenance status, community support, stars, updates
3. EASE OF USE (0-10): Installation complexity, documentation quality, learning curve

SCORING GUIDELINES:
- Relevance: Exact match (9-10), Close match (7-8), Partial match (5-6), Weak match (3-4), Poor match (0-2)
- Reliability: Active development & high stars (9-10), Maintained (7-8), Occasionally updated (5-6), Stale (3-4), Abandoned (0-2)
- Ease of Use: Simple install & great docs (9-10), Easy install (7-8), Moderate complexity (5-6), Complex (3-4), Very difficult (0-2)

TOOL IDENTIFICATION:
- Focus on actual tools, software, and utilities
- Prioritize open-source and well-documented tools  
- Exclude tutorials, articles, and non-tool content
- Identify installation methods and platform support

OUTPUT FORMAT:
Provide responses as valid JSON matching the ToolRecommendation schema. Include:
- Accurate tool names and descriptions
- Realistic scoring based on provided criteria
- Platform support and installation methods
- Official URLs and documentation links
- Relevant tags and metadata

Be thorough but concise. Focus on actionable, accurate information."""

    async def analyze_search_results(
        self, 
        search_results: List[Dict[str, Any]], 
        query: SearchQuery
    ) -> List[ToolRecommendation]:
        """
        Analyze search results and return ranked tool recommendations.
        """
        if not search_results:
            return []
        
        # Prepare analysis prompt
        analysis_data = {
            "query": query.dict(),
            "search_results": search_results[:15],  # Limit for context window
            "analysis_request": self._create_analysis_request(query)
        }
        
        try:
            # Get AI analysis
            prompt = self._format_analysis_prompt(analysis_data)
            result = await self.agent.run(prompt)
            
            # Parse and validate results
            recommendations = self._parse_ai_response(result.output, query)
            
            # Calculate overall scores and sort
            for rec in recommendations:
                rec.overall_score = self._calculate_overall_score(rec)
            
            # Sort by overall score (highest first)
            recommendations.sort(key=lambda x: x.overall_score, reverse=True)
            
            return recommendations[:query.max_results]
            
        except Exception as e:
            print(f"Analysis error: {e}")
            # Fallback to simple analysis
            return await self._fallback_analysis(search_results, query)
    
    def _create_analysis_request(self, query: SearchQuery) -> str:
        """
        Create a specific analysis request based on the query.
        """
        request = f"Analyze these search results for: '{query.query}'"
        
        if query.category:
            request += f"\nCategory focus: {query.category.value}"
        
        if query.platform:
            request += f"\nPlatform preference: {query.platform.value}"
        
        if query.difficulty_level:
            request += f"\nUser level: {query.difficulty_level}"
        
        request += f"\nReturn top {query.max_results} tool recommendations as JSON array."
        
        return request
    
    def _format_analysis_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """
        Format the complete analysis prompt for the AI.
        """
        return f"""
{analysis_data['analysis_request']}

SEARCH RESULTS TO ANALYZE:
{json.dumps(analysis_data['search_results'], indent=2)}

QUERY CONTEXT:
{json.dumps(analysis_data['query'], indent=2)}

Please analyze each result and identify actual tools (not articles or tutorials). For each tool found, provide a JSON object with this structure:

{{
    "name": "Tool Name",
    "description": "Clear, concise description of what the tool does",
    "category": "appropriate_category_from_enum",
    "url": "primary_tool_url",
    "github_url": "github_url_if_available",
    "documentation_url": "docs_url_if_available",
    "relevance_score": 8.5,
    "reliability_score": 7.0,
    "ease_of_use_score": 6.5,
    "overall_score": 0,
    "supported_platforms": ["linux", "windows"],
    "installation_methods": {{"linux": ["apt", "pip"], "windows": ["pip"]}},
    "installation_commands": {{"linux_apt": "sudo apt install tool-name", "pip": "pip install tool-name"}},
    "last_updated": "2024",
    "stars": 1500,
    "language": "Python",
    "license": "MIT",
    "tags": ["security", "network", "scanner"]
}}

Return ONLY a JSON array of tool recommendations. No additional text.
"""
    
    def _parse_ai_response(self, response: str, query: SearchQuery) -> List[ToolRecommendation]:
        """
        Parse AI response and convert to ToolRecommendation objects.
        """
        try:
            # Clean response (remove markdown formatting if present)
            cleaned_response = response.strip()
            if cleaned_response.startswith('```json'):
                cleaned_response = cleaned_response[7:]
            if cleaned_response.endswith('```'):
                cleaned_response = cleaned_response[:-3]
            cleaned_response = cleaned_response.strip()
            
            # Parse JSON
            recommendations_data = json.loads(cleaned_response)
            
            if not isinstance(recommendations_data, list):
                recommendations_data = [recommendations_data]
            
            recommendations = []
            for data in recommendations_data:
                try:
                    # Convert string enums to enum objects
                    if 'category' in data and isinstance(data['category'], str):
                        data['category'] = ToolCategory(data['category'])
                    
                    if 'supported_platforms' in data:
                        data['supported_platforms'] = [
                            Platform(p) if isinstance(p, str) else p 
                            for p in data['supported_platforms']
                        ]
                    
                    # Create ToolRecommendation object
                    rec = ToolRecommendation(**data)
                    recommendations.append(rec)
                    
                except Exception as e:
                    print(f"Error parsing recommendation: {e}")
                    continue
            
            return recommendations
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response was: {response[:500]}...")
            return []
        except Exception as e:
            print(f"Response parsing error: {e}")
            return []
    
    def _calculate_overall_score(self, recommendation: ToolRecommendation) -> float:
        """
        Calculate weighted overall score from individual scores.
        """
        # Weights can be adjusted based on priorities
        weights = {
            'relevance': 0.4,
            'reliability': 0.35,
            'ease_of_use': 0.25
        }
        
        overall = (
            recommendation.relevance_score * weights['relevance'] +
            recommendation.reliability_score * weights['reliability'] +
            recommendation.ease_of_use_score * weights['ease_of_use']
        )
        
        return round(overall, 2)
    
    async def _fallback_analysis(
        self, 
        search_results: List[Dict[str, Any]], 
        query: SearchQuery
    ) -> List[ToolRecommendation]:
        """
        Fallback analysis method when AI analysis fails.
        """
        recommendations = []
        
        for i, result in enumerate(search_results[:query.max_results]):
            try:
                # Basic scoring based on search result indicators
                relevance_score = self._calculate_fallback_relevance(result, query)
                reliability_score = self._calculate_fallback_reliability(result)
                ease_of_use_score = 5.0  # Default middle score
                
                rec = ToolRecommendation(
                    name=result.get('title', 'Unknown Tool'),
                    description=result.get('description', 'No description available'),
                    category=query.category or ToolCategory.GENERAL,
                    url=result.get('url', ''),
                    relevance_score=relevance_score,
                    reliability_score=reliability_score,
                    ease_of_use_score=ease_of_use_score,
                    overall_score=0,  # Will be calculated
                    supported_platforms=[Platform.LINUX],  # Default
                    installation_methods={Platform.LINUX: [InstallationMethod.SOURCE]},
                    installation_commands={},
                    tags=[]
                )
                
                rec.overall_score = self._calculate_overall_score(rec)
                recommendations.append(rec)
                
            except Exception as e:
                print(f"Fallback analysis error for result {i}: {e}")
                continue
        
        return sorted(recommendations, key=lambda x: x.overall_score, reverse=True)
    
    def _calculate_fallback_relevance(self, result: Dict[str, Any], query: SearchQuery) -> float:
        """
        Calculate relevance score for fallback analysis.
        """
        score = 5.0  # Base score
        
        title = result.get('title', '').lower()
        description = result.get('description', '').lower()
        url = result.get('url', '').lower()
        query_terms = query.query.lower().split()
        
        # Check for query terms in title and description
        for term in query_terms:
            if term in title:
                score += 1.0
            if term in description:
                score += 0.5
        
        # Bonus for GitHub repositories
        indicators = result.get('relevance_indicators', {})
        if indicators.get('is_github'):
            score += 1.0
        if indicators.get('is_tool'):
            score += 1.0
        if indicators.get('has_documentation'):
            score += 0.5
        
        return min(score, 10.0)
    
    def _calculate_fallback_reliability(self, result: Dict[str, Any]) -> float:
        """
        Calculate reliability score for fallback analysis.
        """
        score = 5.0  # Base score
        
        # GitHub specific indicators
        if 'github_stars' in result:
            stars = result.get('github_stars', 0)
            if stars > 1000:
                score += 2.0
            elif stars > 100:
                score += 1.0
            elif stars > 10:
                score += 0.5
        
        # Recent updates
        indicators = result.get('relevance_indicators', {})
        if indicators.get('is_maintained'):
            score += 1.0
        
        # Official or well-known domains
        if indicators.get('is_official_site'):
            score += 1.0
        
        return min(score, 10.0)
