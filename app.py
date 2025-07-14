"""
AI Tool Assistant - Streamlit Application
Select a tool from the sidebar, then ask questions to execute that specific tool.
"""

import streamlit as st
import requests
import json
from typing import Dict, Any

def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "server_status" not in st.session_state:
        st.session_state.server_status = "unknown"
    
    if "available_tools" not in st.session_state:
        st.session_state.available_tools = {}
    
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = None


def check_server_connection(server_url: str) -> bool:
    """Check if the tool recommendation server is available."""
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def get_available_tools(server_url: str) -> Dict[str, Any]:
    """Get list of available tools from the server."""
    try:
        response = requests.get(f"{server_url}/tools", timeout=10)
        if response.status_code == 200:
            return response.json().get("tools", {})
    except Exception:
        pass
    return {}


def execute_selected_tool(tool_name: str, user_input: str, server_url: str) -> str:
    """Execute the selected tool with user input."""
    try:
        # Map user input to appropriate tool parameters
        tool_params = map_input_to_tool_params(tool_name, user_input)
        
        payload = {
            "tool_name": tool_name,
            "parameters": tool_params
        }
        
        response = requests.post(
            f"{server_url}/execute",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("result", "No result returned")
        else:
            return f"❌ Error executing tool: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"❌ Error: {str(e)}"


def map_input_to_tool_params(tool_name: str, user_input: str) -> Dict[str, Any]:
    """Map user input to appropriate tool parameters based on the tool."""
    
    # Define parameter mappings for each tool
    tool_param_map = {
        "search_tools": {"query": user_input},
        "analyze_tools": {"tools": user_input},
        "compare_tools": {"tools": user_input.split(",") if "," in user_input else [user_input]},
        "get_installation_guide": {"tool_name": user_input},
        "search_web": {"query": user_input},
        "search_github_repositories": {"query": user_input},
        "get_repository_structure": {"repo_url": user_input},
        "analyze_repository": {"repo_url": user_input},
        "quick_repo_summary": {"repo_url": user_input},
        "get_file_from_repository": {"repo_url": user_input.split()[0] if " " in user_input else user_input,
                                    "file_path": user_input.split()[1] if " " in user_input else ""},
        "perplexity_search": {"query": user_input},
        "natural_language_query": {"query": user_input},
        "get_database_schema": {}  # No parameters needed
    }
    
    return tool_param_map.get(tool_name, {"input": user_input})


def setup_sidebar():
    """Setup the sidebar with tool selection and server status."""
    with st.sidebar:
        st.header("🔧 Tool Selection & Configuration")
        
        # Server connection
        st.subheader("🔗 Server Connection")
        server_url = st.text_input(
            "Server URL", 
            value="http://localhost:8947",
            help="URL of the Tool Recommendation Server"
        )
        
        # Check connection and get tools
        if st.button("🔄 Connect & Load Tools") or st.session_state.server_status == "unknown":
            with st.spinner("Connecting to server and loading tools..."):
                is_connected = check_server_connection(server_url)
                
                if is_connected:
                    st.session_state.server_status = "connected"
                    
                    # Get available tools
                    tools = get_available_tools(server_url)
                    st.session_state.available_tools = tools
                    
                    st.success("✅ Connected to server!")
                    st.success(f"📋 Loaded {len(tools)} tools")
                    
                else:
                    st.session_state.server_status = "disconnected"
                    st.error("❌ Cannot connect to server")
        
        # Tool Selection
        if st.session_state.server_status == "connected" and st.session_state.available_tools:
            st.subheader("🛠️ Select Tool")
            
            # Create tool categories for better organization
            tool_categories = {
                "🔍 Search & Discovery": ["search_tools", "search_web", "search_github_repositories"],
                "🔬 Analysis": ["analyze_tools", "analyze_repository", "compare_tools"],
                "📚 Information": ["get_installation_guide", "quick_repo_summary", "get_repository_structure"],
                "🗃️ Repository": ["get_file_from_repository"],
                "🤖 AI Search": ["perplexity_search"],
                "💾 Database": ["natural_language_query", "get_database_schema"]
            }
            
            # Tool selection dropdown
            all_tools = list(st.session_state.available_tools.keys())
            
            selected_tool = st.selectbox(
                "Choose a tool to use:",
                options=["None"] + all_tools,
                index=0 if st.session_state.selected_tool is None else all_tools.index(st.session_state.selected_tool) + 1,
                help="Select the tool you want to use for your query"
            )
            
            if selected_tool != "None":
                st.session_state.selected_tool = selected_tool
                
                # Show tool description
                tool_info = st.session_state.available_tools.get(selected_tool, {})
                if tool_info.get("description"):
                    st.info(f"📝 **Tool Description:**\n{tool_info['description']}")
                
                # Show tool category
                for category, tools in tool_categories.items():
                    if selected_tool in tools:
                        st.success(f"📂 **Category:** {category}")
                        break
                
                # Show example usage
                examples = get_tool_examples(selected_tool)
                if examples:
                    st.markdown("💡 **Example inputs:**")
                    for example in examples:
                        st.code(example, language="text")
            else:
                st.session_state.selected_tool = None
        
        # Connection status
        if st.session_state.server_status == "connected":
            st.success(f"✅ Server Connected ({len(st.session_state.available_tools)} tools)")
        elif st.session_state.server_status == "disconnected":
            st.error("❌ Server Disconnected")
        else:
            st.info("🔄 Not connected - Click 'Connect & Load Tools'")


def get_tool_examples(tool_name: str) -> list:
    """Get example inputs for each tool."""
    examples = {
        "search_tools": [
            "Python web frameworks",
            "JavaScript testing libraries",
            "Machine learning frameworks"
        ],
        "analyze_tools": [
            "React, Vue, Angular",
            "Docker, Kubernetes",
            "FastAPI"
        ],
        "compare_tools": [
            "React, Vue, Angular",
            "PostgreSQL, MySQL, MongoDB"
        ],
        "get_installation_guide": [
            "Docker",
            "Node.js",
            "Python"
        ],
        "search_web": [
            "Best Python frameworks 2024",
            "How to deploy FastAPI"
        ],
        "search_github_repositories": [
            "FastAPI",
            "React components",
            "Python machine learning"
        ],
        "get_repository_structure": [
            "https://github.com/tiangolo/fastapi",
            "https://github.com/facebook/react"
        ],
        "analyze_repository": [
            "https://github.com/tiangolo/fastapi",
            "https://github.com/streamlit/streamlit"
        ],
        "quick_repo_summary": [
            "https://github.com/tiangolo/fastapi"
        ],
        "get_file_from_repository": [
            "https://github.com/tiangolo/fastapi README.md",
            "https://github.com/facebook/react package.json"
        ],
        "perplexity_search": [
            "Latest trends in web development",
            "Best practices for API design"
        ],
        "natural_language_query": [
            "Show me all Python tools",
            "What are the most popular frameworks?"
        ],
        "get_database_schema": [
            "(No input needed - shows database structure)"
        ]
    }
    
    return examples.get(tool_name, [])


def display_chat_interface():
    """Display the main chat interface."""
    st.header("🤖 AI Tool Assistant")
    
    if st.session_state.selected_tool:
        st.info(f"🔧 **Selected Tool:** {st.session_state.selected_tool}")
    else:
        st.warning("⚠️ Please select a tool from the sidebar first!")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about tools or enter your query for the selected tool..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate assistant response
        with st.chat_message("assistant"):
            if st.session_state.selected_tool and st.session_state.server_status == "connected":
                with st.spinner(f"🔄 Executing {st.session_state.selected_tool}..."):
                    response = execute_selected_tool(
                        st.session_state.selected_tool, 
                        prompt, 
                        "http://localhost:8947"
                    )
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            elif not st.session_state.selected_tool:
                response = "Please select a tool from the sidebar first, then ask your question!"
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            else:
                response = "Server not connected. Please connect to the server first."
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    """Main application function."""
    st.set_page_config(
        page_title="AI Tool Assistant",
        page_icon="🔧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Setup sidebar
    setup_sidebar()
    
    # Main content area
    col1, col2 = st.columns([3, 1])
    
    with col1:
        display_chat_interface()
    
    with col2:
        st.subheader("ℹ️ How to Use")
        st.markdown("""
        **Step 1:** Connect to server in sidebar
        
        **Step 2:** Select a tool from dropdown
        
        **Step 3:** Ask your question in chat
        
        **Step 4:** Bot executes selected tool!
        """)
        
        if st.session_state.selected_tool:
            st.success(f"✅ Ready to use: **{st.session_state.selected_tool}**")
        else:
            st.info("👈 Select a tool to get started")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        f"🔧 AI Tool Assistant | Server: {'✅' if st.session_state.server_status == 'connected' else '❌'} | "
        f"Selected Tool: {st.session_state.selected_tool or 'None'}"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
