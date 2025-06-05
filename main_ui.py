"""
Streamlit UI for Docy_Search with Memory System
Chat Tab Implementation
"""

import streamlit as st
import asyncio
import os
import uuid
import random
from datetime import datetime
from dotenv import load_dotenv

# Import pydantic-ai components
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel

# Import memory system
from memory.memory_manager import MemoryManager

# Load environment variables
load_dotenv()

# Initialize model (same logic as app.py)
model_type = os.getenv("AI_MODEL", "openai").lower()
if model_type == "claude":
    model = AnthropicModel(model_name="claude-3-opus-20240229")
elif model_type == "gemini":
    model = GoogleModel(model_name="gemini-1.5-flash")
elif model_type == "deepseek":
    model = OpenAIModel(model_name="deepseek-chat", base_url="https://api.deepseek.com/v1")
else:
    model = OpenAIModel(model_name="gpt-4o-mini")

# Define MCP servers (from app.py)
brave_server = MCPServerStdio('python', ['brave_search.py'])
python_tools_server = MCPServerStdio('python', ['python_tools.py'])
tool_recommendation_server = MCPServerStdio('python', ['tool_recommendation/mcp_server.py'])
github_server = MCPServerStdio('python', ['github_mcp_server.py'])

# Page configuration
st.set_page_config(
    page_title="Docy Search Assistant",
    page_icon="🔧",
    layout="wide"
)

# Get random port for display
PORT = random.randint(8502, 8599)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    user_session_file = ".user_session"
    if os.path.exists(user_session_file):
        with open(user_session_file, 'r') as f:
            st.session_state.user_id = f.read().strip()
    else:
        st.session_state.user_id = str(uuid.uuid4())
        with open(user_session_file, 'w') as f:
            f.write(st.session_state.user_id)

# Load project context function
def load_project_context():
    context_file = "project_context.md"
    if os.path.exists(context_file):
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            st.warning(f"Could not load project context: {e}")
            return ""
    return ""

# Create agent function (from app.py)
def create_agent_with_context(project_context="", user_id=None):
    context_section = ""
    if project_context.strip():
        context_section = f"""
**PROJECT CONTEXT**
The user has provided the following information about their current project:

{project_context}

Use this context to provide more targeted and relevant tool recommendations.

---

"""
    
    # Load memories if available
    if user_id and memory_manager:
        try:
            memories = memory_manager.retrieve_memories(
                user_id=user_id,
                limit=5,
                category="tool_recommendation"
            )
            if memories and memories != "No previous interactions found.":
                context_section += f"""
**PREVIOUS INTERACTIONS**
{memories}

---

"""
        except Exception:
            pass
    
    system_prompt = f"""{context_section}You are an intelligent tool recommendation assistant specializing in helping developers, engineers, and technical professionals discover, analyze, and implement the best tools for their projects and workflows."""
    
    return Agent(
        model, 
        mcp_servers=[brave_server, python_tools_server, tool_recommendation_server, github_server],
        retries=3,
        system_prompt=system_prompt
    )

# Initialize memory manager
@st.cache_resource
def get_memory_manager():
    try:
        return MemoryManager(db_path="data/memories.db", model=model)
    except Exception as e:
        st.warning(f"Memory system disabled: {e}")
        return None

memory_manager = get_memory_manager()
project_context = load_project_context()

# Main UI
st.title("🔧 Docy Search Tool Recommendation Assistant")

# Sidebar
with st.sidebar:
    st.markdown("### Session Info")
    st.text(f"Session ID: {st.session_state.user_id[:8]}...")
    st.success("✅ Memory active" if memory_manager else "⚠️ Memory disabled")
    st.info(f"Run: `streamlit run main_ui.py --server.port {PORT}`")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("memory_saved"):
            st.caption("💾 Memory saved")

# Chat input
if prompt := st.chat_input("Ask about development tools..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Build conversation context
            context = "Recent conversation:\n"
            for msg in st.session_state.messages[-6:]:
                context += f"{msg['role']}: {msg['content']}\n"
            
            # Create agent and get response
            agent = create_agent_with_context(project_context, st.session_state.user_id)
            
            async def get_response():
                async with agent.run_mcp_servers():
                    result = await agent.run(f"{context}\nCurrent message: {prompt}")
                    return result.output
            
            response = asyncio.run(get_response())
            st.markdown(response)
            
            # Save to memory if significant
            memory_saved = False
            if memory_manager and len(response) > 100:
                try:
                    memory_content = f"User asked: {prompt[:200]}\nAssistant provided: {response[:500]}"
                    if len(response) > 500:
                        memory_content += "..."
                    
                    memory_id = memory_manager.save_memory(
                        user_id=st.session_state.user_id,
                        content=memory_content,
                        metadata={
                            "timestamp": datetime.now().isoformat(),
                            "user_input_length": len(prompt),
                            "response_length": len(response),
                            "category": "tool_recommendation"
                        },
                        category="tool_recommendation"
                    )
                    memory_saved = True
                    st.caption(f"💾 Memory saved (ID: {memory_id})")
                except Exception as e:
                    st.error(f"Memory error: {e}")
            
            # Add to message history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "memory_saved": memory_saved
            })

# Footer
st.markdown("---")
st.caption("Memory persists across sessions")
