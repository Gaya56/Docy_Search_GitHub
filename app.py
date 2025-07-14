"""
AI Tool Assistant - OpenAI Powered Chatbot
An intelligent chatbot that uses OpenAI to understand user queries and execute the appropriate tools.
"""

import streamlit as st
import requests
import json
import os
from typing import Dict, Any, List
from openai import OpenAI


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "server_status" not in st.session_state:
        st.session_state.server_status = "unknown"
    
    if "available_tools" not in st.session_state:
        st.session_state.available_tools = {}
    
    if "mcp_servers" not in st.session_state:
        st.session_state.mcp_servers = {}
    
    if "selected_mcp_server" not in st.session_state:
        st.session_state.selected_mcp_server = None
    
    if "selected_tool" not in st.session_state:
        st.session_state.selected_tool = None
    
    if "openai_client" not in st.session_state:
        st.session_state.openai_client = None
    
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = ""
    
    if "notion_api_key" not in st.session_state:
        st.session_state.notion_api_key = ""
    
    if "notion_page_id" not in st.session_state:
        st.session_state.notion_page_id = ""


def check_server_connection(server_url: str) -> bool:
    """Check if the tool recommendation server is available."""
    try:
        response = requests.get(f"{server_url}/health", timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def get_mcp_servers(server_url: str) -> Dict[str, Any]:
    """Get list of available MCP servers from the server."""
    try:
        response = requests.get(f"{server_url}/mcp-servers", timeout=10)
        if response.status_code == 200:
            return response.json().get("servers", {})
    except Exception:
        pass
    return {}


def get_server_tools(server_url: str, server_name: str) -> Dict[str, Any]:
    """Get tools for a specific MCP server."""
    try:
        response = requests.get(f"{server_url}/mcp-servers/{server_name}/tools", timeout=10)
        if response.status_code == 200:
            return response.json().get("tools", {})
    except Exception:
        pass
    return {}


def get_available_tools(server_url: str) -> Dict[str, Any]:
    """Get list of available tools from the server."""
    try:
        response = requests.get(f"{server_url}/tools", timeout=10)
        if response.status_code == 200:
            return response.json().get("tools", {})
    except Exception:
        pass
    return {}


def execute_tool_on_server(tool_name: str, parameters: Dict[str, Any], server_url: str) -> str:
    """Execute a tool on the server with given parameters."""
    try:
        payload = {
            "tool_name": tool_name,
            "parameters": parameters
        }
        
        # Add Notion credentials for Notion tools
        if tool_name.startswith('notion_') or 'notion' in tool_name.lower():
            notion_api_key = st.session_state.get("notion_api_key")
            notion_page_id = st.session_state.get("notion_page_id")
            
            if notion_api_key:
                payload["notion_api_key"] = notion_api_key
            
            # If no page_id in parameters but we have a default one, use it
            if notion_page_id and "page_id" not in parameters:
                parameters["page_id"] = notion_page_id
                payload["parameters"] = parameters
            
            if notion_page_id:
                payload["notion_page_id"] = notion_page_id
        
        response = requests.post(
            f"{server_url}/execute",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("result", "No result returned")
        else:
            return f"Error executing tool: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"


def create_openai_function_definitions(available_tools: Dict[str, Any]) -> List[Dict]:
    """Create OpenAI function definitions from available tools."""
    # Check if we have a default Notion page ID configured
    has_default_page_id = bool(st.session_state.get("notion_page_id"))
    
    function_definitions = {
        "search_tools": {
            "name": "search_tools",
            "description": "Search for development tools and frameworks based on a query",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for tools"
                    }
                },
                "required": ["query"]
            }
        },
        "analyze_tools": {
            "name": "analyze_tools",
            "description": "Analyze specific tools or frameworks",
            "parameters": {
                "type": "object",
                "properties": {
                    "tools": {
                        "type": "string",
                        "description": "Tools to analyze"
                    }
                },
                "required": ["tools"]
            }
        },
        "quick_repo_summary": {
            "name": "quick_repo_summary",
            "description": "Get a quick summary of a GitHub repository",
            "parameters": {
                "type": "object",
                "properties": {
                    "repo_url": {
                        "type": "string",
                        "description": "GitHub repository URL"
                    }
                },
                "required": ["repo_url"]
            }
        },
        "get_installation_guide": {
            "name": "get_installation_guide",
            "description": "Get installation instructions for a tool",
            "parameters": {
                "type": "object",
                "properties": {
                    "tool_name": {
                        "type": "string",
                        "description": "Name of the tool"
                    }
                },
                "required": ["tool_name"]
            }
        },
        "read_notion_page": {
            "name": "read_notion_page",
            "description": "Read content from a Notion page" + (" (uses default page if none specified)" if has_default_page_id else ""),
            "parameters": {
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "Notion page ID to read from" + (" (optional, uses default if not provided)" if has_default_page_id else "")
                    }
                },
                "required": [] if has_default_page_id else ["page_id"]
            }
        },
        "search_notion_page": {
            "name": "search_notion_page",
            "description": "Search for content within Notion pages" + (" (uses default page if none specified)" if has_default_page_id else ""),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query to find in Notion"
                    },
                    "page_id": {
                        "type": "string",
                        "description": "Notion page ID to search in" + (" (optional, uses default if not provided)" if has_default_page_id else "")
                    }
                },
                "required": ["query"] + ([] if has_default_page_id else ["page_id"])
            }
        },
        "add_to_notion_page": {
            "name": "add_to_notion_page",
            "description": "Add content to a Notion page" + (" (uses default page if none specified)" if has_default_page_id else ""),
            "parameters": {
                "type": "object",
                "properties": {
                    "page_id": {
                        "type": "string",
                        "description": "Notion page ID to add content to" + (" (optional, uses default if not provided)" if has_default_page_id else "")
                    },
                    "content": {
                        "type": "string",
                        "description": "Content to add to the page"
                    }
                },
                "required": ["content"] + ([] if has_default_page_id else ["page_id"])
            }
        }
    }
    
    return [func_def for tool_name, func_def in function_definitions.items() 
            if tool_name in available_tools]


def chat_with_openai(user_message: str, available_tools: Dict[str, Any], openai_client) -> str:
    """Chat with OpenAI and let it decide which tools to use."""
    try:
        functions = create_openai_function_definitions(available_tools)
        
        system_message = """You are an AI assistant that helps users with development tools and technology questions.

When a user asks a question:
1. Analyze what they're asking for
2. Choose the most appropriate tool to answer their question
3. Call the tool with appropriate parameters
4. Provide a helpful response based on the tool results

Available tools:
- search_tools: Find development tools and frameworks
- analyze_tools: Get detailed analysis of specific tools
- quick_repo_summary: Get repo overview
- get_installation_guide: Get installation instructions"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=[{"type": "function", "function": func} for func in functions],
            tool_choice="auto",
            temperature=0.7
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute the tool on our server
            tool_result = execute_tool_on_server(function_name, function_args, "http://localhost:8947")
            
            # Add assistant message with tool call
            messages.append({
                "role": "assistant", 
                "content": "",  # Always use empty string instead of None
                "tool_calls": message.tool_calls
            })
            
            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })
            
            # Get final response
            final_response = openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7
            )
            
            return final_response.choices[0].message.content
        else:
            return message.content
            
    except Exception as e:
        return f"❌ Error in OpenAI chat: {str(e)}"


def setup_sidebar():
    """Setup the sidebar with configuration."""
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # OpenAI API Key
        st.subheader("🤖 OpenAI Configuration")
        openai_api_key = st.text_input(
            "OpenAI API Key", 
            type="password",
            value=st.session_state.openai_api_key,
            help="Enter your OpenAI API key"
        )
        
        if openai_api_key:
            st.session_state.openai_api_key = openai_api_key
            try:
                st.session_state.openai_client = OpenAI(api_key=openai_api_key)
                st.success("✅ OpenAI API Key Set")
            except Exception as e:
                st.error(f"❌ Invalid OpenAI API Key: {e}")
        else:
            st.warning("⚠️ Please enter your OpenAI API Key")
        
        # Server connection
        st.subheader("🔗 Tool Server Connection")
        server_url = st.text_input(
            "Server URL", 
            value="http://localhost:8947",
            help="URL of the Tool Recommendation Server"
        )
        
        if st.button("🔄 Connect to Tool Server"):
            with st.spinner("Connecting to server and loading tools..."):
                is_connected = check_server_connection(server_url)
                
                if is_connected:
                    st.session_state.server_status = "connected"
                    tools = get_available_tools(server_url)
                    st.session_state.available_tools = tools
                    
                    # Load MCP servers
                    mcp_servers = get_mcp_servers(server_url)
                    st.session_state.mcp_servers = mcp_servers
                    
                    st.success("✅ Connected to server!")
                    st.success(f"📋 Loaded {len(tools)} tools")
                    st.success(f"🖥️ Found {len(mcp_servers)} MCP servers")
                else:
                    st.session_state.server_status = "disconnected"
                    st.error("❌ Cannot connect to server")
        
        # MCP Server Selection
        st.subheader("🖥️ MCP Server Selection")
        
        if st.session_state.mcp_servers:
            server_names = list(st.session_state.mcp_servers.keys())
            selected_server = st.selectbox(
                "Choose MCP Server",
                options=[""] + server_names,
                index=0 if not st.session_state.selected_mcp_server else 
                      server_names.index(st.session_state.selected_mcp_server) + 1 if st.session_state.selected_mcp_server in server_names else 0,
                key="mcp_server_selector"
            )
            
            if selected_server and selected_server != st.session_state.selected_mcp_server:
                st.session_state.selected_mcp_server = selected_server
                st.session_state.selected_tool = None  # Reset tool selection
                st.rerun()
            
            # Show server info
            if selected_server:
                server_info = st.session_state.mcp_servers.get(selected_server, {})
                st.info(f"📊 {server_info.get('tool_count', 0)} tools available")
                
                # Show tools for selected server
                with st.expander(f"🛠️ Tools in {selected_server}"):
                    for tool_name in server_info.get('tools', []):
                        st.write(f"• {tool_name}")
        else:
            st.warning("⚠️ Connect to server first to see MCP servers")
        
        # Notion Configuration
        st.subheader("📝 Notion Configuration")
        
        notion_api_key = st.text_input(
            "Notion API Key",
            type="password",
            value=st.session_state.get("notion_api_key", ""),
            help="Enter your Notion API key (integration token)",
            key="notion_api_key_input"
        )
        
        notion_page_id = st.text_input(
            "Default Notion Page ID",
            value=st.session_state.get("notion_page_id", ""),
            help="Enter the default Notion page ID for operations",
            key="notion_page_id_input"
        )
        
        # Update session state when values change
        if notion_api_key:
            st.session_state.notion_api_key = notion_api_key
            # Set environment variable for the tool server to use
            os.environ["NOTION_API_KEY"] = notion_api_key
            st.success("✅ Notion API Key Set")
        else:
            st.warning("⚠️ Notion API key not set (optional)")
            
        if notion_page_id:
            st.session_state.notion_page_id = notion_page_id
            # Set environment variable for the tool server to use
            os.environ["NOTION_PAGE_ID"] = notion_page_id
            st.success("✅ Notion Page ID Set")
        else:
            st.warning("⚠️ Notion page ID not set (optional)")
        
        # Status indicators
        st.markdown("---")
        st.subheader("📊 Status")
        
        if st.session_state.openai_client:
            st.success("✅ OpenAI: Connected")
        else:
            st.error("❌ OpenAI: Not configured")
        
        if st.session_state.server_status == "connected":
            st.success(f"✅ Tools: Connected ({len(st.session_state.available_tools)} available)")
        else:
            st.error("❌ Tools: Not connected")
            
        # Notion status
        if st.session_state.get("notion_api_key"):
            if st.session_state.get("notion_page_id"):
                st.success("✅ Notion: Fully configured")
            else:
                st.warning("⚠️ Notion: API key set, page ID missing")
        else:
            st.info("ℹ️ Notion: Not configured (optional)")
        
        if st.session_state.available_tools:
            with st.expander("🛠️ Available Tools"):
                for tool_name in st.session_state.available_tools.keys():
                    st.write(f"• {tool_name}")


def display_tool_selector():
    """Display tool selection interface."""
    if not st.session_state.selected_mcp_server:
        st.info("👆 Select an MCP server from the sidebar to see available tools")
        return None
    
    server_name = st.session_state.selected_mcp_server
    server_info = st.session_state.mcp_servers.get(server_name, {})
    available_tools = server_info.get('tools', [])
    
    if not available_tools:
        st.warning(f"No tools available for {server_name}")
        return None
    
    # Create tool selection interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_tool = st.selectbox(
            f"Choose a tool from {server_name}",
            options=[""] + available_tools,
            index=0 if not st.session_state.selected_tool else 
                  available_tools.index(st.session_state.selected_tool) + 1 if st.session_state.selected_tool in available_tools else 0,
            key="tool_selector"
        )
    
    with col2:
        if selected_tool:
            if st.button("🚀 Use Tool", key="use_tool_button"):
                st.session_state.selected_tool = selected_tool
                return selected_tool
    
    if selected_tool and selected_tool != st.session_state.selected_tool:
        st.session_state.selected_tool = selected_tool
    
    return selected_tool


def execute_selected_tool(tool_name: str, user_input: str) -> str:
    """Execute a selected tool with user input as parameters."""
    try:
        # Parse user input to extract parameters
        # For now, we'll use a simple approach - let OpenAI help us parse the input
        parameters = parse_tool_parameters(tool_name, user_input)
        
        # Execute the tool on our server
        result = execute_tool_on_server(tool_name, parameters, "http://localhost:8947")
        
        return f"**Tool:** {tool_name}\n**Result:**\n{result}"
        
    except Exception as e:
        return f"❌ Error executing tool '{tool_name}': {str(e)}"


def parse_tool_parameters(tool_name: str, user_input: str) -> Dict[str, Any]:
    """Parse user input into tool parameters using OpenAI."""
    try:
        if not st.session_state.openai_client:
            # Fallback: simple parameter parsing
            return {"query": user_input} if "query" in get_tool_parameter_names(tool_name) else {}
        
        # Define expected parameters for each tool
        tool_params = get_tool_parameter_names(tool_name)
        
        if not tool_params:
            return {}
        
        # Use OpenAI to parse the input
        system_message = f"""You are a parameter parser. Extract parameters from user input for the tool '{tool_name}'.
        
Expected parameters: {', '.join(tool_params)}

Return only a JSON object with the extracted parameters. If a parameter is not found, omit it.
Examples:
- For "search for python web frameworks": {{"query": "python web frameworks"}}
- For "analyze React repository": {{"query": "React", "tools": "React"}}
"""
        
        response = st.session_state.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            temperature=0.1
        )
        
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # Fallback to simple parsing
            return {"query": user_input} if "query" in tool_params else {}
            
    except Exception:
        # Fallback to simple parsing
        return {"query": user_input}


def get_tool_parameter_names(tool_name: str) -> List[str]:
    """Get expected parameter names for a tool."""
    tool_parameters = {
        "search_tools": ["query", "category"],
        "analyze_tools": ["tools"],
        "get_installation_guide": ["tool_name"],
        "compare_tools": ["tools"],
        "search_web": ["query"],
        "perplexity_search": ["query"],
        "search_github_repositories": ["query", "language", "limit"],
        "get_repository_structure": ["repo_url"],
        "get_file_from_repository": ["repo_url", "file_path"],
        "analyze_repository": ["repo_url"],
        "quick_repo_summary": ["repo_url"],
        "natural_language_query": ["query"],
        "get_database_schema": [],
        "read_notion_page": ["page_id"],
        "search_notion_page": ["query", "page_id"],
        "add_to_notion_page": ["page_id", "content"],
    }
    return tool_parameters.get(tool_name, ["query"])


def display_chat_interface():
    """Display the main chat interface."""
    st.header("🤖 AI Tool Assistant")
    st.markdown("*Powered by OpenAI GPT-4 with intelligent tool selection*")
    
    if not st.session_state.openai_client:
        st.warning("⚠️ Please configure your OpenAI API key in the sidebar first!")
        return
    
    if st.session_state.server_status != "connected":
        st.warning("⚠️ Please connect to the tool server in the sidebar first!")
        return
    
    # Display tool selector
    st.subheader("🛠️ Tool Selection")
    selected_tool = display_tool_selector()
    
    if selected_tool:
        st.success(f"✅ Selected tool: **{selected_tool}** from **{st.session_state.selected_mcp_server}**")
        
        # Show tool description if available
        server_tools = get_server_tools("http://localhost:8947", st.session_state.selected_mcp_server)
        if selected_tool in server_tools:
            tool_info = server_tools[selected_tool]
            st.info(f"📋 {tool_info.get('description', 'No description available')}")
    
    st.markdown("---")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input - only enabled when tool is selected
    if selected_tool:
        if prompt := st.chat_input(f"Enter parameters for {selected_tool}..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Execute the selected tool directly
            with st.chat_message("assistant"):
                with st.spinner(f"🔧 Executing {selected_tool}..."):
                    response = execute_selected_tool(selected_tool, prompt)
                
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
    else:
        st.text_input("Select a tool first to enable chat", disabled=True, key="disabled_chat")


def main():
    """Main application function."""
    st.set_page_config(
        page_title="AI Tool Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    setup_sidebar()
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        display_chat_interface()
    
    with col2:
        st.subheader("ℹ️ How It Works")
        st.markdown("""
        **1.** Configure OpenAI API key
        
        **2.** Connect to tool server
        
        **3.** Select an MCP server (e.g., GitHub, Notion)
        
        **4.** Choose a specific tool from that server
        
        **5.** Enter parameters and execute!
        """)
        
        st.markdown("---")
        st.subheader("💡 Example Usage")
        st.markdown("""
        **GitHub MCP Server:**
        • search_github_repositories: "python web frameworks"
        • quick_repo_summary: "https://github.com/user/repo"
        
        **Notion MCP Server:**
        • read_notion_page: (uses default page)
        • search_notion_page: "machine learning"
        
        **Tool Recommendation:**
        • search_tools: "docker alternatives"
        • analyze_tools: "React vs Vue"
        """)
        
        # Show selected tool info
        if st.session_state.selected_mcp_server and st.session_state.selected_tool:
            st.markdown("---")
            st.subheader("🎯 Current Selection")
            st.success(f"**Server:** {st.session_state.selected_mcp_server}")
            st.success(f"**Tool:** {st.session_state.selected_tool}")
            
            # Show expected parameters
            expected_params = get_tool_parameter_names(st.session_state.selected_tool)
            if expected_params:
                st.info(f"**Expected parameters:** {', '.join(expected_params)}")
    
    # Footer
    st.markdown("---")
    openai_status = "✅" if st.session_state.openai_client else "❌"
    server_status = "✅" if st.session_state.server_status == "connected" else "❌"
    mcp_server = st.session_state.selected_mcp_server or "None"
    selected_tool = st.session_state.selected_tool or "None"
    
    st.markdown(
        f"<div style='text-align: center; color: #666;'>"
        f"🤖 AI Tool Assistant | OpenAI: {openai_status} | Tools: {server_status} | "
        f"MCP Server: {mcp_server} | Tool: {selected_tool} | Port: 8947"
        f"</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
