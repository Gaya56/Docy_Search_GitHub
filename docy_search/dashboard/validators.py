# docy_search/dashboard/validators.py
"""JSON validation for dashboard generation"""
import json
from typing import Dict, Any


def validate_schema_analysis(json_str: str) -> Dict[str, Any]:
    """Validate schema analysis JSON"""
    data = json.loads(json_str.strip())
    
    required = ["domain", "key_metrics"]
    if not all(key in data for key in required):
        raise ValueError(f"Missing required keys: {required}")
    
    for metric in data.get("key_metrics", []):
        metric_required = ["metric", "description", "visualization_type", "sql"]
        if not all(key in metric for key in metric_required):
            raise ValueError(f"Metric missing keys: {metric_required}")
    
    return data


def clean_json_response(response: str) -> str:
    """Extract JSON from AI response"""
    if "```json" in response:
        response = response.split("```json")[1].split("```")[0]
    elif "```" in response:
        # Handle cases where JSON is in code blocks without language specification
        parts = response.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith('{') and part.endswith('}'):
                response = part
                break
    
    return response.strip()


def clean_html_response(response: str) -> str:
    """Extract HTML from AI response"""
    if "```html" in response:
        response = response.split("```html")[1].split("```")[0]
    elif "```" in response:
        # Handle cases where HTML is in code blocks without language specification
        parts = response.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith('<!DOCTYPE') or part.startswith('<html'):
                response = part
                break
    
    return response.strip()
