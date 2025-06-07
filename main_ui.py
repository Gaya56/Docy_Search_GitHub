"""
Streamlit UI for Docy_Search with Memory System
Chat Tab Implementation with Live Activity Tracking
"""

import streamlit as st
import asyncio
import os
import sys
import uuid
import random
import json
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import activity tracking and cost tracking
from activity_tracker import activity_tracker
from memory.cost_tracker import CostTracker

# Import UI components
from ui.components.sidebar import SidebarComponent

# Import from existing app.py
from app import (
    load_project_context, 
    create_agent_with_context,
    get_model_from_name,
    model,
    memory_manager
)

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Docy Search Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .session-info {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .memory-indicator {
        padding: 0.5rem;
        border-radius: 5px;
        margin: 0.5rem 0;
    }
    .memory-active {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .memory-disabled {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
    }
    .live-indicator {
        color: #28a745;
        font-weight: bold;
    }
    .activity-refresh {
        font-size: 0.8em;
        color: #6c757d;
    }
    .tool-card {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.25rem 0;
    }
    .tool-card.selected {
        background-color: #d4edda;
        border-color: #c3e6cb;
    }
    .model-info {
        background-color: #e9ecef;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.85em;
    }
    .config-summary {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 6px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.8em;
    }
</style>""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    """Initialize all session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'user_id' not in st.session_state:
        # Load or create user session
        user_session_file = ".user_session"
        if os.path.exists(user_session_file):
            with open(user_session_file, 'r') as f:
                st.session_state.user_id = f.read().strip()
        else:
            st.session_state.user_id = str(uuid.uuid4())
            with open(user_session_file, 'w') as f:
                f.write(st.session_state.user_id)
    
    if 'project_context' not in st.session_state:
        st.session_state.project_context = load_project_context()
    
    # Initialize cost tracker
    if 'cost_tracker' not in st.session_state:
        st.session_state.cost_tracker = CostTracker()
    
    # Initialize auto-refresh tracking
    if 'last_activity_count' not in st.session_state:
        st.session_state.last_activity_count = 0
    
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    # Initialize async operation caches
    if 'daily_cost' not in st.session_state:
        st.session_state.daily_cost = 0.0
    
    if 'monthly_cost' not in st.session_state:
        st.session_state.monthly_cost = 0.0
    
    if 'memory_stats' not in st.session_state:
        st.session_state.memory_stats = {
            'total': 0, 'active': 0, 'compressed': 0, 'archived': 0
        }
    
    if 'maintenance_results' not in st.session_state:
        st.session_state.maintenance_results = {'compressed': 0, 'archived': 0}
    
    if 'cleared_count' not in st.session_state:
        st.session_state.cleared_count = 0
    
    # Initialize AI model selection
    if 'selected_ai_model' not in st.session_state:
        st.session_state.selected_ai_model = "openai"  # Default
    
    if 'previous_ai_model' not in st.session_state:
        st.session_state.previous_ai_model = st.session_state.selected_ai_model

# Load project context
@st.cache_data
def get_project_context():
    """Load and cache project context"""
    return load_project_context()

def display_sidebar():
    """Enhanced sidebar with live activity tracking"""
    sidebar = SidebarComponent(memory_manager, model)
    config_changes = sidebar.render()
    
    # Handle configuration changes
    if config_changes.get('tools_changed') or config_changes.get('model_changed'):
        # Clear cached agents
        for key in list(st.session_state.keys()):
            if isinstance(key, str) and key.startswith("agent_"):
                del st.session_state[key]

async def get_agent_response(prompt, conversation_context):
    """Get response from the agent with dynamic model switching"""
    try:
        # Get current model selection
        current_model = st.session_state.get('selected_ai_model', 'openai')
        
        # Create cache key based on model and selected tools
        selected_tools_list = [k for k, v in st.session_state.selected_tools.items() if v] if 'selected_tools' in st.session_state else []
        tools_hash = hash(tuple(sorted(selected_tools_list)))
        agent_cache_key = f"agent_{current_model}_{tools_hash}"
        
        # Create agent if not cached or model/tools changed
        if agent_cache_key not in st.session_state:
            # Clear any old agent cache when model or tools change
            for key in list(st.session_state.keys()):
                if isinstance(key, str) and key.startswith('agent_'):
                    del st.session_state[key]
            
            # Create new agent with selected model and tools
            st.session_state[agent_cache_key] = create_agent_with_context(
                st.session_state.project_context, 
                st.session_state.user_id,
                model_name=current_model,
                selected_tools=selected_tools_list  # Pass only enabled tools
            )
        
        agent = st.session_state[agent_cache_key]
        
        # Build full prompt with conversation context
        full_prompt = f"{conversation_context}\nCurrent message: {prompt}"
        
        # Run agent with MCP servers
        async with agent.run_mcp_servers():
            result = await agent.run(full_prompt)
            return result.output
    
    except Exception as e:
        st.error(f"Error getting response: {str(e)}")
        return f"I apologize, but I encountered an error: {str(e)}. Please try again."

def save_memory(prompt, response):
    """Save interaction to memory if conditions are met"""
    if not memory_manager or len(response) < 100:
        return False, None
    
    try:
        # Create memory content
        memory_content = f"User asked: {prompt[:200]}"
        if len(prompt) > 200:
            memory_content += "..."
        memory_content += f"\nAssistant provided: {response[:500]}"
        if len(response) > 500:
            memory_content += "..."
        
        # Save memory asynchronously using asyncio.run for Streamlit compatibility
        async def async_save():
            return await memory_manager.async_manager.save_memory(
                user_id=st.session_state.user_id,
                content=memory_content,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "user_input_length": len(prompt),
                    "response_length": len(response),
                    "category": "tool_recommendation",
                    "ui": "streamlit"
                },
                category="tool_recommendation"
            )
        
        # Run async operation in a way that's compatible with Streamlit
        import asyncio
        
        # Save memory in background without blocking UI
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            memory_task = loop.create_task(async_save())
            memory_id = None  # Don't wait for result to avoid blocking
        except:
            # Fallback to synchronous save if async fails
            try:
                memory_id = asyncio.run(async_save())
            except:
                memory_id = None
        
        return True, memory_id
    
    except Exception as e:
        st.error(f"Could not save memory: {str(e)}")
        return False, None

def main():
    """Main Streamlit application"""
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">🔧 Docy Search Tool Recommendation Assistant</h1>', unsafe_allow_html=True)
    
    # Display sidebar
    display_sidebar()
    
    # Configuration status banner
    if 'selected_tools' in st.session_state and 'selected_ai_model' in st.session_state:
        selected_tools_count = sum(1 for selected in st.session_state.selected_tools.values() if selected)
        total_tools = len(st.session_state.selected_tools)
        
        # Model display mapping
        model_names = {
            "openai": "GPT-4o Mini",
            "claude": "Claude 3 Opus", 
            "gemini": "Gemini 1.5 Flash",
            "deepseek": "DeepSeek Chat"
        }
        
        current_model = model_names.get(st.session_state.selected_ai_model, "Unknown")
        
        st.info(f"🔧 **Active Configuration:** {selected_tools_count}/{total_tools} tools enabled | 🤖 Model: {current_model}")
    
    # Welcome message for new users
    if not st.session_state.messages:
        st.markdown("""
        ### Welcome to your intelligent development assistant! 🚀
        
        I can help you with:
        - **🔍 Tool Discovery**: Find the best development tools for your projects
        - **📊 Tool Analysis**: Compare tools with detailed analysis and rankings
        - **📚 Installation Guides**: Get step-by-step setup instructions
        - **🐙 GitHub Integration**: Access official repositories and code examples
        - **🧠 Memory**: Remember your preferences and past conversations
        
        **Try asking something like:**
        - "I need React development tools"
        - "Compare Vue.js vs Angular" 
        - "Best database for a Node.js project"
        - "How do I set up a Python FastAPI project?"
        """)
    
    # Chat container
    chat_container = st.container()
    
    # Display chat history
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show memory indicator for assistant messages
                if message["role"] == "assistant" and message.get("memory_saved"):
                    memory_id = message.get("memory_id")
                    if memory_id:
                        st.caption(f"💾 Memory saved (ID: {memory_id})")
                    else:
                        st.caption("💾 Memory saved")
    
    # Chat input
    if prompt := st.chat_input("Ask about development tools, frameworks, or project setup..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display response
        with st.chat_message("assistant"):
            # Show active tools before processing
            if 'selected_tools' in st.session_state:
                active_tools = [k for k, v in st.session_state.selected_tools.items() if v]
                if active_tools:
                    tool_names = {
                        "web_search": "🔍 Web Search",
                        "github_search": "🐙 GitHub",
                        "python_tools": "🐍 Python",
                        "tool_recommend": "🎯 AI Analysis",
                        "data_viz": "📊 Visualization"
                    }
                    active_tool_display = " | ".join([tool_names.get(tool, tool) or tool for tool in active_tools])
                    st.caption(f"**Available tools:** {active_tool_display}")
            
            with st.spinner("🤔 Thinking..."):
                # Build conversation context from recent messages
                context_messages = st.session_state.messages[-6:]  # Last 6 messages for context
                context = "Recent conversation:\n"
                for msg in context_messages:
                    context += f"{msg['role']}: {msg['content']}\n"
                
                # Get response from agent
                response = asyncio.run(get_agent_response(prompt, context))
                
                # Display response
                st.markdown(response)
                
                # Save to memory
                memory_saved, memory_id = save_memory(prompt, response)
                
                # Show memory status
                if memory_saved:
                    if memory_id:
                        st.caption(f"💾 Memory saved (ID: {memory_id})")
                    else:
                        st.caption("💾 Memory saved")
                
                # Add assistant message to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response,
                    "memory_saved": memory_saved,
                    "memory_id": memory_id
                })
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("🧠 Memory persists across sessions")
    
    with col2:
        st.caption("🔧 Type questions about development tools")
    
    with col3:
        st.caption("🚀 Powered by Pydantic AI & MCP")

if __name__ == "__main__":
    main()
