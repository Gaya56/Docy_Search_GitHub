"""
Enhanced search engine using Brave API for tool discovery.
"""
import os
import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
from .models import SearchQuery, ToolCategory

load_dotenv()


class BraveSearchEngine:
    """Enhanced Brave Search API client for tool discovery."""
    
    def __init__(self):
        self.api_key = os.getenv("BRAVE_API_KEY", "")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.session = None
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def search_tools(self, query: SearchQuery) -> List[Dict[str, Any]]:
        """
        Search for tools based on the query with enhanced search terms.
        """
        if not self.api_key:
            raise ValueError("BRAVE_API_KEY environment variable is required")
            
        # Enhance search query based on category and context
        enhanced_query = self._enhance_search_query(query)
        
        # Perform multiple targeted searches
        search_tasks = []
        for search_term in enhanced_query:
            search_tasks.append(self._perform_search(search_term, query.max_results // len(enhanced_query) + 2))
        
        results = await asyncio.gather(*search_tasks, return_exceptions=True)
        
        # Combine and deduplicate results
        all_results = []
        seen_urls = set()
        
        for result_set in results:
            if isinstance(result_set, Exception):
                continue
            for result in result_set:
                if result.get('url') not in seen_urls:
                    seen_urls.add(result.get('url'))
                    all_results.append(result)
        
        return all_results[:query.max_results * 2]  # Return extra for filtering
    
    def _enhance_search_query(self, query: SearchQuery) -> List[str]:
        """
        Generate multiple enhanced search queries based on the original query and category.
        """
        base_terms = [query.query]
        
        # Add category-specific terms
        category_terms = {
            ToolCategory.CYBERSECURITY: ["security tool", "cybersecurity", "infosec"],
            ToolCategory.DEVELOPMENT: ["development tool", "programmer", "coding"],
            ToolCategory.NETWORKING: ["network tool", "networking", "nettools"],
            ToolCategory.FORENSICS: ["forensics tool", "digital forensics", "investigation"],
            ToolCategory.REVERSE_ENGINEERING: ["reverse engineering", "disassembler", "decompiler"],
            ToolCategory.WEB_SECURITY: ["web security", "webapp security", "web pentest"],
            ToolCategory.MOBILE_SECURITY: ["mobile security", "android security", "ios security"],
            ToolCategory.CLOUD_SECURITY: ["cloud security", "aws security", "azure security"],
            ToolCategory.CTF: ["ctf tool", "capture the flag", "hacking challenge"],
            ToolCategory.OSINT: ["osint tool", "open source intelligence", "reconnaissance"]
        }
        
        enhanced_queries = []
        
        # Base query variations
        for base in base_terms:
            enhanced_queries.append(f"{base} github")
            enhanced_queries.append(f"{base} open source")
            enhanced_queries.append(f"{base} tool download")
            
            if query.category:
                category_specific = category_terms.get(query.category, [])
                for cat_term in category_specific[:2]:  # Limit to avoid too many queries
                    enhanced_queries.append(f"{base} {cat_term}")
        
        # Platform-specific searches
        if query.platform:
            platform_term = query.platform.value
            enhanced_queries.append(f"{query.query} {platform_term}")
        
        return enhanced_queries[:4]  # Limit to 4 searches to avoid rate limits
    
    async def _perform_search(self, search_term: str, count: int) -> List[Dict[str, Any]]:
        """
        Perform a single search request to Brave API.
        """
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": self.api_key
        }
        
        params = {
            "q": search_term,
            "count": count,
            "summary": 1,
            "freshness": "py",  # past year for recent tools
            "search_lang": "en",
            "country": "US",
            "safe_search": "moderate"
        }
        
        try:
            async with self.session.get(self.base_url, headers=headers, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                
                web_results = data.get("web", {}).get("results", [])
                
                # Filter and enhance results
                filtered_results = []
                for result in web_results:
                    # Skip certain domains that are less likely to contain tools
                    url = result.get("url", "").lower()
                    if any(domain in url for domain in ["stackoverflow.com", "reddit.com", "quora.com"]):
                        continue
                        
                    # Enhance result with additional metadata
                    enhanced_result = {
                        **result,
                        "search_term": search_term,
                        "relevance_indicators": self._extract_relevance_indicators(result)
                    }
                    filtered_results.append(enhanced_result)
                
                return filtered_results
                
        except Exception as e:
            print(f"Search error for '{search_term}': {e}")
            return []
    
    def _extract_relevance_indicators(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevance indicators from search result.
        """
        url = result.get("url", "").lower()
        title = result.get("title", "").lower()
        description = result.get("description", "").lower()
        
        indicators = {
            "is_github": "github.com" in url,
            "is_official_site": any(keyword in url for keyword in [".org", ".io", "docs.", "www."]),
            "has_download": any(keyword in title + description for keyword in ["download", "install", "setup"]),
            "is_tool": any(keyword in title + description for keyword in ["tool", "software", "utility", "program"]),
            "is_maintained": any(keyword in description for keyword in ["2024", "2023", "updated", "latest"]),
            "has_documentation": any(keyword in url + title for keyword in ["docs", "documentation", "wiki", "readme"])
        }
        
        return indicators


class SearchResultEnhancer:
    """
    Enhances search results with additional metadata from various sources.
    """
    
    @staticmethod
    async def enhance_github_results(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Enhance GitHub results with repository information.
        """
        enhanced_results = []
        
        async with aiohttp.ClientSession() as session:
            for result in results:
                enhanced_result = result.copy()
                
                if "github.com" in result.get("url", ""):
                    try:
                        github_info = await SearchResultEnhancer._fetch_github_info(
                            session, result.get("url")
                        )
                        enhanced_result.update(github_info)
                    except Exception as e:
                        print(f"Failed to enhance GitHub result: {e}")
                
                enhanced_results.append(enhanced_result)
        
        return enhanced_results
    
    @staticmethod
    async def _fetch_github_info(session: aiohttp.ClientSession, github_url: str) -> Dict[str, Any]:
        """
        Fetch additional information from GitHub API.
        """
        # Extract owner/repo from URL
        parts = github_url.replace("https://github.com/", "").split("/")
        if len(parts) < 2:
            return {}
            
        owner, repo = parts[0], parts[1]
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        
        try:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "github_stars": data.get("stargazers_count", 0),
                        "github_forks": data.get("forks_count", 0),
                        "github_language": data.get("language"),
                        "github_updated": data.get("updated_at"),
                        "github_license": data.get("license", {}).get("name") if data.get("license") else None,
                        "github_description": data.get("description"),
                        "github_topics": data.get("topics", [])
                    }
        except Exception:
            pass
            
        return {}
