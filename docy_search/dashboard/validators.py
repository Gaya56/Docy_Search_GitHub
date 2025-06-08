"""Validation functions for dashboard generation"""
from typing import Dict, Any, List


def validate_schema_analysis(schema_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and clean schema analysis data"""
    if not isinstance(schema_data, dict):
        raise ValueError("Schema data must be a dictionary")
    
    # Ensure required keys exist
    if "key_metrics" not in schema_data:
        schema_data["key_metrics"] = []
    
    # Validate metrics structure
    if not isinstance(schema_data["key_metrics"], list):
        schema_data["key_metrics"] = []
    
    # Ensure each metric has required fields
    validated_metrics = []
    for metric in schema_data["key_metrics"]:
        if isinstance(metric, dict):
            validated_metric = {
                "metric": metric.get("metric", "Unknown Metric"),
                "description": metric.get("description", "No description"),
                "sql": metric.get("sql", "SELECT 1 as value"),
                "type": metric.get("type", "count")
            }
            validated_metrics.append(validated_metric)
    
    schema_data["key_metrics"] = validated_metrics
    
    return schema_data


def validate_metrics_data(metrics_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate metrics data structure"""
    if not isinstance(metrics_data, dict):
        return {"metrics": []}
    
    if "metrics" not in metrics_data:
        metrics_data["metrics"] = []
    
    return metrics_data