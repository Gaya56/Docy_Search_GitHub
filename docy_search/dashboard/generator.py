"""Dashboard generation orchestration"""
import asyncio
from typing import Any, Dict, Optional
from datetime import datetime

from docy_search.tool_recommendation.activity_tracker import activity_tracker
from .validators import validate_schema_analysis


async def retry_on_failure(func, max_retries=3, delay=2):
    """Retry async function on failure with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
            wait_time = delay * (attempt + 1)
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time}s: {e}")
            await asyncio.sleep(wait_time)


class DashboardGenerator:
    """Orchestrates dashboard generation from database"""

    def __init__(self, model):
        self.model = model

    async def generate_full_dashboard(
        self, user_id: Optional[str] = None
    ) -> str:
        """Generate complete HTML dashboard"""
        activity_id = await activity_tracker.start_activity(
            "dashboard_generation",
            {"user_id": user_id}
        )

        try:
            # Step 1: Analyze schema
            await activity_tracker.update_activity(
                activity_id, 0.2, {"status": "Analyzing schema"}
            )
            schema_analysis = await self._analyze_database_schema()

            # Step 2: Fetch metric data
            await activity_tracker.update_activity(
                activity_id, 0.5, {"status": "Fetching metrics"}
            )
            metrics_data = await self._fetch_metrics_data(schema_analysis)

            # Step 3: Generate HTML
            await activity_tracker.update_activity(
                activity_id, 0.8, {"status": "Generating HTML"}
            )
            html_content = await self._generate_html(metrics_data)

            await activity_tracker.complete_activity(
                activity_id, "Dashboard generated"
            )
            return html_content

        except Exception as e:
            await activity_tracker.complete_activity(
                activity_id, f"Failed: {str(e)}"
            )
            raise

    async def _analyze_database_schema(self) -> Dict[str, Any]:
        """Analyze SQLite database with retry logic"""
        async def analyze():
            # Use our SQLite database manager for schema analysis
            try:
                from docy_search.database.db_manager import get_db_manager
                db = get_db_manager()
                db_stats = db.get_database_stats()
                
                # SQLite-compatible schema analysis
                schema_analysis = {
                    "database_summary": "SQLite database with chat history, memory entries, and activity logs",
                    "key_metrics": [
                        {
                            "metric": "Total Chat Records",
                            "description": "Number of chat interactions stored",
                            "sql": "SELECT COUNT(*) as count FROM chat_history",
                            "type": "count"
                        },
                        {
                            "metric": "Memory Entries",
                            "description": "Number of memory entries stored",
                            "sql": "SELECT COUNT(*) as count FROM memory_entries",
                            "type": "count"
                        },
                        {
                            "metric": "Activity Logs",
                            "description": "Number of activity log entries",
                            "sql": "SELECT COUNT(*) as count FROM activity_log",
                            "type": "count"
                        },
                        {
                            "metric": "Recent Activity (24h)",
                            "description": "Activity in the last 24 hours",
                            "sql": "SELECT COUNT(*) as count FROM activity_log WHERE timestamp > datetime('now', '-24 hours')",
                            "type": "count"
                        },
                        {
                            "metric": "Total Database Records",
                            "description": "Sum of all records across tables",
                            "sql": "SELECT (SELECT COUNT(*) FROM chat_history) + (SELECT COUNT(*) FROM memory_entries) + (SELECT COUNT(*) FROM activity_log) as total",
                            "type": "count"
                        }
                    ],
                    "database_stats": db_stats
                }
                return validate_schema_analysis(schema_analysis)
            except Exception as e:
                # Fallback to basic mock analysis if database is not available
                mock_schema = {
                    "database_summary": "SQLite database (connection failed)",
                    "key_metrics": [
                        {
                            "metric": "Database Status",
                            "description": "Current database connectivity",
                            "sql": "SELECT 'Database Unavailable' as status",
                            "type": "status"
                        }
                    ],
                    "error": str(e)
                }
                return validate_schema_analysis(mock_schema)

        return await retry_on_failure(analyze)

    async def _fetch_metrics_data(
        self, schema_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute SQL queries for each metric with retry logic"""
        async def fetch_single_metric(metric):
            """Fetch data for a single metric with retry"""
            async def fetch():
                try:
                    # Use our SQLite database manager directly for better reliability
                    from docy_search.database.db_manager import get_db_manager
                    import sqlite3
                    
                    db = get_db_manager()
                    sql_query = metric['sql']
                    
                    with sqlite3.connect(db.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute(sql_query)
                        result = cursor.fetchone()
                        
                        if result:
                            # Convert to dictionary with proper column names
                            columns = [description[0] for description in cursor.description]
                            data = dict(zip(columns, result))
                            return [data]
                        else:
                            return [{"result": "No data"}]
                            
                except Exception as e:
                    # Return error result if direct query fails
                    return [{"result": f"Error: {str(e)}"}]

            return await retry_on_failure(fetch, max_retries=2)

        metrics_with_data: Dict[str, Any] = {"metrics": []}

        for metric in schema_analysis["key_metrics"]:
            try:
                data = await fetch_single_metric(metric)
                metrics_with_data["metrics"].append({
                    **metric,
                    "data": data
                })
            except Exception as e:
                print(f"Failed to fetch {metric['metric']}: {e}")
                # Add metric with error indication
                metrics_with_data["metrics"].append({
                    **metric,
                    "data": [{"result": "Error fetching data"}]
                })

        return metrics_with_data

    async def _generate_html(self, metrics_data: Dict[str, Any]) -> str:
        """Generate HTML dashboard from metrics"""
        async def generate():
            # Enhanced HTML template with better styling and data display
            metrics_html = ""
            for metric in metrics_data.get("metrics", []):
                metric_name = metric.get("metric", "Unknown")
                metric_desc = metric.get("description", "")
                
                # Extract value from data
                data = metric.get("data", [{}])
                if data and isinstance(data, list) and len(data) > 0:
                    first_result = data[0]
                    if isinstance(first_result, dict):
                        # Try to get the first numeric value or 'count' field
                        metric_value = (
                            first_result.get("count") or 
                            first_result.get("total") or 
                            first_result.get("result") or 
                            list(first_result.values())[0] if first_result else "N/A"
                        )
                    else:
                        metric_value = first_result
                else:
                    metric_value = "N/A"
                
                metrics_html += f'''
            <div class="metric">
                <div class="metric-title">{metric_name}</div>
                <div class="metric-value">{metric_value}</div>
                <div class="metric-description">{metric_desc}</div>
            </div>'''

            html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>Docy Search Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .metric {{
            background: rgba(255, 255, 255, 0.95);
            padding: 25px;
            margin: 15px 0;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: transform 0.3s ease;
        }}
        .metric:hover {{
            transform: translateY(-5px);
        }}
        .metric-title {{
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
            font-size: 18px;
        }}
        .metric-value {{
            font-size: 36px;
            color: #3182ce;
            font-weight: bold;
            margin-bottom: 8px;
        }}
        .metric-description {{
            color: #718096;
            font-size: 14px;
            line-height: 1.4;
        }}
        h1 {{
            color: white;
            text-align: center;
            margin-bottom: 40px;
            font-size: 48px;
            font-weight: 300;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.8);
            margin-top: 40px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Docy Search Dashboard</h1>
        <div class="metrics-grid">{metrics_html}
        </div>
        <div class="footer">
            Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | SQLite Database
        </div>
    </div>
</body>
</html>"""
            return html_template.strip()

        return await retry_on_failure(generate)
