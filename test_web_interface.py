#!/usr/bin/env python3
"""
Simple web interface to test perplexity_search tool.
Access at http://localhost:8000 after starting.
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

app = FastAPI(title="Perplexity Search Test", version="1.0.0")

class SearchRequest(BaseModel):
    query: str
    focus: str = "general"
    max_results: int = 5

class PerplexityTester:
    def __init__(self):
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"
        
    async def perplexity_search(self, query: str, focus: str = "general", max_results: int = 5) -> str:
        """Test the perplexity search function directly"""
        try:
            # Validate and sanitize inputs
            if not query or not query.strip():
                return "Error: Query cannot be empty"
            
            query = query.strip()
            
            # Ensure focus is not None and is a valid string
            if not focus or not isinstance(focus, str):
                focus = "general"
            focus = focus.lower().strip()
            
            # Validate focus value
            valid_focuses = ["general", "academic", "news", "coding", "business"]
            if focus not in valid_focuses:
                focus = "general"
            
            # Validate max_results
            if not isinstance(max_results, int) or max_results < 1:
                max_results = 5
            max_results = min(max_results, 10)  # Cap at 10
            
            if not self.perplexity_api_key:
                return "Error: PERPLEXITY_API_KEY not found in environment variables"
            
            # Define focus prompts
            focus_prompts = {
                "academic": "Provide academic and research-focused results with citations and scholarly sources",
                "news": "Focus on recent news and current events from reliable news sources", 
                "coding": "Emphasize programming, technical documentation, and development resources",
                "business": "Focus on business insights, market analysis, and industry information",
                "general": "Provide comprehensive general information from reliable sources"
            }
            
            # Prepare the request
            headers = {
                "Authorization": f"Bearer {self.perplexity_api_key}",
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
                    self.perplexity_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        
                        if 'choices' in data and len(data['choices']) > 0:
                            result = data['choices'][0]['message']['content']
                            return result
                        else:
                            return "No results found in Perplexity response"
                    else:
                        error_text = await response.text()
                        return f"Perplexity API Error: {response.status} - {error_text}"
                        
        except Exception as e:
            return f"Error occurred while searching with Perplexity: {str(e)}"

# Initialize the tester
tester = PerplexityTester()

@app.get("/", response_class=HTMLResponse)
async def get_test_interface():
    """Serve the test interface"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Perplexity Search Test</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
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
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 Perplexity Search Test</h1>
            <form id="searchForm">
                <div class="form-group">
                    <label for="query">Search Query:</label>
                    <input type="text" id="query" placeholder="Enter your search query..." required>
                </div>
                <div class="form-group">
                    <label for="focus">Focus:</label>
                    <select id="focus">
                        <option value="general">General</option>
                        <option value="academic">Academic</option>
                        <option value="news">News</option>
                        <option value="coding">Coding</option>
                        <option value="business">Business</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="max_results">Max Results:</label>
                    <input type="number" id="max_results" value="5" min="1" max="10">
                </div>
                <button type="submit" id="searchBtn">Search</button>
            </form>
            
            <div id="result" style="display: none;"></div>
        </div>

        <script>
            document.getElementById('searchForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const query = document.getElementById('query').value;
                const focus = document.getElementById('focus').value;
                const max_results = parseInt(document.getElementById('max_results').value);
                
                const resultDiv = document.getElementById('result');
                const searchBtn = document.getElementById('searchBtn');
                
                // Show loading state
                resultDiv.style.display = 'block';
                resultDiv.className = 'result loading';
                resultDiv.innerHTML = '🔍 Searching with Perplexity...';
                searchBtn.disabled = true;
                searchBtn.textContent = 'Searching...';
                
                try {
                    const response = await fetch('/search', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            query: query,
                            focus: focus,
                            max_results: max_results
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultDiv.className = 'result success';
                        resultDiv.innerHTML = '<h3>🎯 Search Results:</h3><pre>' + data.result + '</pre>';
                    } else {
                        resultDiv.className = 'result error';
                        resultDiv.innerHTML = '<h3>❌ Error:</h3>' + (data.detail || 'Unknown error');
                    }
                } catch (error) {
                    resultDiv.className = 'result error';
                    resultDiv.innerHTML = '<h3>❌ Error:</h3>' + error.message;
                }
                
                // Reset button
                searchBtn.disabled = false;
                searchBtn.textContent = 'Search';
            });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/search")
async def search_perplexity(request: SearchRequest):
    """Test the perplexity search endpoint"""
    try:
        result = await tester.perplexity_search(
            query=request.query,
            focus=request.focus,
            max_results=request.max_results
        )
        return {"result": result, "query": request.query, "focus": request.focus}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    api_key_status = "✅ Available" if tester.perplexity_api_key else "❌ Missing"
    return {
        "status": "healthy",
        "perplexity_api_key": api_key_status
    }

if __name__ == "__main__":
    print("🚀 Starting Perplexity Search Test Server...")
    print("📱 Open http://localhost:8000 to test the interface")
    print("🔧 API docs available at http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
