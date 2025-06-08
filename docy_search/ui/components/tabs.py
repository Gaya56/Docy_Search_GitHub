import streamlit as st
from typing import Callable, Dict, Any

class TabComponent:
    """Manages tab navigation"""
    
    def __init__(self):
        if "active_tab" not in st.session_state:
            st.session_state.active_tab = "chat"
    
    def render(self, tabs: Dict[str, Dict[str, Any]]):
        """Render tab navigation
        
        Args:
            tabs: Dict of tab_key -> {"label": str, "icon": str, "render": Callable}
        """
        # Create columns for tabs
        cols = st.columns(len(tabs))
        
        for idx, (key, config) in enumerate(tabs.items()):
            with cols[idx]:
                if st.button(
                    f"{config['icon']} {config['label']}", 
                    use_container_width=True,
                    type="primary" if st.session_state.active_tab == key else "secondary",
                    key=f"tab_{key}"
                ):
                    st.session_state.active_tab = key
                    st.rerun()
        
        # Render active tab content
        active_config = tabs.get(st.session_state.active_tab)
        if active_config and "render" in active_config:
            active_config["render"]()