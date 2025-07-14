"""
Complete Streamlit Chatbot Example with Tool Recommendation Integration

This example shows how to integrate the Tool Recommendation Container
into a full-featured Streamlit chatbot application with Notion integration.
"""

import streamlit as st
import requests
import json
import os

# Import the client (adjust path as needed)
try:
    from client import StreamlitToolClient, ToolRecommendationClient
except ImportError:
    st.error("❌ Cannot import client. Make sure client.py is in the same directory.")
    st.stop()


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "tool_client" not in st.session_state:
        st.session_state.tool_client = None
    
    if "server_status" not in st.session_state:
        st.session_state.server_status = "unknown"
    
    if "available_tools" not in st.session_state:
        st.session_state.available_tools = {}
    
    if "notion_enabled" not in st.session_state:
        st.session_state.notion_enabled = False
    
    if "notion_config" not in st.session_state:
        st.session_state.notion_config = {
            "api_key": "",
            "page_id": "",
            "connected": False
        }


class NotionClient:
    """Simple Notion client for Streamlit integration."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
    
    def test_connection(self) -> bool:
        """Test if the API key is valid by making a simple request."""
        try:
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def read_page(self, page_id: str) -> dict:
        """Read a Notion page content."""
        try:
            # Get page details
            page_response = requests.get(
                f"{self.base_url}/pages/{page_id}",
                headers=self.headers,
                timeout=10
            )
            
            if page_response.status_code != 200:
                return {"error": f"Failed to fetch page: {page_response.status_code}"}
            
            page_data = page_response.json()
            
            # Get page blocks
            blocks_response = requests.get(
                f"{self.base_url}/blocks/{page_id}/children",
                headers=self.headers,
                timeout=10
            )
            
            if blocks_response.status_code != 200:
                return {"error": f"Failed to fetch blocks: {blocks_response.status_code}"}
            
            blocks_data = blocks_response.json()
            
            return {
                "page": page_data,
                "blocks": blocks_data.get("results", [])
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def format_page_content(self, page_data: dict) -> str:
        """Format page content for display."""
        if "error" in page_data:
            return f"❌ Error: {page_data['error']}"
        
        page = page_data["page"]
        blocks = page_data["blocks"]
        
        # Extract title
        title = "Untitled"
        if 'properties' in page and 'title' in page['properties']:
            title_prop = page['properties']['title']
            if 'title' in title_prop and title_prop['title']:
                title = title_prop['title'][0]['text']['content']
        
        # Format content
        content = self._format_blocks(blocks)
        
        return f"""
📑 **{title}**
**Last Edited**: {page.get('last_edited_time', 'Unknown')}

**Content**:
{content}
"""
    
    def _format_blocks(self, blocks: list) -> str:
        """Format Notion blocks into readable text."""
        formatted_text = ""
        
        for block in blocks:
            block_type = block.get('type', 'unknown')
            
            if block_type == 'paragraph':
                text = self._extract_rich_text(block.get('paragraph', {}).get('rich_text', []))
                if text.strip():
                    formatted_text += f"{text}\n\n"
            
            elif block_type == 'heading_1':
                text = self._extract_rich_text(block.get('heading_1', {}).get('rich_text', []))
                if text.strip():
                    formatted_text += f"# {text}\n\n"
            
            elif block_type == 'heading_2':
                text = self._extract_rich_text(block.get('heading_2', {}).get('rich_text', []))
                if text.strip():
                    formatted_text += f"## {text}\n\n"
            
            elif block_type == 'heading_3':
                text = self._extract_rich_text(block.get('heading_3', {}).get('rich_text', []))
                if text.strip():
                    formatted_text += f"### {text}\n\n"
            
            elif block_type == 'bulleted_list_item':
                text = self._extract_rich_text(block.get('bulleted_list_item', {}).get('rich_text', []))
                if text.strip():
                    formatted_text += f"• {text}\n"
            
            elif block_type == 'numbered_list_item':
                text = self._extract_rich_text(block.get('numbered_list_item', {}).get('rich_text', []))
                if text.strip():
                    formatted_text += f"1. {text}\n"
            
            elif block_type == 'to_do':
                text = self._extract_rich_text(block.get('to_do', {}).get('rich_text', []))
                checked = block.get('to_do', {}).get('checked', False)
                checkbox = "☑️" if checked else "☐"
                if text.strip():
                    formatted_text += f"{checkbox} {text}\n"
            
            elif block_type == 'code':
                code_block = block.get('code', {})
                text = self._extract_rich_text(code_block.get('rich_text', []))
                language = code_block.get('language', 'plain')
                if text.strip():
                    formatted_text += f"```{language}\n{text}\n```\n\n"
        
        return formatted_text or "No content found."
    
    def _extract_rich_text(self, rich_text_list: list) -> str:
        """Extract plain text from Notion rich text format."""
        text = ""
        for item in rich_text_list:
            if 'text' in item:
                text += item['text']['content']
        return text


def check_server_connection(server_url: str) -> bool:
    """Check if the tool recommendation server is available."""
    try:
        client = ToolRecommendationClient(server_url)
        return client.health_check()
    except Exception:
        return False


def setup_sidebar():
    """Setup the sidebar with server status and tools info."""
    with st.sidebar:
        st.header("🔧 Tool Recommendation System")
        
        # Server connection settings
        st.subheader("🔗 Server Connection")
        server_url = st.text_input(
            "Server URL", 
            value="http://localhost:8947",
            help="URL of the Tool Recommendation MCP Server"
        )
        
        # Connection status
        if st.button("🔄 Check Connection") or st.session_state.server_status == "unknown":
            with st.spinner("Checking server connection..."):
                is_connected = check_server_connection(server_url)
                
            if is_connected:
                st.session_state.server_status = "connected"
                st.session_state.tool_client = StreamlitToolClient(server_url)
                
                # Get available tools
                try:
                    tools_info = st.session_state.tool_client.client.list_tools()
                    st.session_state.available_tools = tools_info.get("tools", {})
                except Exception as e:
                    st.warning(f"Could not get tools list: {e}")
                
            else:
                st.session_state.server_status = "disconnected"
                st.session_state.tool_client = None
        
        # Show connection status
        if st.session_state.server_status == "connected":
            st.success("✅ Connected to Tool Recommendation Server")
        elif st.session_state.server_status == "disconnected":
            st.error("❌ Cannot connect to server")
            st.info("Make sure the Docker container is running:\n```\nmake run\n```")
        else:
            st.info("🔄 Connection status unknown")
        
        # Notion Integration Section
        st.markdown("---")
        st.subheader("📝 Notion Integration")
        
        # Notion API Key input
        notion_api_key = st.text_input(
            "Notion API Key",
            type="password",
            value=st.session_state.notion_config["api_key"],
            help="Your Notion API integration token"
        )
        
        # Notion Page ID input
        notion_page_id = st.text_input(
            "Default Page ID",
            value=st.session_state.notion_config["page_id"],
            help="Default Notion page ID to work with"
        )
        
        # Update config
        st.session_state.notion_config["api_key"] = notion_api_key
        st.session_state.notion_config["page_id"] = notion_page_id
        
        # Test Notion connection
        if st.button("🔄 Test Notion Connection"):
            if notion_api_key:
                with st.spinner("Testing Notion connection..."):
                    notion_client = NotionClient(notion_api_key)
                    is_connected = notion_client.test_connection()
                    
                    if is_connected:
                        st.session_state.notion_config["connected"] = True
                        st.session_state.notion_enabled = True
                        st.success("✅ Connected to Notion!")
                    else:
                        st.session_state.notion_config["connected"] = False
                        st.session_state.notion_enabled = False
                        st.error("❌ Failed to connect to Notion")
            else:
                st.warning("Please enter your Notion API key first")
        
        # Show Notion status
        if st.session_state.notion_config["connected"]:
            st.success("✅ Notion Connected")
            
            # Quick Notion actions
            if st.button("📖 Read Default Page"):
                if notion_page_id:
                    notion_client = NotionClient(notion_api_key)
                    page_data = notion_client.read_page(notion_page_id)
                    formatted_content = notion_client.format_page_content(page_data)
                    
                    # Add to chat messages
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": f"📝 **Notion Page Content**\n\n{formatted_content}"
                    })
                    st.rerun()
                else:
                    st.warning("Please enter a page ID first")
        
        elif notion_api_key:
            st.info("🔄 Notion connection not tested")
        else:
            st.info("Enter API key to connect to Notion")
        
        # Show available tools
        if st.session_state.available_tools:
            st.subheader("🛠️ Available Tools")
            with st.expander("Tool Categories", expanded=False):
                
                tool_categories = {
                    "🔍 Search & Analysis": [
                        "search_tools", "analyze_tools", "get_installation_guide"
                    ],
                    "🌐 Web & GitHub": [
                        "search_web", "search_github_repositories", "get_repository_structure"
                    ],
                    "🐍 Python & Code": [
                        "python_repl", "data_visualization", "analyze_repository"
                    ],
                    "🗃️ Database": [
                        "natural_language_query", "execute_sql_query"
                    ],
                    "🤖 AI Search": [
                        "perplexity_search"
                    ]
                }
                
                for category, tools in tool_categories.items():
                    st.write(f"**{category}**")
                    available_in_category = [
                        tool for tool in tools 
                        if tool in st.session_state.available_tools
                    ]
                    if available_in_category:
                        for tool in available_in_category:
                            st.write(f"  • {tool}")
                    else:
                        st.write("  • No tools available")
        
        # Activity monitoring
        if st.session_state.tool_client:
            st.subheader("📊 Activity Monitor")
            if st.button("📈 View Activity"):
                try:
                    activity = st.session_state.tool_client.client.get_activity_status()
                    
                    if activity.get("current_activity"):
                        current = activity["current_activity"]
                        st.write("**Current Activity:**")
                        st.write(f"🔧 {current.get('action', 'Unknown')}")
                        st.progress(current.get('progress', 0.0))
                    
                    if activity.get("recent_activities"):
                        st.write("**Recent Activities:**")
                        for act in activity["recent_activities"][-3:]:
                            st.write(f"• {act.get('action', 'Unknown')} ({act.get('status', 'unknown')})")
                    
                    if activity.get("resource_usage"):
                        resources = activity["resource_usage"]
                        api_calls = resources.get("api_calls", {})
                        if any(api_calls.values()):
                            st.write("**API Usage:**")
                            for api, count in api_calls.items():
                                if count > 0:
                                    st.write(f"• {api}: {count} calls")
                
                except Exception as e:
                    st.error(f"Could not get activity status: {e}")


def display_welcome_message():
    """Display a welcome message with usage instructions."""
    st.markdown("""
    # 🤖 AI Tool Recommendation Chatbot with Notion Integration
    
    Welcome! I'm your AI assistant for finding and analyzing development tools, plus I can help you work with your Notion documents. I can help you with:
    
    ### 🔍 **Tool Discovery**
    - Find tools for any development task
    - Get AI-powered analysis and recommendations
    - Compare different tools and frameworks
    
    ### 📚 **Installation & Setup**
    - Get step-by-step installation guides
    - Platform-specific instructions (Linux, Windows, macOS)
    - Troubleshooting common issues
    
    ### 🐙 **GitHub Integration**
    - Search GitHub repositories
    - Analyze code quality and structure
    - Explore repository contents
    
    ### 🐍 **Code Execution**
    - Run Python code snippets
    - Create data visualizations
    - Test code examples
    
    ### � **Notion Integration**
    - Read and analyze your Notion pages
    - Search through your documentation
    - Get insights from your notes and knowledge base
    
    ### �💬 **Example Questions**
    Try asking me:
    - "Find me the best Python web frameworks"
    - "How do I install Docker on Ubuntu?"
    - "Show me popular React component libraries"
    - "Analyze the FastAPI repository on GitHub"
    - "Read my Notion page about project planning"
    - "Search my Notion workspace for API documentation"
    
    ---
    **💡 Tips:** 
    - Be specific about your requirements for better recommendations!
    - Set up your Notion integration in the sidebar to access your documents
    - Use the quick action buttons below for common tasks
    """)


def process_user_message(message: str) -> str:
    """Process user message and get response from tool recommendation system or Notion."""
    # Check if this is a Notion-related query
    notion_keywords = ['notion', 'page', 'document', 'note', 'read page', 'notion page']
    is_notion_query = any(keyword in message.lower() for keyword in notion_keywords)
    
    if is_notion_query and st.session_state.notion_enabled:
        return process_notion_query(message)
    
    # Regular tool recommendation processing
    if not st.session_state.tool_client:
        return "❌ Tool Recommendation Server is not connected. Please check the connection in the sidebar."
    
    try:
        # Use the streamlit-optimized client
        response = st.session_state.tool_client.get_tool_recommendation(message)
        return response
    except Exception as e:
        return f"❌ Error processing your request: {str(e)}"


def process_notion_query(message: str) -> str:
    """Process Notion-specific queries."""
    if not st.session_state.notion_config["connected"]:
        return "❌ Notion is not connected. Please configure your Notion API key in the sidebar."
    
    api_key = st.session_state.notion_config["api_key"]
    page_id = st.session_state.notion_config["page_id"]
    
    notion_client = NotionClient(api_key)
    
    # Simple keyword matching for different actions
    message_lower = message.lower()
    
    if any(keyword in message_lower for keyword in ['read', 'show', 'get', 'fetch']):
        if 'page' in message_lower and page_id:
            page_data = notion_client.read_page(page_id)
            return notion_client.format_page_content(page_data)
        else:
            return "Please specify a page ID or set a default page ID in the sidebar."
    
    else:
        return f"🤖 I can help you with Notion! Try asking me to:\n\n" \
               f"• 'Read my Notion page'\n" \
               f"• 'Show me the content of page [ID]'\n" \
               f"• 'Get my Notion documentation'\n\n" \
               f"Your current default page ID: {page_id or 'Not set'}"


def format_message(content: str, role: str) -> None:
    """Format and display a chat message."""
    with st.chat_message(role):
        if role == "assistant":
            # Format assistant messages with better styling
            lines = content.split('\n')
            formatted_content = ""
            
            for line in lines:
                if line.startswith('###'):
                    formatted_content += f"\n{line}\n"
                elif line.startswith('-') or line.startswith('•'):
                    formatted_content += f"{line}\n"
                elif line.startswith('http'):
                    formatted_content += f"🔗 [{line}]({line})\n"
                else:
                    formatted_content += f"{line}\n"
            
            st.markdown(formatted_content)
        else:
            st.markdown(content)


def main():
    """Main application function."""
    st.set_page_config(
        page_title="AI Tool Recommendation Chatbot",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Setup sidebar
    setup_sidebar()
    
    # Main chat interface
    if not st.session_state.messages:
        display_welcome_message()
    
    # Display chat history
    for message in st.session_state.messages:
        format_message(message["content"], message["role"])
    
    # Chat input
    if prompt := st.chat_input("What tools are you looking for?"):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        format_message(prompt, "user")
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            if st.session_state.server_status != "connected":
                response = "❌ Please connect to the Tool Recommendation Server first (check the sidebar)."
                st.markdown(response)
            else:
                with st.spinner("🤖 Analyzing your request..."):
                    response = process_user_message(prompt)
                
                # Format and display response
                format_message(response, "assistant")
            
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Quick action buttons
    if st.session_state.server_status == "connected" or st.session_state.notion_enabled:
        st.markdown("---")
        st.subheader("🚀 Quick Actions")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 Popular Web Frameworks"):
                quick_message = "Show me the most popular web development frameworks in 2024"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
        
        with col2:
            if st.button("🐍 Python Data Tools"):
                quick_message = "Find me the best Python tools for data analysis and visualization"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
        
        with col3:
            if st.session_state.notion_enabled and st.button("📝 Read Notion Page"):
                quick_message = "Read my Notion page"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
            elif st.button("🔒 Security Tools"):
                quick_message = "Recommend cybersecurity tools for vulnerability scanning"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
        
        with col4:
            if st.button("🤖 AI/ML Frameworks"):
                quick_message = "What are the best machine learning frameworks for beginners?"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
        
        # Additional Notion quick actions if enabled
        if st.session_state.notion_enabled:
            st.markdown("#### 📝 Notion Quick Actions")
            col5, col6, col7, col8 = st.columns(4)
            
            with col5:
                if st.button("📋 Notion Help"):
                    quick_message = "How can you help me with my Notion documents?"
                    st.session_state.messages.append({"role": "user", "content": quick_message})
                    st.rerun()
            
            with col6:
                if st.button("🔍 Search Docs"):
                    quick_message = "How can I search through my Notion documentation?"
                    st.session_state.messages.append({"role": "user", "content": quick_message})
                    st.rerun()
            
            with col7:
                if st.button("📊 Page Analysis"):
                    quick_message = "Analyze the content of my Notion page"
                    st.session_state.messages.append({"role": "user", "content": quick_message})
                    st.rerun()
            
            with col8:
                if st.button("💡 Notion Tips"):
                    quick_message = "Give me tips for organizing my Notion workspace"
                    st.session_state.messages.append({"role": "user", "content": quick_message})
                    st.rerun()
    
    # Footer
    st.markdown("---")
    server_status_icon = '✅' if st.session_state.server_status == 'connected' else '❌'
    notion_status_icon = '✅' if st.session_state.notion_enabled else '❌'
    
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🔧 Powered by AI Tool Recommendation System & Notion Integration | "
        f"Tools: {server_status_icon} | Notion: {notion_status_icon}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
