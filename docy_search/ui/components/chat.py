import streamlit as st
import asyncio
from typing import List, Dict, Optional, Tuple

class ChatComponent:
    """Handles chat interface and message management"""
    
    def __init__(self, agent_getter):
        self.get_agent = agent_getter
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize chat-specific session state"""
        if 'messages' not in st.session_state:
            st.session_state.messages = []
    
    def render(self) -> Optional[Tuple[str, str]]:
        """Render chat interface and return (prompt, response) if new message"""
        # Welcome message
        if not st.session_state.messages:
            self._render_welcome()
        
        # Chat history
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["role"] == "assistant" and message.get("memory_saved"):
                        st.caption(f"💾 Memory saved{f' (ID: {message.get('memory_id')})' if message.get('memory_id') else ''}")
        
        # Chat input
        if prompt := st.chat_input("Ask about development tools, frameworks, or project setup..."):
            return self._handle_message(prompt, chat_container)
        
        return None
    
    def _handle_message(self, prompt: str, container) -> Tuple[str, str]:
        """Process user message and get response"""
        # Add to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with container:
            with st.chat_message("user"):
                st.markdown(prompt)
        
        # Get response
        with st.chat_message("assistant"):
            self._show_active_tools()
            
            with st.spinner("🤔 Thinking..."):
                context = self._build_context()
                response = asyncio.run(self._get_response(prompt, context))
                
                st.markdown(response)
                return prompt, response
    
    async def _get_response(self, prompt: str, context: str) -> str:
        """Get agent response with proper MCP server context"""
        try:
            agent = self.get_agent()
            full_prompt = f"{context}\nCurrent message: {prompt}"
            
            # Run agent within MCP server context
            async with agent.run_mcp_servers():
                result = await agent.run(full_prompt)
                return result.output
        except Exception as e:
            error_msg = str(e)
            if "MCP server is not running" in error_msg:
                return (f"I apologize, but there was an issue connecting to the tools. "
                       f"The system is initializing. Please try your question again in a moment.")
            return f"I apologize, but I encountered an error: {error_msg}. Please try again."
    
    def _build_context(self) -> str:
        """Build conversation context"""
        context_messages = st.session_state.messages[-6:]
        context = "Recent conversation:\n"
        for msg in context_messages:
            context += f"{msg['role']}: {msg['content']}\n"
        return context
    
    def _show_active_tools(self):
        """Display active tools"""
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
                display = " | ".join([tool_names.get(tool, tool) or tool for tool in active_tools])
                st.caption(f"**Available tools:** {display}")
    
    def _render_welcome(self):
        """Render welcome message"""
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
    
    def add_assistant_message(self, content: str, memory_saved: bool = False, memory_id: Optional[int] = None):
        """Add assistant message to history"""
        st.session_state.messages.append({
            "role": "assistant",
            "content": content,
            "memory_saved": memory_saved,
            "memory_id": memory_id
        })
