#!/usr/bin/env python3
"""
Notion MCP Server for interacting with Notion pages.
Provides tools to read, write, search, and manage Notion documents.
"""

from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import aiohttp
from typing import Dict, List, Optional

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
    name="notion",
    version="1.0.0"
)

# Initialize Notion API configuration
notion_token = os.getenv("NOTION_API_KEY", "")
notion_page_id = os.getenv("NOTION_PAGE_ID", "")
notion_base_url = "https://api.notion.com/v1"
notion_headers = {
    "Authorization": f"Bearer {notion_token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

@mcp.tool()
async def read_notion_page(page_id: str = "") -> str:
    """
    Read the content of a Notion page
    
    Args:
        page_id: Notion page ID (uses default from env if not provided)
    """
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                "read_notion_page",
                {"page_id": page_id or notion_page_id}
            )
        
        # Use provided page_id or default from environment
        target_page_id = page_id or notion_page_id
        
        if not notion_token:
            error_msg = "Error: NOTION_API_KEY not found in environment variables"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        if not target_page_id:
            error_msg = "Error: No page ID provided and NOTION_PAGE_ID not set"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=30,
                details={"status": "Fetching page content"}
            )
        
        async with aiohttp.ClientSession() as session:
            # Get page details
            async with session.get(
                f"{notion_base_url}/pages/{target_page_id}",
                headers=notion_headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Failed to fetch page: {response.status} - {error_text}"
                    
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=error_msg)
                    
                    return error_msg
                
                page_data = await response.json()
        
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.update_activity(
                    activity_id,
                    progress=60,
                    details={"status": "Fetching page blocks"}
                )
            
            # Get page blocks
            async with session.get(
                f"{notion_base_url}/blocks/{target_page_id}/children",
                headers=notion_headers
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Failed to fetch page blocks: {response.status} - {error_text}"
                    
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=error_msg)
                    
                    return error_msg
                
                blocks_data = await response.json()
        
        # Format the result
        page_title = ""
        if 'properties' in page_data and 'title' in page_data['properties']:
            title_prop = page_data['properties']['title']
            if 'title' in title_prop and title_prop['title']:
                page_title = title_prop['title'][0]['text']['content']
        
        formatted_result = f"""
📑 **Notion Page Content**
**Page ID**: {target_page_id}
**Title**: {page_title or 'Untitled'}
**Last Edited**: {page_data.get('last_edited_time', 'Unknown')}

**Content**:
{_format_blocks(blocks_data.get('results', []))}

---
✅ Page content retrieved successfully!
"""
        
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"Read page: {page_title or 'Untitled'}"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return formatted_result
        
    except Exception as e:
        error_msg = f"Error reading Notion page: {str(e)}"
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=error_msg)
        
        return error_msg

@mcp.tool()
async def search_notion_page(query: str, page_id: str = "") -> str:
    """
    Search for content within a Notion page
    
    Args:
        query: Search query string
        page_id: Notion page ID (uses default from env if not provided)
    """
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                "search_notion_page",
                {"query": query, "page_id": page_id or notion_page_id}
            )
        
        # Use provided page_id or default from environment
        target_page_id = page_id or notion_page_id
        
        if not notion_token:
            error_msg = "Error: NOTION_API_KEY not found in environment variables"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        if not target_page_id:
            error_msg = "Error: No page ID provided and NOTION_PAGE_ID not set"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=30,
                details={"status": "Searching Notion"}
            )
        
        # Use Notion's search API
        search_payload = {
            "query": query,
            "filter": {
                "value": "page",
                "property": "object"
            },
            "page_size": 10
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{notion_base_url}/search",
                headers=notion_headers,
                json=search_payload
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Search failed: {response.status} - {error_text}"
                    
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=error_msg)
                    
                    return error_msg
                
                search_data = await response.json()
        
        # Format search results
        results = search_data.get('results', [])
        
        if not results:
            result_msg = f"No results found for query: '{query}'"
            
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=result_msg)
            
            return result_msg
        
        formatted_result = f"""
🔍 **Notion Search Results**
**Query**: {query}
**Found**: {len(results)} result(s)

**Results**:
"""
        
        for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
            title = "Untitled"
            if 'properties' in result and 'title' in result['properties']:
                title_prop = result['properties']['title']
                if 'title' in title_prop and title_prop['title']:
                    title = title_prop['title'][0]['text']['content']
            
            formatted_result += f"""
{i}. **{title}**
   - ID: {result['id']}
   - URL: {result.get('url', 'N/A')}
   - Last edited: {result.get('last_edited_time', 'Unknown')}
"""
        
        formatted_result += "\n---\n✅ Search completed successfully!"
        
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"Found {len(results)} results for '{query}'"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return formatted_result
        
    except Exception as e:
        error_msg = f"Error searching Notion: {str(e)}"
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=error_msg)
        
        return error_msg

@mcp.tool()
async def add_to_notion_page(content: str, page_id: str = "", block_type: str = "paragraph") -> str:
    """
    Add content to a Notion page
    
    Args:
        content: Content to add to the page
        page_id: Notion page ID (uses default from env if not provided)
        block_type: Type of block to create (paragraph, heading_1, heading_2, heading_3, bulleted_list_item, numbered_list_item)
    """
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                "add_to_notion_page",
                {"content": content[:50] + "..." if len(content) > 50 else content, 
                 "page_id": page_id or notion_page_id, "block_type": block_type}
            )
        
        # Use provided page_id or default from environment
        target_page_id = page_id or notion_page_id
        
        if not notion_token:
            error_msg = "Error: NOTION_API_KEY not found in environment variables"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        if not target_page_id:
            error_msg = "Error: No page ID provided and NOTION_PAGE_ID not set"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=30,
                details={"status": "Creating block content"}
            )
        
        # Create block data based on type
        block_data = _create_block_data(content, block_type)
        
        payload = {
            "children": [block_data]
        }
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=60,
                details={"status": "Adding to Notion page"}
            )
        
        async with aiohttp.ClientSession() as session:
            async with session.patch(
                f"{notion_base_url}/blocks/{target_page_id}/children",
                headers=notion_headers,
                json=payload
            ) as response:
                
                if response.status != 200:
                    error_text = await response.text()
                    error_msg = f"Failed to add content: {response.status} - {error_text}"
                    
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(activity_id, result=error_msg)
                    
                    return error_msg
                
                await response.json()
        
        formatted_result = f"""
📝 **Content Added to Notion Page**
**Page ID**: {target_page_id}
**Block Type**: {block_type}
**Content**: {content[:100]}{'...' if len(content) > 100 else ''}

---
✅ Content added successfully!
"""
        
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"Added {block_type} to page"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return formatted_result
        
    except Exception as e:
        error_msg = f"Error adding content to Notion page: {str(e)}"
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=error_msg)
        
        return error_msg

def _format_blocks(blocks: List[Dict]) -> str:
    """Format Notion blocks for display"""
    formatted_content = ""
    
    for block in blocks:
        block_type = block.get('type', 'unknown')
        block_content = block.get(block_type, {})
        
        if block_type == 'paragraph':
            text = _extract_text_from_rich_text(block_content.get('rich_text', []))
            if text.strip():
                formatted_content += f"{text}\n\n"
        
        elif block_type.startswith('heading_'):
            level = block_type.split('_')[1]
            text = _extract_text_from_rich_text(block_content.get('rich_text', []))
            if text.strip():
                prefix = '#' * int(level)
                formatted_content += f"{prefix} {text}\n\n"
        
        elif block_type in ['bulleted_list_item', 'numbered_list_item']:
            text = _extract_text_from_rich_text(block_content.get('rich_text', []))
            if text.strip():
                prefix = '•' if block_type == 'bulleted_list_item' else '1.'
                formatted_content += f"{prefix} {text}\n"
        
        elif block_type == 'to_do':
            text = _extract_text_from_rich_text(block_content.get('rich_text', []))
            checked = block_content.get('checked', False)
            checkbox = '☑️' if checked else '☐'
            if text.strip():
                formatted_content += f"{checkbox} {text}\n"
        
        else:
            # Generic handling for other block types
            if 'rich_text' in block_content:
                text = _extract_text_from_rich_text(block_content.get('rich_text', []))
                if text.strip():
                    formatted_content += f"[{block_type.upper()}] {text}\n\n"
    
    return formatted_content.strip() or "No content found"

def _extract_text_from_rich_text(rich_text_array: List[Dict]) -> str:
    """Extract plain text from Notion rich text array"""
    text = ""
    for item in rich_text_array:
        if 'text' in item and 'content' in item['text']:
            text += item['text']['content']
    return text

def _create_block_data(content: str, block_type: str) -> Dict:
    """Create block data for Notion API"""
    rich_text = [{"type": "text", "text": {"content": content}}]
    
    if block_type == "paragraph":
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": rich_text}
        }
    elif block_type.startswith("heading_"):
        return {
            "object": "block", 
            "type": block_type,
            block_type: {"rich_text": rich_text}
        }
    elif block_type in ["bulleted_list_item", "numbered_list_item"]:
        return {
            "object": "block",
            "type": block_type,
            block_type: {"rich_text": rich_text}
        }
    elif block_type == "to_do":
        return {
            "object": "block",
            "type": "to_do", 
            "to_do": {"rich_text": rich_text, "checked": False}
        }
    else:
        # Default to paragraph
        return {
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": rich_text}
        }

if __name__ == "__main__":
    mcp.run()
