import streamlit as st
import asyncio
import pandas as pd
from datetime import datetime
from docy_search.dashboard.generator import DashboardGenerator
from docy_search.app import model


class DashboardComponent:
    """Dashboard generation and display"""
    
    def __init__(self):
        if "dashboard_state" not in st.session_state:
            st.session_state.dashboard_state = {
                "generated": False,
                "html_content": None,
                "metadata": None
            }
    
    def render(self):
        """Render dashboard interface"""
        st.markdown("## 📊 AI Dashboard Generator")
        
        # Check database configuration
        if not self._check_db_config():
            st.warning("⚠️ Database not available. SQLite initialization failed.")
            return
        
        # Add tabs for dashboard and data viewer
        tab1, tab2 = st.tabs(["📊 Dashboard", "🗄️ Database Viewer"])
        
        with tab1:
            self._render_dashboard_tab()
        
        with tab2:
            self._render_database_viewer()
    
    def _render_dashboard_tab(self):
        """Render the dashboard generation tab"""
        # Generation section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("Generate an interactive dashboard from your database with AI-powered insights.")
        with col2:
            if st.button("🚀 Generate Dashboard", type="primary", use_container_width=True):
                self._generate_dashboard()
        
        # Display generated dashboard
        if st.session_state.dashboard_state["generated"]:
            self._display_dashboard()
    
    def _check_db_config(self) -> bool:
        """Check if SQLite database is available"""
        try:
            from docy_search.database.db_manager import get_db_manager
            # Try to initialize database manager
            db = get_db_manager()
            return True
        except Exception:
            return False
    
    def _generate_dashboard(self):
        """Generate dashboard using DashboardGenerator"""
        async def generate():
            dashboard_generator = DashboardGenerator(model)
            return await dashboard_generator.generate_full_dashboard()
        
        with st.spinner("🔍 Analyzing database schema..."):
            try:
                # Run async dashboard generation
                html_content = asyncio.run(generate())
                
                # Update session state
                st.session_state.dashboard_state["generated"] = True
                st.session_state.dashboard_state["html_content"] = html_content
                st.session_state.dashboard_state["metadata"] = {
                    "generated_at": datetime.now().isoformat(),
                    "model": model.__class__.__name__,
                    "status": "success"
                }
                st.success("✅ Dashboard generated successfully!")
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Dashboard generation failed: {str(e)}")
                st.session_state.dashboard_state["generated"] = False
    
    def _display_dashboard(self):
        """Display generated dashboard with preview and export"""
        st.divider()

        # Metadata section
        with st.expander("📋 Dashboard Details", expanded=False):
            metadata = st.session_state.dashboard_state.get("metadata", {})
            col1, col2 = st.columns(2)
            with col1:
                generated_at = metadata.get("generated_at", "N/A")[:19]
                st.metric("Generated", generated_at)
            with col2:
                st.metric("Model", metadata.get("model", "Unknown"))

        # Preview section
        st.markdown("### 👁️ Dashboard Preview")

        html_content = st.session_state.dashboard_state.get("html_content")
        if html_content:
            # Display in iframe
            st.components.v1.html(html_content, height=800, scrolling=True)

            # Export section
            st.divider()
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                st.download_button(
                    label="📥 Download Dashboard HTML",
                    data=html_content,
                    file_name=f"dashboard_{timestamp}.html",
                    mime="text/html",
                    use_container_width=True,
                    type="primary"
                )
                st.caption(f"File size: {len(html_content):,} bytes")
        else:
            st.error("No dashboard content available")

    def _render_database_viewer(self):
        """Render database data viewer"""
        st.markdown("### 🗄️ Database Records")
        
        try:
            from docy_search.database.db_manager import get_db_manager
            db = get_db_manager()
            
            # Show database stats
            stats = db.get_database_stats()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Chat Records", stats.get('chat_history_count', 0))
            with col2:
                st.metric("Memory Entries", stats.get('memory_entries_count', 0))
            with col3:
                st.metric("Activity Logs", stats.get('activity_log_count', 0))
            
            st.divider()
            
            # Chat History Viewer
            st.markdown("#### 💬 Recent Chat History")
            if st.button("🔄 Refresh Chat Data"):
                st.rerun()
            
            chat_history = db.get_chat_history(
                user_id=st.session_state.get('user_id', 'unknown'),
                limit=20
            )
            
            if chat_history:
                # Convert to DataFrame for better display
                df = pd.DataFrame(chat_history)
                
                # Show summary stats
                st.write(f"**Showing {len(df)} most recent conversations**")
                
                # Display each chat record
                for idx, record in enumerate(chat_history):
                    with st.expander(f"💬 Chat {idx+1} - {record.get('timestamp', 'Unknown time')[:19]}"):
                        col1, col2 = st.columns([1, 3])
                        
                        with col1:
                            st.write("**Metadata:**")
                            st.write(f"Model: {record.get('model_used', 'Unknown')}")
                            st.write(f"Cost: ${record.get('cost', 0):.4f}")
                            if record.get('tools_used'):
                                tools = record['tools_used']
                                if isinstance(tools, str):
                                    import json
                                    try:
                                        tools = json.loads(tools)
                                    except:
                                        tools = [tools]
                                st.write(f"Tools: {', '.join(tools) if tools else 'None'}")
                        
                        with col2:
                            st.write("**Conversation:**")
                            st.write("🔵 **User:**")
                            st.write(record.get('prompt', 'No prompt')[:500] + ("..." if len(record.get('prompt', '')) > 500 else ""))
                            
                            st.write("🤖 **Assistant:**")
                            st.write(record.get('response', 'No response')[:500] + ("..." if len(record.get('response', '')) > 500 else ""))
                
                # Export functionality
                st.divider()
                col1, col2 = st.columns(2)
                with col1:
                    # Export as CSV
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download as CSV",
                        data=csv_data,
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Export as JSON
                    import json
                    json_data = json.dumps(chat_history, indent=2)
                    st.download_button(
                        label="📥 Download as JSON",
                        data=json_data,
                        file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                    
            else:
                st.info("No chat history found for this user.")
                
        except Exception as e:
            st.error(f"Error accessing database: {str(e)}")