"""
Memory Component for Docy Search Assistant
Handles memory-related UI operations including save operations and memory management
"""

import streamlit as st
import asyncio
from datetime import datetime
from typing import Tuple, Optional

# Import from app for memory_manager access
from docy_search.app import memory_manager


class MemoryComponent:
    """Component for handling memory operations in the UI"""
    
    def __init__(self):
        """Initialize the memory component"""
        pass
    
    def save_memory(self, prompt: str, response: str) -> Tuple[bool, Optional[int]]:
        """
        Save interaction to memory if conditions are met
        
        Args:
            prompt: User prompt/question
            response: Assistant response
            
        Returns:
            Tuple of (success: bool, memory_id: Optional[int])
        """
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
            
            # Use synchronous memory saving to avoid asyncio conflicts in Streamlit
            try:
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
            except Exception as fallback_error:
                memory_id = None
            
            return True, memory_id
        
        except Exception as e:
            st.error(f"Could not save memory: {str(e)}")
            return False, None
    
    def render_memory_status(self, memory_saved: bool, memory_id: Optional[int]) -> None:
        """
        Render memory status indicator in the UI
        
        Args:
            memory_saved: Whether memory was successfully saved
            memory_id: The ID of the saved memory (if any)
        """
        if memory_saved:
            if memory_id:
                st.caption(f"💾 Saved to memory (ID: {memory_id})")
            else:
                st.caption("💾 Saving to memory...")
        else:
            st.caption("ℹ️ Response too short for memory")
