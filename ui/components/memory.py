"""
Memory Component for Docy Search Assistant
Handles memory-related UI operations including save operations and memory management
"""

import streamlit as st
import asyncio
from datetime import datetime
from typing import Tuple, Optional

# Import from app for memory_manager access
from app import memory_manager


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
                    # Final fallback to synchronous memory manager
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
