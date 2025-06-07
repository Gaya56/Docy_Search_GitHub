"""
UI Utils Package
Contains utility functions and constants for the UI
"""

from .styles import inject_all_styles

__all__ = ['inject_all_styles']

from .styles import inject_all_styles, get_main_styles, get_chat_styles, get_sidebar_styles, get_responsive_styles

__all__ = ['inject_all_styles', 'get_main_styles', 'get_chat_styles', 'get_sidebar_styles', 'get_responsive_styles']
