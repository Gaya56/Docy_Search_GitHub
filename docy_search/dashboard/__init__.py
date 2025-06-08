# docy_search/dashboard/__init__.py
"""Dashboard generation module"""

from .generator import DashboardGenerator
from .prompts import ANALYZE_SCHEMA_PROMPT, GENERATE_HTML_PROMPT
from .validators import validate_schema_analysis, clean_json_response

__all__ = [
    'DashboardGenerator',
    'ANALYZE_SCHEMA_PROMPT',
    'GENERATE_HTML_PROMPT',
    'validate_schema_analysis',
    'clean_json_response'
]
