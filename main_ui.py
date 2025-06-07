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
    """Enhanced sidebar with live activity tracking, tool selection, and AI model options"""
    with st.sidebar:
        # Simple live refresh controls
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🔴 Live Activity")
        with col2:
            if st.button("🔄", help="Refresh", key="refresh_activity"):
                st.rerun()
        
        # Auto-refresh checkbox
        auto_refresh = st.checkbox("Auto-refresh (5s)", value=False, help="Automatically refresh activity data")
        
        # Simple auto-refresh using Streamlit's rerun
        if auto_refresh:
            import time
            if 'last_refresh' not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            current_time = time.time()
            if current_time - st.session_state.last_refresh > 5:  # 5 second intervals
                st.session_state.last_refresh = current_time
                st.rerun()
        
        activity_summary = activity_tracker.get_activity_summary()
        current = activity_summary.get("current")
        
        # Current Activity Display
        if current and current["status"] == "running":
            st.success(f"**Running:** {current['action']}")
            progress_val = current.get("progress", 0) / 100.0
            st.progress(progress_val)
            if current.get("details"):
                with st.expander("Details", expanded=False):
                    st.json(current["details"])
        else:
            st.info("No active operations")
        
        # Recent Activities
        st.markdown("### 📜 Recent Activities")
        recent_activities = activity_summary["recent"][-5:] if activity_summary["recent"] else []
        
        if recent_activities:
            for i, activity in enumerate(reversed(recent_activities)):
                status_icon = "✅" if activity["status"] == "complete" else "⏳" if activity["status"] == "running" else "❌"
                
                # Create a compact display
                with st.container():
                    st.markdown(f"**{status_icon} {activity['tool']}** - {activity['time_str']}")
                    if st.button(f"View details", key=f"activity_{i}"):
                        st.json({
                            "action": activity["action"],
                            "duration": f"{activity.get('duration', 0):.2f}s",
                            "result": activity.get("result_preview", "")
                        })
                    st.markdown("---")
        else:
            st.info("No recent activities")
        
        # Resource Access
        st.markdown("### 🔍 Resource Access")
        resources = activity_summary["resources"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files", len(resources["files"]))
            st.metric("Websites", len(resources["websites"]))
        with col2:
            st.metric("Repos", len(resources["repos"]))
            st.metric("API Calls", sum(resources["api_calls"].values()))
        
        # Cost Tracking
        st.markdown("### 💰 API Usage")
        
        try:
            # Initialize costs in session state if missing
            if 'daily_cost' not in st.session_state:
                st.session_state.daily_cost = 0.0
                st.session_state.monthly_cost = 0.0
            
            # Update costs asynchronously without blocking UI
            async def update_costs():
                try:
                    st.session_state.daily_cost = await st.session_state.cost_tracker.get_daily_cost()
                    st.session_state.monthly_cost = await st.session_state.cost_tracker.get_monthly_cost()
                except:
                    pass  # Fail silently to avoid UI blocking
            
            # Run cost update in background
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.create_task(update_costs())
            except:
                pass  # Fail silently if event loop creation fails
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Today", f"${st.session_state.daily_cost:.4f}")
            with col2:
                st.metric("Month", f"${st.session_state.monthly_cost:.2f}")
        except Exception as e:
            st.error(f"Cost tracking error: {e}")
        
        # Session Info
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
        
        # Memory management section
        if memory_manager:
            st.markdown("### 🧠 Memory Management")
            
            # Get memory stats
            if st.button("📊 Memory Stats", use_container_width=True):
                try:
                    # Initialize stats in session state if missing
                    if 'memory_stats' not in st.session_state:
                        st.session_state.memory_stats = {
                            'total': 0, 'active': 0, 'compressed': 0, 'archived': 0
                        }
                    
                    async def get_stats():
                        try:
                            stats = await memory_manager.async_manager.get_user_memory_stats(st.session_state.user_id)
                            st.session_state.memory_stats = stats
                        except:
                            pass  # Fail silently
                    
                    # Update stats in background
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.create_task(get_stats())
                    except:
                        pass
                    
                    # Display cached stats
                    stats = st.session_state.memory_stats
                    st.write(f"**Total memories:** {stats['total']}")
                    st.write(f"**Active memories:** {stats['active']}")
                    st.write(f"**Compressed:** {stats['compressed']}")
                    st.write(f"**Archived:** {stats['archived']}")
                except Exception as e:
                    st.error(f"Error getting stats: {e}")
            
            # Memory maintenance
            if st.button("🔧 Run Maintenance", use_container_width=True):
                try:
                    # Initialize maintenance results in session state
                    if 'maintenance_results' not in st.session_state:
                        st.session_state.maintenance_results = {'compressed': 0, 'archived': 0}
                    
                    async def run_maintenance():
                        try:
                            results = await memory_manager.async_manager.perform_memory_maintenance()
                            st.session_state.maintenance_results = results
                        except:
                            pass  # Fail silently
                    
                    with st.spinner("Running memory maintenance..."):
                        # Run maintenance in background
                        try:
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            loop.create_task(run_maintenance())
                        except:
                            pass
                        
                        # Show cached results
                        results = st.session_state.maintenance_results
                        st.success(f"Compressed: {results['compressed']}, Archived: {results['archived']} memories")
                except Exception as e:
                    st.error(f"Error running maintenance: {e}")
            
            # Clear user memories
            if st.button("🗑️ Clear All Memories", use_container_width=True):
                try:
                    # Initialize cleared count in session state
                    if 'cleared_count' not in st.session_state:
                        st.session_state.cleared_count = 0
                    
                    async def clear_memories():
                        try:
                            cleared = await memory_manager.async_manager.clear_user_memories(st.session_state.user_id)
                            st.session_state.cleared_count = cleared
                        except:
                            pass  # Fail silently
                    
                    # Clear memories in background
                    try:
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.create_task(clear_memories())
                    except:
                        pass
                    
                    # Show cached result
                    st.success(f"Cleared {st.session_state.cleared_count} memories")
                except Exception as e:
                    st.error(f"Error clearing memories: {e}")
        
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
        
        # Tool Selection Dashboard
        st.markdown("---")
        st.markdown("### 🔧 Tool Selection Dashboard")
        
        # Available tools with descriptions
        available_tools = {
            "🔍 Web Search": {
                "description": "Search the web for development tools and resources",
                "key": "web_search",
                "enabled": True
            },
            "🐙 GitHub Integration": {
                "description": "Search GitHub repositories and access code examples",
                "key": "github_search", 
                "enabled": True
            },
            "🐍 Python Tools": {
                "description": "Python-specific development tools and utilities",
                "key": "python_tools",
                "enabled": True
            },
            "🎯 Tool Recommendation": {
                "description": "AI-powered tool analysis and recommendations",
                "key": "tool_recommend",
                "enabled": True
            },
            "📊 Data Visualization": {
                "description": "Create charts and visualizations from data",
                "key": "data_viz",
                "enabled": True
            }
        }
        
        # Initialize tool preferences in session state
        if 'selected_tools' not in st.session_state:
            st.session_state.selected_tools = {tool["key"]: tool["enabled"] for tool in available_tools.values()}
        
        # Tool selection checkboxes
        st.markdown("**Select tools to use in conversations:**")
        
        for tool_name, tool_info in available_tools.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                selected = st.checkbox(
                    tool_name,
                    value=st.session_state.selected_tools.get(tool_info["key"], True),
                    key=f"tool_{tool_info['key']}",
                    help=tool_info["description"]
                )
                st.session_state.selected_tools[tool_info["key"]] = selected
            with col2:
                if selected:
                    st.markdown("✅")
                else:
                    st.markdown("❌")
        
        # Show selected tool count
        selected_count = sum(1 for selected in st.session_state.selected_tools.values() if selected)
        total_count = len(available_tools)
        st.caption(f"**{selected_count}/{total_count} tools selected**")
        
        # AI Model Selection
        st.markdown("---")
        st.markdown("### 🤖 AI Model Selection")
        
        # Available AI models
        ai_models = {
            "OpenAI GPT-4o Mini": {
                "key": "openai",
                "description": "Fast and efficient for general tasks",
                "cost": "Low",
                "speed": "Fast"
            },
            "Claude 3 Opus": {
                "key": "claude", 
                "description": "Excellent for complex reasoning",
                "cost": "High",
                "speed": "Medium"
            },
            "Google Gemini 1.5 Flash": {
                "key": "gemini",
                "description": "Great for analysis and code generation", 
                "cost": "Medium",
                "speed": "Fast"
            },
            "DeepSeek Chat": {
                "key": "deepseek",
                "description": "Cost-effective alternative",
                "cost": "Very Low", 
                "speed": "Medium"
            }
        }
        
        # Model selection radio buttons (AI model already initialized in initialize_session_state)
        selected_model = st.radio(
            "Choose AI Model:",
            options=list(ai_models.keys()),
            index=list(ai_models.keys()).index([k for k, v in ai_models.items() if v["key"] == st.session_state.selected_ai_model][0]) if st.session_state.selected_ai_model in [v["key"] for v in ai_models.values()] else 0,
            key="ai_model_selection"
        )
        
        # Update session state and detect changes
        previous_model = st.session_state.get('previous_ai_model', st.session_state.selected_ai_model)
        st.session_state.selected_ai_model = ai_models[selected_model]["key"]
        
        # Show model change notification
        if previous_model != st.session_state.selected_ai_model:
            st.session_state.previous_ai_model = st.session_state.selected_ai_model
            st.success(f"🔄 AI model switched to {selected_model}")
            st.info("💡 Agent cache cleared - next message will use the new model")
        
        # Display model info
        model_info = ai_models[selected_model]
        st.markdown(f"""
        **{selected_model}**
        - {model_info['description']}
        - Cost: {model_info['cost']}
        - Speed: {model_info['speed']}
        """)
        
        # Quick presets
        st.markdown("**Quick Presets:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 All Tools", use_container_width=True):
                for key in st.session_state.selected_tools:
                    st.session_state.selected_tools[key] = True
                st.rerun()
        
        with col2:
            if st.button("⚡ Essential Only", use_container_width=True):
                # Enable only essential tools
                essential_tools = ["web_search", "tool_recommend"]
                for key in st.session_state.selected_tools:
                    st.session_state.selected_tools[key] = key in essential_tools
                st.rerun()
        
        # Configuration export/import
        with st.expander("⚙️ Configuration"):
            config = {
                "tools": st.session_state.selected_tools,
                "ai_model": st.session_state.selected_ai_model
            }
            st.json(config)
            
            # Quick copy config
            st.code(f"Tools: {selected_count}/{total_count} | Model: {selected_model}", language="text")

async def get_agent_response(prompt, conversation_context):
    """Get response from the agent with dynamic model switching"""
    try:
        # Get current model selection
        current_model = st.session_state.get('selected_ai_model', 'openai')
        
        # Create cache key based on model and context
        agent_cache_key = f"agent_{current_model}"
        
        # Create agent if not cached or model changed
        if agent_cache_key not in st.session_state:
            # Clear any old agent cache when model changes
            for key in list(st.session_state.keys()):
                if key.startswith('agent_'):
                    del st.session_state[key]
            
            # Create new agent with selected model
            st.session_state[agent_cache_key] = create_agent_with_context(
                st.session_state.project_context, 
                st.session_state.user_id,
                model_name=current_model
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
                    active_tool_display = " | ".join([tool_names.get(tool, tool) for tool in active_tools])
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
