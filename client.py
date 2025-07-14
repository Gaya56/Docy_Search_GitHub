"""
Tool Recommendation Client Library

Easy-to-use client for integrating the Tool Recommendation System
into any Python application, especially Streamlit chatbots.
"""

import requests
from typing import Dict, Any


class ToolRecommendationClient:
    """Client for Tool Recommendation MCP Server."""
    
    def __init__(self, base_url: str = "http://localhost:8947"):
        """
        Initialize the client.
        
        Args:
            base_url: URL of the Tool Recommendation MCP Server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> bool:
        """Check if the server is healthy."""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def list_tools(self) -> Dict[str, Any]:
        """Get list of available tools."""
        try:
            response = self.session.get(f"{self.base_url}/tools")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e), "tools": {}}
    
    def execute_tool(self, tool_name: str, **parameters) -> Dict[str, Any]:
        """
        Execute a tool with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            **parameters: Tool parameters
            
        Returns:
            Dictionary with result or error
        """
        try:
            payload = {
                "tool_name": tool_name,
                "parameters": parameters
            }
            
            response = self.session.post(
                f"{self.base_url}/execute",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "result": None
            }
    
    def get_activity_status(self) -> Dict[str, Any]:
        """Get current activity status."""
        try:
            response = self.session.get(f"{self.base_url}/activity")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    # Convenience methods for common operations
    
    def search_tools(self, query: str, category: str = "general") -> str:
        """Search for tools based on query."""
        result = self.execute_tool("search_tools", query=query, category=category)
        return result.get("result", result.get("error", "No result"))
    
    def analyze_tools(self, search_results: str, requirements: str = "") -> str:
        """Analyze tool search results with AI."""
        result = self.execute_tool("analyze_tools", 
                                 search_results=search_results, 
                                 requirements=requirements)
        return result.get("result", result.get("error", "No result"))
    
    def search_web(self, query: str, num_results: int = 5) -> str:
        """Search the web using Brave Search."""
        result = self.execute_tool("search_web", query=query, num_results=num_results)
        return result.get("result", result.get("error", "No result"))
    
    def search_github(self, query: str, language: str = "", limit: int = 5) -> str:
        """Search GitHub repositories."""
        result = self.execute_tool("search_github_repositories", 
                                 query=query, language=language, limit=limit)
        return result.get("result", result.get("error", "No result"))
    
    def get_installation_guide(self, tool_name: str, os_type: str = "linux") -> str:
        """Get installation guide for a tool."""
        result = self.execute_tool("get_installation_guide", 
                                 tool_name=tool_name, os_type=os_type)
        return result.get("result", result.get("error", "No result"))
    
    def query_database(self, question: str) -> str:
        """Query database using natural language."""
        result = self.execute_tool("natural_language_query", question=question)
        return result.get("result", result.get("error", "No result"))


class StreamlitToolClient:
    """
    Streamlit-optimized client with progress tracking and caching.
    """
    
    def __init__(self, base_url: str = "http://localhost:8947"):
        self.client = ToolRecommendationClient(base_url)
    
    def search_and_analyze_tools(self, query: str, requirements: str = "", 
                                category: str = "general") -> Dict[str, str]:
        """
        Complete tool search and analysis workflow.
        Perfect for chatbot responses.
        """
        import streamlit as st
        
        # Show progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Search for tools
            status_text.text("🔍 Searching for tools...")
            progress_bar.progress(25)
            
            search_results = self.client.search_tools(query, category)
            
            if "error" in search_results.lower():
                return {"error": search_results}
            
            # Step 2: Analyze results
            status_text.text("🤖 Analyzing results with AI...")
            progress_bar.progress(75)
            
            analysis = self.client.analyze_tools(search_results, requirements)
            
            # Step 3: Complete
            status_text.text("✅ Analysis complete!")
            progress_bar.progress(100)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            return {
                "search_results": search_results,
                "analysis": analysis,
                "success": True
            }
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            return {"error": str(e), "success": False}
    
    def get_tool_recommendation(self, user_message: str) -> str:
        """
        Get tool recommendation based on user message.
        This is the main method for chatbot integration.
        """
        # Determine the type of request
        if "github" in user_message.lower():
            # GitHub search
            result = self.client.search_github(user_message)
        elif "install" in user_message.lower():
            # Installation guide
            tool_name = user_message.split("install")[-1].strip()
            result = self.client.get_installation_guide(tool_name)
        else:
            # General tool search and analysis
            workflow_result = self.search_and_analyze_tools(user_message)
            if workflow_result.get("success"):
                result = f"{workflow_result['search_results']}\n\n{workflow_result['analysis']}"
            else:
                result = workflow_result.get("error", "Something went wrong.")
        
        return result


# Example usage functions
def example_streamlit_integration():
    """Example of how to integrate with Streamlit."""
    import streamlit as st
    
    st.title("🔧 AI Tool Recommendation System")
    
    # Initialize client
    client = StreamlitToolClient()
    
    # Check server health
    if not client.client.health_check():
        st.error("❌ Tool Recommendation Server is not available!")
        st.stop()
    
    st.success("✅ Connected to Tool Recommendation Server")
    
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What tools are you looking for?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        with st.chat_message("assistant"):
            response = client.get_tool_recommendation(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Sidebar with tools info
    with st.sidebar:
        st.header("Available Tools")
        tools = client.client.list_tools()
        if "tools" in tools:
            for tool_name, tool_info in tools["tools"].items():
                st.text(f"• {tool_name}")


if __name__ == "__main__":
    # Simple test
    client = ToolRecommendationClient()
    
    if client.health_check():
        print("✅ Server is healthy")
        
        # Test tool search
        result = client.search_tools("web development frameworks")
        print("Search result:", result[:200] + "...")
        
    else:
        print("❌ Server is not available")
