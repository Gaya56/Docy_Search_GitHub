#!/usr/bin/env python3
"""
Simple web interface to test GitHub MCP server functionality.
Access at http://localhost:8001 after starting.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import aiohttp
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(title="GitHub MCP Server Test", version="1.0.0")

class SearchRequest(BaseModel):
    query: str
    language: str = ""
    limit: int = 5

class StructureRequest(BaseModel):
    repo_url: str

class GitHubTester:
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN", "")
        self.github_base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Tool-Recommendation-System"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"
        
    async def search_github_repositories(self, query: str, language: str = "", limit: int = 5) -> str:
        """Search for GitHub repositories"""
        try:
            if not query or not query.strip():
                return "Error: Query cannot be empty"
            
            query = query.strip()
            limit = max(1, min(limit, 20))
            
            # Build search query
            search_query = query
            if language:
                search_query += f" language:{language}"
            
            # Search repositories
            search_url = f"{self.github_base_url}/search/repositories"
            params = {
                "q": search_query,
                "sort": "stars",
                "order": "desc",
                "per_page": limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    search_url,
                    headers=self.headers,
                    params=params,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if "items" in data and len(data["items"]) > 0:
                            repositories = data["items"]
                            
                            # Format results
                            result_lines = [
                                f"🔍 GitHub Search Results for '{query}'",
                                f"📊 Found {data.get('total_count', 0)} repositories (showing top {len(repositories)})",
                                ""
                            ]
                            
                            for i, repo in enumerate(repositories, 1):
                                stars = repo.get('stargazers_count', 0)
                                forks = repo.get('forks_count', 0)
                                language_info = repo.get('language', 'N/A')
                                description = repo.get('description', 'No description available')[:150]
                                if len(repo.get('description', '')) > 150:
                                    description += "..."
                                
                                result_lines.extend([
                                    f"{i}. {repo['name']} by {repo['owner']['login']}",
                                    f"   ⭐ {stars:,} stars | 🍴 {forks:,} forks | 💻 {language_info}",
                                    f"   📝 {description}",
                                    f"   🔗 {repo['html_url']}",
                                    ""
                                ])
                            
                            return "\n".join(result_lines)
                        else:
                            return f"No repositories found for query: '{query}'"
                    
                    elif response.status == 403:
                        error_text = await response.text()
                        if "rate limit" in error_text.lower():
                            return "GitHub API rate limit exceeded. Please wait or add a GitHub token."
                        else:
                            return f"GitHub API access denied: {error_text}"
                    
                    else:
                        error_text = await response.text()
                        return f"GitHub API Error: {response.status} - {error_text}"
                        
        except Exception as e:
            return f"Error occurred while searching GitHub: {str(e)}"
    
    async def get_repository_structure(self, repo_url: str) -> str:
        """Get repository structure"""
        try:
            # Parse repo URL
            if "github.com/" in repo_url:
                parts = repo_url.replace("https://github.com/", "").replace("http://github.com/", "").strip("/").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                else:
                    return "Error: Invalid GitHub repository URL format"
            else:
                parts = repo_url.strip().split("/")
                if len(parts) == 2:
                    owner, repo = parts[0], parts[1]
                else:
                    return "Error: Invalid repository format. Use 'owner/repo' or full GitHub URL"
            
            # Get repository contents
            contents_url = f"{self.github_base_url}/repos/{owner}/{repo}/contents"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    contents_url,
                    headers=self.headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        # Format repository structure
                        result_lines = [
                            f"📁 Repository Structure: {owner}/{repo}",
                            f"🔗 https://github.com/{owner}/{repo}",
                            ""
                        ]
                        
                        # Separate files and directories
                        files = []
                        directories = []
                        
                        for item in data:
                            if item['type'] == 'file':
                                files.append(item)
                            elif item['type'] == 'dir':
                                directories.append(item)
                        
                        # Show directories first
                        if directories:
                            result_lines.append("📂 Directories:")
                            for directory in sorted(directories, key=lambda x: x['name']):
                                result_lines.append(f"   📁 {directory['name']}/")
                            result_lines.append("")
                        
                        # Show files
                        if files:
                            result_lines.append("📄 Files:")
                            for file in sorted(files, key=lambda x: x['name']):
                                size = file.get('size', 0)
                                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                                result_lines.append(f"   📄 {file['name']} ({size_str})")
                        
                        return "\n".join(result_lines)
                    
                    elif response.status == 404:
                        return f"Repository '{owner}/{repo}' not found or is private"
                    elif response.status == 403:
                        error_text = await response.text()
                        return f"Access denied to repository '{owner}/{repo}': {error_text}"
                    else:
                        error_text = await response.text()
                        return f"GitHub API Error: {response.status} - {error_text}"
                        
        except Exception as e:
            return f"Error occurred while getting repository structure: {str(e)}"

# Initialize the tester
tester = GitHubTester()

@app.get("/", response_class=HTMLResponse)
async def get_test_interface():
    """Serve the test interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GitHub MCP Server Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .tab-container { margin-bottom: 20px; }
            .tab-buttons { display: flex; border-bottom: 2px solid #ddd; }
            .tab-button { padding: 10px 20px; border: none; background: #f8f9fa; cursor: pointer; border-bottom: 2px solid transparent; }
            .tab-button.active { background: #007bff; color: white; border-bottom-color: #007bff; }
            .tab-content { display: none; padding: 20px 0; }
            .tab-content.active { display: block; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; font-weight: bold; }
            input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
            button { background-color: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #0056b3; }
            button:disabled { background-color: #6c757d; cursor: not-allowed; }
            .result { margin-top: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #f8f9fa; }
            .loading { text-align: center; color: #007bff; }
            .error { color: #dc3545; background-color: #f8d7da; border-color: #f5c6cb; }
            .success { color: #155724; background-color: #d4edda; border-color: #c3e6cb; }
            pre { white-space: pre-wrap; word-wrap: break-word; font-family: 'Courier New', monospace; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🐙 GitHub MCP Server Test</h1>
            
            <div class="tab-container">
                <div class="tab-buttons">
                    <button class="tab-button active" onclick="showTab('search')">🔍 Search Repositories</button>
                    <button class="tab-button" onclick="showTab('structure')">📁 Repository Structure</button>
                </div>
                
                <div id="search" class="tab-content active">
                    <form id="searchForm">
                        <div class="form-group">
                            <label for="query">Search Query:</label>
                            <input type="text" id="query" placeholder="e.g., machine learning, fastapi, react..." required>
                        </div>
                        <div class="form-group">
                            <label for="language">Language Filter (optional):</label>
                            <select id="language">
                                <option value="">All Languages</option>
                                <option value="python">Python</option>
                                <option value="javascript">JavaScript</option>
                                <option value="typescript">TypeScript</option>
                                <option value="java">Java</option>
                                <option value="go">Go</option>
                                <option value="rust">Rust</option>
                                <option value="c++">C++</option>
                                <option value="c">C</option>
                                <option value="c#">C#</option>
                                <option value="ruby">Ruby</option>
                                <option value="php">PHP</option>
                                <option value="swift">Swift</option>
                                <option value="kotlin">Kotlin</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <label for="limit">Number of Results:</label>
                            <input type="number" id="limit" value="5" min="1" max="20">
                        </div>
                        <button type="submit" id="searchBtn">Search Repositories</button>
                    </form>
                </div>
                
                <div id="structure" class="tab-content">
                    <form id="structureForm">
                        <div class="form-group">
                            <label for="repo_url">Repository URL or Owner/Repo:</label>
                            <input type="text" id="repo_url" placeholder="e.g., microsoft/vscode or https://github.com/python/cpython" required>
                        </div>
                        <button type="submit" id="structureBtn">Get Repository Structure</button>
                    </form>
                </div>
            </div>
            
            <div id="result" style="display: none;"></div>
        </div>

        <script>
            function showTab(tabName) {
                // Hide all tab contents
                document.querySelectorAll('.tab-content').forEach(tab => {
                    tab.classList.remove('active');
                });
                
                // Remove active class from all buttons
                document.querySelectorAll('.tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });
                
                // Show selected tab
                document.getElementById(tabName).classList.add('active');
                event.target.classList.add('active');
            }
            
            document.getElementById('searchForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const query = document.getElementById('query').value;
                const language = document.getElementById('language').value;
                const limit = parseInt(document.getElementById('limit').value);
                
                await makeRequest('/search', {
                    query: query,
                    language: language,
                    limit: limit
                }, 'searchBtn', 'Searching...');
            });
            
            document.getElementById('structureForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const repo_url = document.getElementById('repo_url').value;
                
                await makeRequest('/structure', {
                    repo_url: repo_url
                }, 'structureBtn', 'Getting structure...');
            });
            
            async function makeRequest(endpoint, data, buttonId, loadingText) {
                const resultDiv = document.getElementById('result');
                const button = document.getElementById(buttonId);
                const originalText = button.textContent;
                
                // Show loading state
                resultDiv.style.display = 'block';
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = '🔍 ' + loadingText;
                button.disabled = true;
                button.textContent = loadingText;
                
                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const responseData = await response.json();
                    
                    if (response.ok) {
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = '<h3>🎯 Results:</h3><pre>' + responseData.result + '</pre>';
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = '<h3>❌ Error:</h3>' + (responseData.detail || 'Unknown error');
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = '<h3>❌ Error:</h3>' + error.message;
                }
                
                // Reset button
                button.disabled = false;
                button.textContent = originalText;
            }
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/search")
async def search_repositories(request: SearchRequest):
    """Search GitHub repositories endpoint"""
    try:
        result = await tester.search_github_repositories(
            query=request.query,
            language=request.language,
            limit=request.limit
        )
        return {"result": result, "query": request.query, "language": request.language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/structure")
async def get_repository_structure(request: StructureRequest):
    """Get repository structure endpoint"""
    try:
        result = await tester.get_repository_structure(repo_url=request.repo_url)
        return {"result": result, "repo_url": request.repo_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    token_status = "✅ Available" if tester.github_token else "❌ Missing"
    return {
        "status": "healthy",
        "github_token": token_status
    }

if __name__ == "__main__":
    print("🚀 Starting GitHub MCP Server Test...")
    print("📱 Open http://localhost:8001 to test the interface")
    print("🔧 API docs available at http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)
