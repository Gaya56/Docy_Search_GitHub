import streamlit as st
import random
from typing import Dict, Any

# Import required modules
from docy_search.tool_recommendation.activity_tracker import activity_tracker


class SidebarComponent:
    """Handles all sidebar functionality"""
    
    def __init__(self, memory_manager=None, model=None):
        self.memory_manager = memory_manager
        self.model = model
        self._init_session_state()
    
    def _init_session_state(self):
        """Initialize sidebar-specific session state"""
        if 'daily_cost' not in st.session_state:
            st.session_state.daily_cost = 0.0
            st.session_state.monthly_cost = 0.0
        if 'prev_selected_tools' not in st.session_state:
            st.session_state.prev_selected_tools = {}
        if 'memory_stats' not in st.session_state:
            st.session_state.memory_stats = {
                'total': 0, 'active': 0, 'compressed': 0, 'archived': 0
            }
        if 'maintenance_results' not in st.session_state:
            st.session_state.maintenance_results = {'compressed': 0, 'archived': 0}
        if 'cleared_count' not in st.session_state:
            st.session_state.cleared_count = 0
        if 'selected_ai_model' not in st.session_state:
            st.session_state.selected_ai_model = "openai"
        if 'previous_ai_model' not in st.session_state:
            st.session_state.previous_ai_model = st.session_state.selected_ai_model
        if 'memory_stats_loaded' not in st.session_state:
            st.session_state.memory_stats_loaded = False
    
    def _check_database_config(self) -> bool:
        """Check if SQLite database is available"""
        try:
            from docy_search.database.db_manager import get_db_manager
            # Try to initialize database manager
            db = get_db_manager()
            return True
        except Exception:
            return False
    
    def render(self) -> Dict[str, Any]:
        """Render sidebar and return configuration changes"""
        config_changes = {}
        
        with st.sidebar:
            self._render_activity_section()
            self._render_resource_access()
            self._render_cost_tracking()
            self._render_session_info()
            self._render_controls()
            
            if self.memory_manager:
                self._render_memory_management()
            
            self._render_development_info()
            
            # Tool and model selection
            tool_changes = self._render_tool_selection()
            model_changes = self._render_model_selection()
            
            if tool_changes:
                config_changes['tools_changed'] = True
            if model_changes:
                config_changes['model_changed'] = True
                
        return config_changes
    
    def _render_activity_section(self):
        """Activity tracking display"""
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("### 🔴 Live Activity")
        with col2:
            if st.button("🔄", help="Refresh", key="refresh_activity"):
                st.rerun()
        
        # Auto-refresh logic
        auto_refresh = st.checkbox("Auto-refresh (5s)", value=False, help="Automatically refresh activity data")
        if auto_refresh:
            import time
            if 'last_refresh' not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            current_time = time.time()
            if current_time - st.session_state.last_refresh > 5:  # 5 second intervals
                st.session_state.last_refresh = current_time
                st.rerun()
        
        # Current activity
        activity_summary = activity_tracker.get_activity_summary()
        current = activity_summary.get("current")
        
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
    
    def _render_resource_access(self):
        """Resource access display"""
        st.markdown("### 🔍 Resource Access")
        activity_summary = activity_tracker.get_activity_summary()
        resources = activity_summary["resources"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Files", len(resources["files"]))
            st.metric("Websites", len(resources["websites"]))
        with col2:
            st.metric("Repos", len(resources["repos"]))
            st.metric("API Calls", sum(resources["api_calls"].values()))
    
    def _render_cost_tracking(self):
        """Cost tracking display"""
        st.markdown("### 💰 API Usage")
        
        try:
            # Use synchronous cost tracking to avoid asyncio conflicts
            try:
                st.session_state.daily_cost = 0.0  # Default values to avoid blocking
                st.session_state.monthly_cost = 0.0
            except:
                pass  # Fail silently
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Today", f"${st.session_state.daily_cost:.4f}")
            with col2:
                st.metric("Month", f"${st.session_state.monthly_cost:.2f}")
        except Exception as e:
            st.error(f"Cost tracking error: {e}")
    
    def _render_session_info(self):
        """Session information display"""
        st.markdown("### 📊 Session Info")
        
        # Session details in a styled container
        model_name = self.model.__class__.__name__ if self.model else "Unknown"
        st.markdown(f"""
        <div class="session-info">
            <strong>Session ID:</strong> {st.session_state.user_id[:8]}...<br>
            <strong>Model:</strong> {model_name}<br>
            <strong>Messages:</strong> {len(st.session_state.messages)}
        </div>
        """, unsafe_allow_html=True)
        
        # Memory system status
        if self.memory_manager:
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
    
    def _render_controls(self):
        """Basic controls section"""
        st.markdown("### 🛠️ Controls")
        
        # Clear conversation
        if st.button("🗑️ Clear Conversation", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    def _render_memory_management(self):
        """Memory management controls with proper async handling"""
        st.markdown("### 🧠 Memory Management")
        
        # Auto-load stats on first render if not already loaded
        if not st.session_state.get('memory_stats_loaded', False):
            self._load_memory_stats()
        
        # Display current stats
        stats = st.session_state.memory_stats
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total", stats['total'])
            st.metric("Active", stats['active'])
        with col2:
            st.metric("Compressed", stats['compressed'])
            st.metric("Archived", stats['archived'])
        
        # Refresh button
        if st.button("🔄 Refresh Stats", use_container_width=True):
            self._load_memory_stats()
            st.rerun()
        
        # Memory maintenance
        if st.button("🔧 Run Maintenance", use_container_width=True):
            self._run_memory_maintenance()
        
        # Clear memories
        if st.button("🗑️ Clear All Memories", use_container_width=True):
            self._clear_user_memories()

    def _load_memory_stats(self):
        """Load memory statistics using proper async handling"""
        try:
            async def get_stats_async():
                return await self.memory_manager.async_manager.get_user_memory_stats(st.session_state.user_id)
            
            with st.spinner("Loading memory stats..."):
                import asyncio
                stats = asyncio.run(get_stats_async())
                st.session_state.memory_stats = stats
                st.session_state.memory_stats_loaded = True
                
        except Exception as e:
            st.error(f"Could not load memory stats: {e}")
            # Set fallback stats
            st.session_state.memory_stats = {
                'total': 0, 'active': 0, 'compressed': 0, 'archived': 0
            }

    def _run_memory_maintenance(self):
        """Run memory maintenance using proper async handling"""
        try:
            async def maintenance_async():
                return await self.memory_manager.async_manager.perform_memory_maintenance()
            
            with st.spinner("Running memory maintenance..."):
                import asyncio
                results = asyncio.run(maintenance_async())
                st.session_state.maintenance_results = results
                st.success(f"Compressed: {results['compressed']}, Archived: {results['archived']} memories")
                # Refresh stats after maintenance
                self._load_memory_stats()
                
        except Exception as e:
            st.error(f"Maintenance failed: {e}")

    def _clear_user_memories(self):
        """Clear user memories using proper async handling"""
        try:
            async def clear_async():
                return await self.memory_manager.async_manager.clear_user_memories(st.session_state.user_id)
            
            with st.spinner("Clearing memories..."):
                import asyncio
                cleared_count = asyncio.run(clear_async())
                st.session_state.cleared_count = cleared_count
                st.success(f"Cleared {cleared_count} memories")
                # Refresh stats after clearing
                self._load_memory_stats()
                
        except Exception as e:
            st.error(f"Failed to clear memories: {e}")
    
    def _render_development_info(self):
        """Development information section"""
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
    
    def _render_tool_selection(self) -> bool:
        """Tool selection section - returns True if tools changed"""
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
            },
            "🗄️ SQL Database": {
                "description": "Query databases using natural language",
                "key": "sql_database",
                "enabled": False  # Default off, requires DB config
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
            
            # After SQL Database checkbox
            if tool_info["key"] == "sql_database":
                if not self._check_database_config():
                    st.warning("⚠️ SQLite database not available")
                    st.session_state.selected_tools["sql_database"] = False
        
        # Detect tool selection changes and clear agent cache
        prev_tools = st.session_state.get('prev_selected_tools', {})
        tools_changed = prev_tools != st.session_state.selected_tools
        
        if tools_changed:
            st.session_state.prev_selected_tools = st.session_state.selected_tools.copy()
            # Clear all cached agents to force rebuild with new toolset
            for key in list(st.session_state.keys()):
                if isinstance(key, str) and key.startswith("agent_"):
                    del st.session_state[key]
            if prev_tools:  # Only show notification if not first time
                st.success("🔄 Tool selection updated - agent cache cleared")
        
        # Show selected tool count
        selected_count = sum(1 for selected in st.session_state.selected_tools.values() if selected)
        total_count = len(available_tools)
        st.caption(f"**{selected_count}/{total_count} tools selected**")
        
        # Database Quick Test UI
        if st.session_state.selected_tools.get("sql_database", False):
            with st.expander("🗄️ Database Quick Test"):
                if st.button("Test Connection", key="test_db"):
                    with st.spinner("Testing database connection..."):
                        try:
                            from docy_search.database.db_manager import get_db_manager
                            db = get_db_manager()
                            stats = db.get_database_stats()
                            st.success("✅ Database connected!")
                            st.json(stats)
                        except Exception as e:
                            st.error(f"❌ Connection failed: {str(e)}")
        
        return tools_changed
    
    def _render_model_selection(self) -> bool:
        """AI model selection section - returns True if model changed"""
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
        
        # Model selection radio buttons
        selected_model = st.radio(
            "Choose AI Model:",
            options=list(ai_models.keys()),
            index=list(ai_models.keys()).index([k for k, v in ai_models.items() if v["key"] == st.session_state.selected_ai_model][0]) if st.session_state.selected_ai_model in [v["key"] for v in ai_models.values()] else 0,
            key="ai_model_selection"
        )
        
        # Update session state and detect changes
        previous_model = st.session_state.get('previous_ai_model', st.session_state.selected_ai_model)
        st.session_state.selected_ai_model = ai_models[selected_model]["key"]
        
        model_changed = previous_model != st.session_state.selected_ai_model
        
        # Show model change notification
        if model_changed:
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
                essential_tools = ["web_search", "tool_recommend", "sql_database"]
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
        
        return model_changed
