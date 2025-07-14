#!/usr/bin/env python3
"""
Test script to verify Perplexity API key and connection
"""

import os
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()

async def test_perplexity_api():
    """Test Perplexity API connection and key validity"""
    
    api_key = os.getenv("PERPLEXITY_API_KEY", "")
    
    print("🔍 Testing Perplexity API Connection")
    print("=" * 40)
    
    # Check if API key exists
    if not api_key:
        print("❌ PERPLEXITY_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...{api_key[-5:] if len(api_key) > 15 else api_key}")
    print(f"📏 Key length: {len(api_key)} characters")
    
    # Expected format: pplx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (at least 40+ chars)
    if len(api_key) < 30:
        print("⚠️  API key seems too short. Perplexity keys are usually 40+ characters")
    
    if not api_key.startswith("pplx-"):
        print("⚠️  API key should start with 'pplx-'")
    
    # Test API connection
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, this is a test. Please respond with 'API connection successful'."}
        ],
        "max_tokens": 50,
        "temperature": 0.1
    }
    
    print("\n🌐 Testing API connection...")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                
                print(f"📡 Response status: {response.status}")
                
                if response.status == 200:
                    data = await response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        result = data['choices'][0]['message']['content']
                        print("✅ API Connection Successful!")
                        print(f"🤖 Response: {result}")
                        return True
                    else:
                        print("❌ Unexpected response format")
                        print(f"Response: {data}")
                        return False
                        
                elif response.status == 401:
                    print("❌ 401 Unauthorized - Invalid API key")
                    response_text = await response.text()
                    print(f"Error details: {response_text}")
                    return False
                    
                elif response.status == 429:
                    print("❌ 429 Rate Limited - Too many requests")
                    return False
                    
                else:
                    print(f"❌ API Error: {response.status}")
                    response_text = await response.text()
                    print(f"Error details: {response_text}")
                    return False
                    
    except asyncio.TimeoutError:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

async def main():
    success = await test_perplexity_api()
    
    if not success:
        print("\n💡 Troubleshooting Tips:")
        print("1. Check your Perplexity API key at https://www.perplexity.ai/settings/api")
        print("2. Ensure the key starts with 'pplx-' and is complete")
        print("3. Verify your account has API access enabled")
        print("4. Check if you have sufficient credits/quota")
        print("5. Try regenerating your API key if needed")

if __name__ == "__main__":
    asyncio.run(main())
