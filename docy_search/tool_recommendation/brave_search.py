from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests
import json

# Import activity tracking with graceful fallback
try:
    from .activity_tracker import activity_tracker
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    print("Activity tracking not available - running without tracking")


load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP(
    name="websearch", 
    version="1.0.0",
    description="Web search capability using Brave Search API"
)

# Initialize the Brave Search API
brave_api_key = os.getenv("BRAVE_API_KEY", "")
brave_search_url = "https://api.search.brave.com/res/v1/web/search"

# Default search configuration
websearch_config = {
    "parameters": {
        "default_num_results": 5,
        "include_domains": []
    }
}

@mcp.tool()
async def search_web(query: str, num_results: int = None) -> str:
    """Search the web using Brave Search API and return results as markdown formatted text."""
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="search_web",
                params={
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "num_results": num_results or websearch_config["parameters"]["default_num_results"]
                }
            )
            await activity_tracker.update_activity(activity_id, progress=20, details={"status": "Preparing search request"})
        
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": brave_api_key
        }
        
        params = {
            "q": query,
            "count": num_results or websearch_config["parameters"]["default_num_results"],
            "summary": 1,
            "freshness": "pw"  # past week for recent results
        }
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=40, details={"status": "Sending API request"})
        
        response = requests.get(brave_search_url, headers=headers, params=params)
        response.raise_for_status()
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Processing results"})
        
        search_results = response.json()
        formatted_results = format_search_results(search_results)
        
        # Complete activity tracking with success
        if TRACKING_AVAILABLE and activity_id:
            results_count = len(search_results.get("web", {}).get("results", []))
            result_preview = f"Found {results_count} results for: {query[:50]}{'...' if len(query) > 50 else ''}"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return formatted_results
    except Exception as e:
        error_msg = f"An error occurred while searching with Brave: {e}"
        
        # Complete activity tracking with error
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"Search failed: {str(e)[:100]}")
        
        return error_msg

def format_search_results(search_results):
    web_results = search_results.get("web", {}).get("results", [])
    if not web_results:
        return "No results found."

    markdown_results = "### Search Results:\n\n"
    for idx, result in enumerate(web_results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "")
        published_date = f" (Published: {result.get('age', '')})" if result.get('age') else ""
        
        markdown_results += f"**{idx}.** [{title}]({url}){published_date}\n"
        
        description = result.get("description", "")
        if description:
            markdown_results += f"> **Summary:** {description}\n\n"
        else:
            markdown_results += "\n"
    
    return markdown_results

if __name__ == "__main__":
    mcp.run()
