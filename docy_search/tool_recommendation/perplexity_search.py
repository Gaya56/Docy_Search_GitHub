from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import aiohttp

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
    name="perplexity_search",
    version="1.0.0",
    description="Perplexity AI-powered web search with focus areas"
)

# Initialize the Perplexity API
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
perplexity_url = "https://api.perplexity.ai/chat/completions"

# Default search configuration
perplexity_config = {
    "parameters": {
        "default_max_results": 5,
        "default_focus": "general"
    }
}


@mcp.tool()
async def perplexity_search(
    query: str,
    focus: str = "general",
    max_results: int = 5
) -> str:
    """
    Search using Perplexity AI with focused results
    
    Args:
        query: Search query
        focus: Focus area (general, academic, news, coding, business)
        max_results: Maximum number of results
    """
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            query_preview = (query[:50] + "..." 
                           if len(query) > 50 else query)
            activity_id = await activity_tracker.start_activity(
                tool_name="perplexity_search",
                params={
                    "query": query_preview,
                    "focus": focus,
                    "max_results": max_results
                }
            )
            await activity_tracker.update_activity(
                activity_id, 
                progress=20, 
                details={"status": "Preparing Perplexity search"}
            )
        
        # Check API key
        if not perplexity_api_key:
            error_msg = ("Error: PERPLEXITY_API_KEY not found in "
                        "environment variables")
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
        # Define focus prompts
        focus_prompts = {
            "academic": ("Provide academic and research-focused results "
                        "with citations and scholarly sources"),
            "news": ("Focus on recent news and current events from "
                    "reliable news sources"),
            "coding": ("Emphasize programming, technical documentation, "
                      "and development resources"),
            "business": ("Focus on business insights, market analysis, "
                        "and industry information"),
            "general": ("Provide comprehensive general information "
                       "from reliable sources")
        }
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id, 
                progress=40, 
                details={"status": "Sending API request"}
            )
        
        # Prepare the request
        headers = {
            "Authorization": f"Bearer {perplexity_api_key}",
            "Content-Type": "application/json"
        }
        
        system_prompt = focus_prompts.get(focus, focus_prompts['general'])
        
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            "max_tokens": 1000,
            "temperature": 0.2
        }
        
        # Make the API call
        async with aiohttp.ClientSession() as session:
            async with session.post(
                perplexity_url, 
                headers=headers, 
                json=payload
            ) as response:
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.update_activity(
                        activity_id, 
                        progress=70, 
                        details={"status": "Processing results"}
                    )
                
                if response.status == 200:
                    data = await response.json()
                    result_content = data['choices'][0]['message']['content']
                    
                    # Format the result
                    formatted_result = format_perplexity_results(
                        query, focus, result_content)
                    
                    # Complete activity tracking with success
                    if TRACKING_AVAILABLE and activity_id:
                        result_preview = (
                            f"Perplexity search completed for: "
                            f"{query[:30]}{'...' if len(query) > 30 else ''}"
                        )
                        await activity_tracker.complete_activity(
                            activity_id, result=result_preview)
                    
                    return formatted_result
                else:
                    error_text = await response.text()
                    error_msg = (f"Perplexity API Error: {response.status} "
                               f"- {error_text}")
                    
                    # Complete activity tracking with error
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(
                            activity_id, 
                            result=f"API Error: {response.status}")
                    
                    return error_msg
                    
    except Exception as e:
        error_msg = (f"An error occurred while searching with Perplexity: "
                    f"{str(e)}")
        
        # Complete activity tracking with error
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, 
                result=f"Search failed: {str(e)[:50]}")
        
        return error_msg


def format_perplexity_results(query: str, focus: str, content: str) -> str:
    """Format Perplexity results for better readability"""
    if not content:
        return "No results found."
    
    formatted_result = "### 🧠 Perplexity AI Search Results\n\n"
    formatted_result += f"**Query:** {query}\n"
    formatted_result += f"**Focus:** {focus.title()}\n\n"
    formatted_result += "---\n\n"
    formatted_result += content
    formatted_result += "\n\n---\n"
    formatted_result += "*Powered by Perplexity AI*"
    
    return formatted_result


if __name__ == "__main__":
    mcp.run()
