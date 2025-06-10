import streamlit as st
import streamlit.components.v1 as components
import asyncio
from datetime import datetime
from docy_search.database import run_sql_query
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