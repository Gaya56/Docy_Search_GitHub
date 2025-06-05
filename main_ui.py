"""
Streamlit UI for Docy_Search with Memory System
Chat Tab Implementation
"""

import streamlit as st
import asyncio
import os
import sys
import uuid
import random
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from existing app.py
from app import (
    load_project_context, 
    create_agent_with_context,
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
</style>
""", unsafe_allow_html=True)

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

# Load project context
@st.cache_data
def get_project_context():
    """Load and cache project context"""
    return load_project_context()

def display_sidebar():
    """Display sidebar with session info and controls"""
    with st.sidebar:
        st.markdown("### 📊 Session Info")
        
        # Session details in a styled container
        st.markdown(f"""
        <div class="session-info">
            <strong>Session ID:</strong> {st.session_state.user_id[:8]}...<br>
            <strong>Model:</strong> {model.__class__.__name__}<br>
            <strong>Messages:</strong> {len(st.session_state.messages)}
        </div>
        """, unsafe_allow_html=True)
        
        # Memory system status
        if memory_manager:
            st.markdown("""
            <div class="memory-indicator memory-active">
                ✅ Memory system active<br>
                <small>Conversations are being remembered</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="memory-indicator memory-disabled">
                ⚠️ Memory system disabled<br>
                <small>Running in stateless mode</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 🛠️ Controls")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
        
        # Port suggestion for easier development
        port = random.randint(8502, 8599)
        st.markdown("### 🚀 Development")
        st.info(f"Run with custom port:\n```bash\nstreamlit run main_ui.py --server.port {port}\n```")
        
        # Project context preview
        if st.session_state.project_context:
            with st.expander("📋 Project Context Preview"):
                st.text(st.session_state.project_context[:300] + "..." if len(st.session_state.project_context) > 300 else st.session_state.project_context)
        else:
            st.info("💡 Create `project_context.md` for personalized recommendations")

async def get_agent_response(prompt, conversation_context):
    """Get response from the agent"""
    try:
        # Create agent with context and user ID
        agent = create_agent_with_context(
            st.session_state.project_context, 
            st.session_state.user_id
        )
        
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
        
        # Save memory
        memory_id = memory_manager.save_memory(
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
