from fastmcp import FastMCP
import os
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from typing import List, Dict, Any
import re
import aiohttp
import sqlite3
import tempfile
import subprocess
import shutil
from pathlib import Path

# Import activity tracking with graceful fallback
try:
    from .activity_tracker import activity_tracker
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    print("Activity tracking not available - running without tracking")

load_dotenv()
mcp = FastMCP("tool_recommendation")

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-1.5-flash')

@mcp.tool()
async def search_tools(query: str, category: str = "general") -> str:
    """Search for tools using Brave Search API and return relevant results for any development task."""
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="search_tools",
                params={
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "category": category
                }
            )
            await activity_tracker.update_activity(activity_id, progress=20, details={"status": "Preparing tool search"})
        
        brave_api_key = os.getenv('BRAVE_API_KEY')
        if not brave_api_key:
            error_msg = "Error: BRAVE_API_KEY not found in environment variables"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        # Enhanced category keywords for general development
        category_keywords = {
            "web": "web development tools frameworks frontend backend",
            "mobile": "mobile app development tools android ios react native flutter",
            "desktop": "desktop application development tools electron qt",
            "database": "database tools management sql nosql mongodb postgresql",
            "devops": "devops tools ci cd deployment docker kubernetes",
            "testing": "testing tools unit integration automation selenium jest",
            "design": "design tools ui ux figma sketch prototyping",
            "data": "data analysis tools python r jupyter pandas numpy",
            "ai": "artificial intelligence machine learning tools tensorflow pytorch",
            "game": "game development tools unity unreal godot",
            "security": "security tools vulnerability scanning penetration testing",
            "productivity": "productivity tools development ide editors vscode",
            "general": "development tools programming utilities software engineering"
        }
        
        enhanced_query = f"{query} {category_keywords.get(category, category_keywords['general'])}"
        
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": brave_api_key
        }
        
        params = {
            "q": enhanced_query,
            "count": 10,
            "search_lang": "en",
            "country": "US",
            "safesearch": "moderate",
            "freshness": "py"  # Past year for recent tools
        }
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=40, details={"status": "Sending tool search request"})
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Processing tool search results"})
        
        data = response.json()
        results = data.get('web', {}).get('results', [])
        
        if not results:
            error_msg = f"No search results found for query: {query}"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(activity_id, result=error_msg)
            return error_msg
        
        output = f"Search Results for '{query}' (Category: {category}):\n\n"
        
        for i, result in enumerate(results[:8], 1):
            title = result.get('title', 'No title')
            url = result.get('url', 'No URL')
            description = result.get('description', 'No description')
            
            output += f"{i}. **{title}**\n"
            output += f"   URL: {url}\n"
            output += f"   Description: {description}\n\n"
        
        # Complete activity tracking with success
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"Found {len(results[:8])} tool results for: {query[:50]}{'...' if len(query) > 50 else ''}"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return output
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Search API error: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"Tool search API error: {str(e)[:100]}")
        return error_msg
    except Exception as e:
        error_msg = f"Unexpected error during search: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"Tool search error: {str(e)[:100]}")
        return error_msg

@mcp.tool()
async def analyze_tools(search_results: str, requirements: str = "") -> str:
    """Analyze search results using AI to rank and evaluate tools for any development purpose."""
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="analyze_tools",
                params={
                    "requirements": requirements[:100] + "..." if len(requirements) > 100 else requirements,
                    "results_length": len(search_results)
                }
            )
            await activity_tracker.update_activity(activity_id, progress=30, details={"status": "Preparing AI analysis"})
        
        prompt = f"""Analyze these tool search results and provide intelligent recommendations:

SEARCH RESULTS:
{search_results}

USER REQUIREMENTS: {requirements if requirements else "General development use case"}

Please analyze and rank the tools based on:
1. Relevance to requirements
2. Reliability and maturity
3. Ease of installation/use
4. Community support and documentation
5. Performance and scalability
6. Cost considerations (free vs paid)

For each recommended tool, provide:
- Tool name and brief description
- Relevance score (1-10)
- Reliability assessment
- Installation complexity (Easy/Medium/Hard)
- Key features and use cases
- Potential concerns or limitations
- Cost information (if applicable)

Rank the top 5 tools and explain your reasoning. Focus on practical recommendations for developers, engineers, and technical professionals working on various projects."""

        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Running AI tool analysis"})

        response = model.generate_content(prompt)
        result = f"# Tool Analysis and Recommendations\n\n{response.text}"
        
        # Complete activity tracking with success
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"AI analysis complete: {len(response.text)} chars of recommendations"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return result
    except Exception as e:
        error_msg = f"Analysis failed: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"AI analysis error: {str(e)[:100]}")
        return error_msg

@mcp.tool()
async def get_installation_guide(tool_name: str, os_type: str = "linux") -> str:
    """Generate installation instructions for a specific tool on various platforms."""
    
    # Search for official installation instructions
    brave_api_key = os.getenv('BRAVE_API_KEY')
    if not brave_api_key:
        return "Error: BRAVE_API_KEY not found in environment variables"
    
    query = f"{tool_name} official installation guide {os_type} setup instructions documentation"
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave_api_key
    }
    
    params = {
        "q": query,
        "count": 5,
        "search_lang": "en"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = data.get('web', {}).get('results', [])
        
        # Collect installation-related content
        installation_content = ""
        for result in results:
            title = result.get('title', '')
            url = result.get('url', '')
            description = result.get('description', '')
            
            if any(keyword in title.lower() or keyword in description.lower() 
                   for keyword in ['install', 'setup', 'download', 'documentation', 'guide', 'getting started']):
                installation_content += f"Source: {title}\nURL: {url}\nInfo: {description}\n\n"
        
        # Generate installation guide using AI
        prompt = f"""Create a comprehensive installation guide for {tool_name} on {os_type} systems.

Use this research data:
{installation_content}

Provide:
1. Prerequisites and system requirements
2. Step-by-step installation instructions
3. Common installation methods (package manager, binary download, source compilation)
4. Post-installation verification steps
5. Common troubleshooting tips
6. Configuration recommendations
7. Getting started tips

Format as a clear, actionable guide that developers and technical users can follow."""

        ai_response = model.generate_content(prompt)
        return f"# Installation Guide: {tool_name} ({os_type})\n\n{ai_response.text}"
        
    except Exception as e:
        return f"Installation guide generation failed: {str(e)}"

@mcp.tool()
async def recommend_tools_for_task(task_description: str, skill_level: str = "intermediate") -> str:
    """Get comprehensive tool recommendations for a specific development task or project."""
    
    # Search for tools related to the task
    search_query = f"best tools for {task_description} {skill_level} development 2024 2025"
    
    brave_api_key = os.getenv('BRAVE_API_KEY')
    if not brave_api_key:
        return "Error: BRAVE_API_KEY not found in environment variables"
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": brave_api_key
    }
    
    params = {
        "q": search_query,
        "count": 15,
        "search_lang": "en",
        "freshness": "py"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        results = data.get('web', {}).get('results', [])
        
        # Compile search results
        search_content = ""
        for result in results:
            title = result.get('title', '')
            url = result.get('url', '')
            description = result.get('description', '')
            search_content += f"Title: {title}\nURL: {url}\nDescription: {description}\n\n"
        
        # Analyze with AI
        prompt = f"""Based on this search data, provide comprehensive tool recommendations for: "{task_description}"

Target skill level: {skill_level}

SEARCH DATA:
{search_content}

Provide a structured recommendation including:

1. **Essential Tools** (3-5 must-have tools)
2. **Specialized Tools** (2-3 advanced/specific tools)
3. **Alternative Options** (backup choices)
4. **Tool Categories and Workflow**
5. **Learning Path** (if beginner/intermediate)
6. **Integration Recommendations**
7. **Budget Considerations** (free vs paid options)

For each tool include:
- Name and brief description
- Why it's recommended for this task
- Difficulty level
- Installation method (brief)
- Key features relevant to the task
- Cost (if applicable)

Focus on practical, actionable recommendations that consider the user's skill level and project requirements."""

        ai_response = model.generate_content(prompt)
        return f"# Tool Recommendations: {task_description}\n\n{ai_response.text}"
        
    except Exception as e:
        return f"Tool recommendation failed: {str(e)}"

@mcp.tool()
async def compare_tools(tool_names: str) -> str:
    """Compare multiple tools side by side with detailed analysis for any development purpose."""
    
    tools = [tool.strip() for tool in tool_names.split(',')]
    if len(tools) < 2:
        return "Please provide at least 2 tools to compare (comma-separated)"
    
    # Search for comparison and information about each tool
    brave_api_key = os.getenv('BRAVE_API_KEY')
    if not brave_api_key:
        return "Error: BRAVE_API_KEY not found in environment variables"
    
    comparison_data = ""
    
    for tool in tools:
        query = f"{tool} features documentation pros cons review comparison 2024"
        
        url = "https://api.search.brave.com/res/v1/web/search"
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": brave_api_key
        }
        
        params = {
            "q": query,
            "count": 5,
            "search_lang": "en"
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('web', {}).get('results', [])
            
            comparison_data += f"\n=== {tool.upper()} ===\n"
            for result in results:
                title = result.get('title', '')
                description = result.get('description', '')
                comparison_data += f"- {title}: {description}\n"
            
        except Exception as e:
            comparison_data += f"\n=== {tool.upper()} ===\nError gathering data: {str(e)}\n"
    
    # Generate comparison using AI
    prompt = f"""Create a detailed comparison of these development tools: {', '.join(tools)}

RESEARCH DATA:
{comparison_data}

Provide a comprehensive comparison including:

1. **Overview Table** (quick feature comparison)
2. **Detailed Analysis** for each tool:
   - Primary use cases
   - Key strengths
   - Notable limitations
   - Target audience
   - Learning curve
   - Installation complexity
   - Cost (free/paid/freemium)
   - Community support
   - Performance characteristics
3. **Head-to-Head Comparison**
4. **Recommendation Matrix** (when to use which tool)
5. **Migration Considerations** (if switching between tools)
6. **Future Outlook** (development trends, roadmap)

Make the comparison actionable for decision-making in development projects."""

    try:
        ai_response = model.generate_content(prompt)
        return f"# Tool Comparison: {', '.join(tools)}\n\n{ai_response.text}"
    except Exception as e:
        return f"Tool comparison failed: {str(e)}"


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
            query_preview = (
                query[:50] + "..." if len(query) > 50 else query
            )
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
        
        perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
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
                "https://api.perplexity.ai/chat/completions",
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
                    formatted_result = f"### 🧠 Perplexity AI Search Results\n\n"
                    formatted_result += f"**Query:** {query}\n"
                    formatted_result += f"**Focus:** {focus.title()}\n\n"
                    formatted_result += "---\n\n"
                    formatted_result += result_content
                    formatted_result += "\n\n---\n"
                    formatted_result += "*Powered by Perplexity AI*"
                    
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


@mcp.tool()
async def natural_language_query(question: str) -> str:
    """
    Convert natural language question to SQL and execute against database
    
    Args:
        question: Natural language question about the database
    """
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            question_preview = (
                question[:50] + "..." if len(question) > 50 else question
            )
            activity_id = await activity_tracker.start_activity(
                tool_name="natural_language_query",
                params={"question": question_preview}
            )
            await activity_tracker.update_activity(
                activity_id,
                progress=20,
                details={"status": "Converting to SQL"}
            )
    
        db_path = "/workspaces/Docy_Search_GitHub/docy_search.db"
        
        # Simple NL to SQL conversion patterns
        sql_patterns = {
            r"how many.*conversations":
                "SELECT COUNT(*) as count FROM conversations",
            r"latest.*conversations":
                ("SELECT * FROM conversations ORDER BY created_at DESC "
                 "LIMIT 10"),
            r"search.*memory":
                "SELECT * FROM memory_items WHERE content LIKE '%{}%'",
            r"all.*agents":
                "SELECT * FROM agents",
            r"recent.*activity":
                ("SELECT * FROM conversations ORDER BY updated_at DESC "
                 "LIMIT 5"),
            r"show.*tables":
                "SELECT name FROM sqlite_master WHERE type='table'",
            r"count.*memory":
                "SELECT COUNT(*) as count FROM memory_items",
            r"list.*conversations":
                "SELECT id, title, created_at FROM conversations LIMIT 20"
        }
        
        question_lower = question.lower()
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=50,
                details={"status": "Executing query"}
            )
        
        # Find matching pattern
        sql_query = None
        for pattern, query_template in sql_patterns.items():
            if re.search(pattern, question_lower):
                if '{}' in query_template:
                    # Extract search term (last few words)
                    words = question_lower.split()
                    search_term = ' '.join(words[-2:])
                    sql_query = query_template.format(search_term)
                else:
                    sql_query = query_template
                break
        
        if not sql_query:
            error_msg = (
                f"Could not understand question: '{question}'. "
                f"Try asking about conversations, memory, or agents."
            )
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
        # Execute query safely (only SELECT operations)
        if not sql_query.upper().strip().startswith('SELECT'):
            error_msg = "Only SELECT queries are allowed for security"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
        try:
            with sqlite3.connect(db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.execute(sql_query)
                rows = cursor.fetchall()
                
                # Convert to list of dicts
                result = []
                for row in rows:
                    result.append(dict(row))
                
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.update_activity(
                        activity_id,
                        progress=80,
                        details={"status": "Formatting results"}
                    )
                
                # Format results
                if len(result) == 0:
                    formatted_result = "No results found."
                else:
                    formatted_result = json.dumps(
                        result, indent=2, default=str
                    )
                
                # Complete activity tracking with success
                if TRACKING_AVAILABLE and activity_id:
                    result_preview = (
                        f"Query completed: {len(result)} rows returned"
                    )
                    await activity_tracker.complete_activity(
                        activity_id, result=result_preview)
                
                return formatted_result
        
        except Exception as e:
            error_msg = f"Database query failed: {str(e)}"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
    except Exception as e:
        error_msg = f"Error processing question: {str(e)}"
        
        # Complete activity tracking with error
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Processing failed: {str(e)[:50]}")
        
        return error_msg


@mcp.tool()
async def get_database_schema() -> str:
    """Get the database schema information"""
    activity_id = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="get_database_schema",
                params={}
            )
            await activity_tracker.update_activity(
                activity_id,
                progress=30,
                details={"status": "Reading schema"}
            )
        
        db_path = "/workspaces/Docy_Search_GitHub/docy_search.db"
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tables = cursor.fetchall()
            
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.update_activity(
                    activity_id,
                    progress=70,
                    details={"status": "Getting table details"}
                )
            
            schema_info = {}
            for (table_name,) in tables:
                cursor = conn.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                schema_info[table_name] = [
                    {
                        "name": col[1],
                        "type": col[2],
                        "not_null": bool(col[3])
                    }
                    for col in columns
                ]
            
            formatted_schema = json.dumps(schema_info, indent=2)
            
            # Complete activity tracking with success
            if TRACKING_AVAILABLE and activity_id:
                result_preview = f"Schema retrieved: {len(tables)} tables"
                await activity_tracker.complete_activity(
                    activity_id, result=result_preview)
            
            return formatted_schema
            
    except Exception as e:
        error_msg = f"Error getting schema: {str(e)}"
        
        # Complete activity tracking with error
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Schema error: {str(e)[:50]}")
        
        return error_msg


@mcp.tool()
async def analyze_repository(repo_url_or_path: str) -> str:
    """
    Analyze any repository's code quality, structure, and dependencies
    
    Args:
        repo_url_or_path: GitHub URL or local path to repository
    """
    activity_id = None
    temp_path = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="analyze_repository",
                params={"repo": repo_url_or_path[:100]}
            )
            await activity_tracker.update_activity(
                activity_id,
                progress=10,
                details={"status": "Cloning repository"}
            )
        
        # Clone or validate repository
        local_path = None
        if repo_url_or_path.startswith(('http://', 'https://', 'git@')):
            # It's a URL, need to clone
            temp_path = tempfile.mkdtemp(prefix="code_analysis_")
            try:
                result = subprocess.run([
                    'git', 'clone', '--depth', '1', 
                    repo_url_or_path, temp_path
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    local_path = temp_path
                else:
                    shutil.rmtree(temp_path, ignore_errors=True)
                    error_msg = f"Could not clone repository: {repo_url_or_path}"
                    if TRACKING_AVAILABLE and activity_id:
                        await activity_tracker.complete_activity(
                            activity_id, result=error_msg)
                    return error_msg
            except (subprocess.TimeoutExpired, 
                   subprocess.CalledProcessError) as e:
                shutil.rmtree(temp_path, ignore_errors=True)
                error_msg = f"Clone failed: {str(e)}"
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.complete_activity(
                        activity_id, result=error_msg)
                return error_msg
        else:
            # It's a local path
            if Path(repo_url_or_path).exists():
                local_path = repo_url_or_path
            else:
                error_msg = f"Path does not exist: {repo_url_or_path}"
                if TRACKING_AVAILABLE and activity_id:
                    await activity_tracker.complete_activity(
                        activity_id, result=error_msg)
                return error_msg
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=40,
                details={"status": "Analyzing structure"}
            )
        
        # Analyze repository
        repo_path = Path(local_path)
        
        # Basic info
        repo_info = {
            "name": repo_path.name,
            "total_files": 0,
            "has_readme": False,
            "languages": {}
        }
        
        # Count files and detect languages
        for file_path in repo_path.rglob("*"):
            if file_path.is_file():
                repo_info["total_files"] += 1
                ext = file_path.suffix.lower()
                if ext:
                    repo_info["languages"][ext] = repo_info["languages"].get(ext, 0) + 1
        
        # Check for README
        readme_files = ["README.md", "readme.md", "README.txt", "README"]
        for readme in readme_files:
            if (repo_path / readme).exists():
                repo_info["has_readme"] = True
                break
        
        # Dependencies analysis
        dependencies = {"language": "unknown", "package_managers": []}
        
        # Python
        py_files = ["requirements.txt", "pyproject.toml", "setup.py"]
        for py_file in py_files:
            if (repo_path / py_file).exists():
                dependencies["language"] = "python"
                dependencies["package_managers"].append(py_file)
        
        # JavaScript/Node.js
        if (repo_path / "package.json").exists():
            dependencies["language"] = "javascript"
            dependencies["package_managers"].append("package.json")
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=80,
                details={"status": "Formatting results"}
            )
        
        # Combine results
        analysis_result = {
            "repository_url": repo_url_or_path,
            "summary": repo_info,
            "dependencies": dependencies
        }
        
        # Clean up temporary directory
        if temp_path:
            shutil.rmtree(temp_path, ignore_errors=True)
        
        # Complete activity tracking
        if TRACKING_AVAILABLE and activity_id:
            result_preview = (
                f"Analysis completed for {repo_info['name']} "
                f"({dependencies['language']} project)"
            )
            await activity_tracker.complete_activity(
                activity_id, result=result_preview)
        
        return json.dumps(analysis_result, indent=2, default=str)
        
    except Exception as e:
        # Clean up on error
        if temp_path:
            shutil.rmtree(temp_path, ignore_errors=True)
        
        error_msg = f"Error analyzing repository: {str(e)}"
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Analysis failed: {str(e)[:50]}")
        
        return error_msg


if __name__ == "__main__":
    mcp.run()
