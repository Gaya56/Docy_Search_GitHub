"""
UI Package for Docy Search Application
Contains modular UI components and utilities
"""

from .components import (
    SidebarComponent,
    ChatComponent,
    MemoryComponent,
    DashboardComponent
)

from .utils import (
    inject_all_styles,
    get_main_styles,
    get_chat_styles,
    get_sidebar_styles,
    get_responsive_styles
)

__all__ = [
    'SidebarComponent',
    'ChatComponent',
    'MemoryComponent',
    'DashboardComponent',
    'inject_all_styles',
    'get_main_styles',
    'get_chat_styles',
    'get_sidebar_styles',
    'get_responsive_styles'
]
