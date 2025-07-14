#!/usr/bin/env python3
"""
Simple test chatbot to verify perplexity_search tool functionality.
This is a temporary testing interface - will be deleted after verification.
"""

import asyncio
import os
from dotenv import load_dotenv
import aiohttp

# Load environment variables
load_dotenv()

class TestChatbot:
    def __init__(self):
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY", "")
        self.perplexity_url = "https://api.perplexity.ai/chat/completions"
        
    async def perplexity_search(self, query: str, focus: str = "general", max_results: int = 5) -> str:
        """
        Test the perplexity search function directly
        """
        try:
            # Validate and sanitize inputs (same as the fixed version)
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
            
            print(f"🔍 Searching Perplexity for: '{query}' with focus: '{focus}'")
            print("⏳ Making API request...")
            
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
                            
                            # Format the result
                            formatted_result = f"""
🎯 **Perplexity Search Results**
**Query**: {query}
**Focus**: {focus.title()}
**Model**: {payload['model']}

**Results**:
{result}

---
✅ Search completed successfully!
"""
                            return formatted_result
                        else:
                            return "No results found in Perplexity response"
                    else:
                        error_text = await response.text()
                        return f"Perplexity API Error: {response.status} - {error_text}"
                        
        except Exception as e:
            return f"Error occurred while searching with Perplexity: {str(e)}"
    
    async def chat_loop(self):
        """Simple chat loop for testing"""
        print("🤖 Simple Test Chatbot for Perplexity Search")
        print("=" * 50)
        print("Commands:")
        print("  - Type your search query")
        print("  - Use 'focus:coding your query' to set focus")
        print("  - Type 'quit' or 'exit' to stop")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    print("⚠️ Please enter a search query")
                    continue
                
                # Parse focus if specified
                focus = "general"
                query = user_input
                
                if user_input.startswith("focus:"):
                    parts = user_input.split(" ", 1)
                    if len(parts) == 2:
                        focus = parts[0].replace("focus:", "")
                        query = parts[1]
                
                print("\n🔍 Bot: Searching...")
                
                # Call the perplexity search
                result = await self.perplexity_search(query, focus)
                
                print(f"\n🤖 Bot: {result}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")

async def main():
    """Run the test chatbot"""
    chatbot = TestChatbot()
    await chatbot.chat_loop()

if __name__ == "__main__":
    print("🚀 Starting Test Chatbot...")
    asyncio.run(main())
