#!/usr/bin/env python3
"""
Simple test chatbot to verify GitHub MCP server functionality.
This is a temporary testing interface - will be deleted after verification.
"""

import asyncio
import os
from dotenv import load_dotenv
import aiohttp

# Load environment variables
load_dotenv()

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
        """
        Search for GitHub repositories (mimicking the MCP server function)
        """
        try:
            if not query or not query.strip():
                return "Error: Query cannot be empty"
            
            query = query.strip()
            limit = max(1, min(limit, 20))  # Limit between 1 and 20
            
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
            
            print(f"🔍 Searching GitHub for: '{query}'" + (f" (language: {language})" if language else ""))
            print("⏳ Making API request...")
            
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
                                f"🔍 **GitHub Search Results for '{query}'**",
                                f"📊 Found {data.get('total_count', 0)} repositories (showing top {len(repositories)})",
                                ""
                            ]
                            
                            for i, repo in enumerate(repositories, 1):
                                stars = repo.get('stargazers_count', 0)
                                forks = repo.get('forks_count', 0)
                                language_info = repo.get('language', 'N/A')
                                description = repo.get('description', 'No description available')[:100]
                                if len(repo.get('description', '')) > 100:
                                    description += "..."
                                
                                result_lines.extend([
                                    f"**{i}. {repo['name']}** by {repo['owner']['login']}",
                                    f"   ⭐ {stars:,} stars | 🍴 {forks:,} forks | 💻 {language_info}",
                                    f"   📝 {description}",
                                    f"   🔗 {repo['html_url']}",
                                    ""
                                ])
                            
                            result_lines.append("✅ Search completed successfully!")
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
        """
        Get repository structure (mimicking the MCP server function)
        """
        try:
            # Parse repo URL to get owner and repo name
            if "github.com/" in repo_url:
                parts = repo_url.replace("https://github.com/", "").replace("http://github.com/", "").strip("/").split("/")
                if len(parts) >= 2:
                    owner, repo = parts[0], parts[1]
                else:
                    return "Error: Invalid GitHub repository URL format"
            else:
                # Assume it's in format "owner/repo"
                parts = repo_url.strip().split("/")
                if len(parts) == 2:
                    owner, repo = parts[0], parts[1]
                else:
                    return "Error: Invalid repository format. Use 'owner/repo' or full GitHub URL"
            
            print(f"📁 Getting structure for: {owner}/{repo}")
            print("⏳ Making API request...")
            
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
                            f"📁 **Repository Structure: {owner}/{repo}**",
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
                            result_lines.append("📂 **Directories:**")
                            for directory in sorted(directories, key=lambda x: x['name']):
                                result_lines.append(f"   📁 {directory['name']}/")
                            result_lines.append("")
                        
                        # Show files
                        if files:
                            result_lines.append("📄 **Files:**")
                            for file in sorted(files, key=lambda x: x['name']):
                                size = file.get('size', 0)
                                size_str = f"{size:,} bytes" if size < 1024 else f"{size/1024:.1f} KB"
                                result_lines.append(f"   📄 {file['name']} ({size_str})")
                            result_lines.append("")
                        
                        result_lines.append("✅ Repository structure retrieved successfully!")
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
    
    async def chat_loop(self):
        """Simple chat loop for testing GitHub functionality"""
        print("🤖 GitHub MCP Server Test Chatbot")
        print("=" * 50)
        print("Commands:")
        print("  - 'search <query>' - Search repositories")
        print("  - 'search <query> lang:<language>' - Search with language filter")
        print("  - 'structure <owner/repo>' - Get repository structure")
        print("  - 'structure <github-url>' - Get repository structure from URL")
        print("  - 'quit' or 'exit' to stop")
        print("=" * 50)
        print(f"🔑 GitHub Token: {'✅ Available' if self.github_token else '❌ Missing'}")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    print("⚠️ Please enter a command")
                    continue
                
                print("\n🔍 Bot: Processing...")
                
                # Parse commands
                if user_input.startswith("search "):
                    query = user_input[7:].strip()
                    language = ""
                    
                    # Check for language filter
                    if " lang:" in query:
                        parts = query.split(" lang:")
                        query = parts[0].strip()
                        language = parts[1].strip()
                    
                    result = await self.search_github_repositories(query, language)
                    
                elif user_input.startswith("structure "):
                    repo_input = user_input[10:].strip()
                    result = await self.get_repository_structure(repo_input)
                    
                else:
                    result = """
❓ Unknown command. Available commands:
- 'search <query>' - Search repositories
- 'search <query> lang:<language>' - Search with language filter  
- 'structure <owner/repo>' - Get repository structure
- 'structure <github-url>' - Get repository structure from URL

Examples:
- search fastapi
- search machine learning lang:python
- structure microsoft/vscode
- structure https://github.com/python/cpython
"""
                
                print(f"\n🤖 Bot: {result}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

async def main():
    """Run the GitHub test chatbot"""
    tester = GitHubTester()
    await tester.chat_loop()

if __name__ == "__main__":
    print("🚀 Starting GitHub MCP Server Test...")
    asyncio.run(main())
