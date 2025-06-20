"""
Streamlit UI for Docy_Search with Memory System
Chat Tab Implementation with Live Activity Tracking
"""

import os
import sys
import uuid
from typing import Optional, List

import streamlit as st
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import from existing app.py
from docy_search.app import (
    load_project_context,
    create_agent_with_context,
    model,
    memory_manager
)

# Import cost tracking
from docy_search.memory.cost_tracker import CostTracker

# Import UI components
from docy_search.ui.components.sidebar import SidebarComponent
from docy_search.ui.components.chat import ChatComponent
from docy_search.ui.components.memory import MemoryComponent
from docy_search.ui.components.dashboard import DashboardComponent
from docy_search.ui.utils.styles import inject_all_styles

# Import database (optional - won't break if it fails)
try:
    from docy_search.database.db_manager import get_db_manager
    from docy_search.database.connection_manager import MCPSQLiteConnection
    DATABASE_AVAILABLE = True
    # Initialize database on import
    MCPSQLiteConnection.initialize_database()
except Exception as e:
    print(f"Database not available: {e}")
    DATABASE_AVAILABLE = False

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Docy Search Assistant",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject all CSS styles
inject_all_styles()

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

def display_configuration_banner():
    """Display configuration status banner"""
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
        
        # Add database status to banner
        db_status = "🗄️ Database: Active" if DATABASE_AVAILABLE else "🗄️ Database: Disabled"
        
        st.info(f"🔧 **Active Configuration:** {selected_tools_count}/{total_tools} tools enabled | 🤖 Model: {current_model} | {db_status}")


def log_chat_to_database(
    prompt: str,
    response: str,
    model_used: Optional[str] = None,
    tools_used: Optional[List[str]] = None,
    memory_id: Optional[str] = None
):
    """Log chat interaction to database if available"""
    if DATABASE_AVAILABLE:
        try:
            db = get_db_manager()
            db.save_chat_interaction(
                user_id=st.session_state.user_id,
                prompt=prompt,
                response=response,
                model_used=model_used,
                tools_used=tools_used,
                memory_id=memory_id
            )
        except Exception as e:
            print(f"Database logging failed: {e}")

def display_footer():
    """Display footer"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.caption("🧠 Memory persists across sessions")
    
    with col2:
        st.caption("🔧 Type questions about development tools")
    
    with col3:
        st.caption("🚀 Powered by Pydantic AI & MCP")


def render_advanced_tools_tab():
    """Render the Advanced Tools tab with our new tools"""
    st.header("🔧 Advanced Tools")
    st.markdown("Powerful tools for search, database queries, and code analysis")
    
    # Create sub-tabs for different tool categories
    tool_tab1, tool_tab2, tool_tab3 = st.tabs([
        "🧠 Perplexity Search", 
        "🗃️ Database Tools", 
        "📊 Code Analysis"
    ])
    
    with tool_tab1:
        render_perplexity_tab()
    
    with tool_tab2:
        render_database_tools_tab()
    
    with tool_tab3:
        render_code_analysis_tab()


def render_perplexity_tab():
    """Render Perplexity AI search interface"""
    st.subheader("🧠 Perplexity AI Search")
    st.markdown("Search with AI-powered analysis and focused results")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        query = st.text_input(
            "Search Query",
            placeholder="Enter your search query...",
            key="perplexity_query"
        )
    
    with col2:
        focus = st.selectbox(
            "Focus Area",
            ["general", "academic", "news", "coding", "business"],
            key="perplexity_focus"
        )
    
    if st.button("🔍 Search with Perplexity", type="primary"):
        if query.strip():
            with st.spinner("Searching with Perplexity AI..."):
                try:
                    # Use the AI agent to call the perplexity search tool
                    agent = st.session_state.get('agent_openai_', None)
                    if not agent:
                        from docy_search.app import create_agent_with_context
                        agent = create_agent_with_context(
                            st.session_state.project_context,
                            st.session_state.user_id,
                            'openai',
                            ['search_tools']
                        )
                    
                    # Create a prompt that will trigger the perplexity search
                    prompt = (f"Please use the perplexity_search tool to search for: "
                             f"'{query}' with focus area '{focus}'")
                    
                    result = agent.run_sync(prompt)
                    
                    st.markdown("### Results")
                    st.markdown(str(result.output))
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a search query")


def render_database_tools_tab():
    """Render database query tools interface"""
    st.subheader("🗃️ Database Query Tools")
    st.markdown("Query your database using natural language")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Natural Language Query")
        question = st.text_area(
            "Ask about your database",
            placeholder="How many conversations are there?",
            key="db_question"
        )
        
        if st.button("🔍 Query Database", type="primary"):
            if question.strip():
                with st.spinner("Querying database..."):
                    try:
                        # Use the AI agent to call the database query tool
                        agent = st.session_state.get('agent_openai_', None)
                        if not agent:
                            from docy_search.app import create_agent_with_context
                            agent = create_agent_with_context(
                                st.session_state.project_context,
                                st.session_state.user_id,
                                'openai',
                                ['search_tools']
                            )
                        
                        # Create a prompt that will trigger the database query
                        prompt = (f"Please use the natural_language_query tool "
                                 f"to answer: '{question}'")
                        
                        result = agent.run_sync(prompt)
                        
                        st.markdown("### Query Results")
                        st.code(str(result.output), language="json")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a question")
    
    with col2:
        st.markdown("#### Database Schema")
        if st.button("📋 Show Database Schema"):
            with st.spinner("Getting database schema..."):
                try:
                    # Use the AI agent to get database schema
                    agent = st.session_state.get('agent_openai_', None)
                    if not agent:
                        from docy_search.app import create_agent_with_context
                        agent = create_agent_with_context(
                            st.session_state.project_context,
                            st.session_state.user_id,
                            'openai',
                            ['search_tools']
                        )
                    
                    prompt = "Please use the get_database_schema tool to show the database schema"
                    
                    result = agent.run_sync(prompt)
                    
                    st.markdown("### Database Schema")
                    st.code(str(result.output), language="json")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")


def render_code_analysis_tab():
    """Render code analysis tools interface"""
    st.subheader("📊 Repository Code Analysis")
    st.markdown("Analyze any GitHub repository for code quality and structure")
    
    repo_url = st.text_input(
        "Repository URL or Path",
        placeholder="https://github.com/user/repo or /path/to/repo",
        key="repo_url"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Full Analysis", type="primary"):
            if repo_url.strip():
                with st.spinner("Analyzing repository..."):
                    try:
                        # Use the AI agent to call the code analysis tool
                        agent = st.session_state.get('agent_openai_', None)
                        if not agent:
                            from docy_search.app import create_agent_with_context
                            agent = create_agent_with_context(
                                st.session_state.project_context,
                                st.session_state.user_id,
                                'openai',
                                ['search_tools']
                            )
                        
                        prompt = (f"Please use the analyze_repository tool "
                                 f"to analyze this repository: {repo_url}")
                        
                        result = agent.run_sync(prompt)
                        
                        st.markdown("### Analysis Results")
                        st.code(str(result.output), language="json")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a repository URL or path")
    
    with col2:
        if st.button("⚡ Quick Summary"):
            if repo_url.strip():
                with st.spinner("Getting repository summary..."):
                    try:
                        # Use the AI agent for quick summary
                        agent = st.session_state.get('agent_openai_', None)
                        if not agent:
                            from docy_search.app import create_agent_with_context
                            agent = create_agent_with_context(
                                st.session_state.project_context,
                                st.session_state.user_id,
                                'openai',
                                ['search_tools']
                            )
                        
                        prompt = (f"Please use the analyze_repository tool "
                                 f"to get a summary of: {repo_url}")
                        
                        result = agent.run_sync(prompt)
                        
                        st.markdown("### Repository Summary")
                        st.code(str(result.output), language="json")
                        
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a repository URL or path")


def main():
    """Main Streamlit application"""
    # Initialize session state
    initialize_session_state()
    
    # Main header
    st.markdown('<h1 class="main-header">🔧 Docy Search Tool Recommendation Assistant</h1>', unsafe_allow_html=True)
    
    # Display sidebar
    display_sidebar()
    
    # Configuration status banner
    display_configuration_banner()
    
    # Create tab-based interface
    tab1, tab2, tab3 = st.tabs(["💬 AI Assistant", "📊 Dashboard", "🔧 Advanced Tools"])
    
    with tab1:
        # Chat interface with memory component
        memory_component = MemoryComponent()
    
    def get_cached_agent():
        """Get or create cached agent"""
        current_model = st.session_state.get('selected_ai_model', 'openai')
        selected_tools_list = [k for k, v in st.session_state.selected_tools.items() if v] if 'selected_tools' in st.session_state else []
        tools_hash = hash(tuple(sorted(selected_tools_list)))
        agent_key = f"agent_{current_model}_{tools_hash}"
        
        if agent_key not in st.session_state:
            # Clear any old agent cache when model or tools change
            for key in list(st.session_state.keys()):
                if isinstance(key, str) and key.startswith('agent_'):
                    del st.session_state[key]
            
            st.session_state[agent_key] = create_agent_with_context(
                st.session_state.project_context,
                st.session_state.user_id,
                st.session_state.selected_ai_model,
                [k for k, v in st.session_state.selected_tools.items() if v] if 'selected_tools' in st.session_state else []
            )
        return st.session_state[agent_key]
    
    chat = ChatComponent(get_cached_agent)
    result = chat.render()
    if result:
        prompt, response = result
        memory_saved, memory_id = memory_component.save_memory(prompt, response)
        chat.add_assistant_message(response, memory_saved, memory_id)
        
        # Log to database if available
        log_chat_to_database(
            prompt=prompt,
            response=response,
            model_used=st.session_state.selected_ai_model,
            tools_used=[k for k, v in st.session_state.selected_tools.items() if v] if 'selected_tools' in st.session_state else [],
            memory_id=str(memory_id) if memory_id is not None else None
        )
    
    with tab2:
        # Dashboard interface
        dashboard_component = DashboardComponent()
        dashboard_component.render()
    
    with tab3:
        # Advanced Tools interface
        render_advanced_tools_tab()
    
    # Footer
    display_footer()

if __name__ == "__main__":
    main()
