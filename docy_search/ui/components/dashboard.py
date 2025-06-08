"""Dashboard component for AI-powered dashboard generation"""
import streamlit as st
import streamlit.components.v1 as components
import asyncio
import os
from datetime import datetime
from docy_search.dashboard.generator import DashboardGenerator
from docy_search.app import get_model_from_name


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
            st.warning(
                "⚠️ Database not configured. Please add database "
                "credentials to .env file."
            )
            return

        # Generation section
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(
                "Generate an interactive dashboard from your database "
                "with AI-powered insights."
            )
        with col2:
            if st.button(
                "🚀 Generate Dashboard",
                type="primary",
                use_container_width=True
            ):
                self._generate_dashboard()

        # Display generated dashboard
        if st.session_state.dashboard_state["generated"]:
            self._display_dashboard()

    def _check_db_config(self) -> bool:
        """Check if database is configured"""
        required = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
        return all(os.getenv(var) for var in required)

    def _generate_dashboard(self):
        """Generate dashboard from database"""
        async def async_generate():
            try:
                model = get_model_from_name(st.session_state.selected_ai_model)
                generator = DashboardGenerator(model)
                
                html_content = await generator.generate_full_dashboard(
                    st.session_state.user_id
                )
                
                return {
                    "success": True,
                    "html": html_content,
                    "metadata": {
                        "generated_at": datetime.now().isoformat(),
                        "model": st.session_state.selected_ai_model
                    }
                }
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        with st.spinner("🔍 Analyzing database schema..."):
            # Run async function
            result = asyncio.run(async_generate())
            
            if result["success"]:
                st.session_state.dashboard_state.update({
                    "generated": True,
                    "html_content": result["html"],
                    "metadata": result["metadata"]
                })
                st.success("✅ Dashboard generated successfully!")
                st.rerun()
            else:
                st.error(f"❌ Dashboard generation failed: {result['error']}")

    def _display_dashboard(self):
        """Display generated dashboard"""
        st.divider()

        # Preview section
        st.markdown("### 👁️ Dashboard Preview")

        if st.session_state.dashboard_state.get("html_content"):
            # Display actual HTML
            components.html(
                st.session_state.dashboard_state["html_content"],
                height=600
            )
        else:
            # Show error message
            error = (
                st.session_state.dashboard_state.get("metadata", {})
                .get("error", "Unknown error occurred")
            )
            st.error(f"Dashboard generation failed: {error}")

        # Download section
        col1, col2, col3 = st.columns([2, 1, 1])
        with col2:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"dashboard_{timestamp}.html"

            st.download_button(
                "📥 Download HTML",
                data=st.session_state.dashboard_state.get(
                    "html_content", ""
                ),
                file_name=filename,
                mime="text/html",
                disabled=not st.session_state.dashboard_state.get(
                    "html_content"
                )
            )
