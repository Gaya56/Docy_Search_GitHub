"""
Complete Streamlit Chatbot Example with Tool Recommendation Integration

This example shows how to integrate the Tool Recommendation Container
into a full-featured Streamlit chatbot application.
"""

import streamlit as st

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
            value="http://localhost:8000",
            help="URL of the Tool Recommendation Container"
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
    # 🤖 AI Tool Recommendation Chatbot
    
    Welcome! I'm your AI assistant for finding and analyzing development tools. I can help you with:
    
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
    
    ### 💬 **Example Questions**
    Try asking me:
    - "Find me the best Python web frameworks"
    - "How do I install Docker on Ubuntu?"
    - "Show me popular React component libraries"
    - "Analyze the FastAPI repository on GitHub"
    - "Create a bar chart of sales data"
    
    ---
    **💡 Tip:** Be specific about your requirements for better recommendations!
    """)


def process_user_message(message: str) -> str:
    """Process user message and get response from tool recommendation system."""
    if not st.session_state.tool_client:
        return "❌ Tool Recommendation Server is not connected. Please check the connection in the sidebar."
    
    try:
        # Use the streamlit-optimized client
        response = st.session_state.tool_client.get_tool_recommendation(message)
        return response
    except Exception as e:
        return f"❌ Error processing your request: {str(e)}"


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
    if st.session_state.server_status == "connected":
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
            if st.button("🔒 Security Tools"):
                quick_message = "Recommend cybersecurity tools for vulnerability scanning"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
        
        with col4:
            if st.button("🤖 AI/ML Frameworks"):
                quick_message = "What are the best machine learning frameworks for beginners?"
                st.session_state.messages.append({"role": "user", "content": quick_message})
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "🔧 Powered by AI Tool Recommendation System | "
        f"Connected: {'✅' if st.session_state.server_status == 'connected' else '❌'}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
