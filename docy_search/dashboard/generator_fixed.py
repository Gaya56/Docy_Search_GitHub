# docy_search/dashboard/generator.py
"""Dashboard generation orchestration"""
import json
from typing import Dict, Any, Optional
from datetime import datetime

from docy_search.activity_tracker import activity_tracker
from docy_search.database import SQLAgent, run_sql_query

from .validators import validate_schema_analysis


class DashboardGenerator:
    """Orchestrates dashboard generation from database"""

    def __init__(self, model):
        self.model = model
        self.sql_agent = SQLAgent(model)

    async def generate_full_dashboard(self, user_id: Optional[str] = None) -> str:
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
        """Analyze database and identify metrics"""
        # Mock schema analysis - will be replaced with actual implementation
        mock_schema = {
            "database_summary": "Mock database analysis",
            "key_metrics": [
                {
                    "metric": "Total Records",
                    "description": "Count of all records",
                    "sql": ("SELECT COUNT(*) as total "
                           "FROM information_schema.tables"),
                    "type": "count"
                },
                {
                    "metric": "Database Tables",
                    "description": "Number of tables in database",
                    "sql": ("SELECT COUNT(*) as table_count "
                           "FROM information_schema.tables "
                           "WHERE table_schema = DATABASE()"),
                    "type": "count"
                }
            ]
        }

        return validate_schema_analysis(mock_schema)

    async def _fetch_metrics_data(self, schema_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SQL queries for each metric"""
        metrics_with_data = {"metrics": []}

        for metric in schema_analysis["key_metrics"]:
            try:
                data = await self.sql_agent.query(
                    f"Execute this SQL: {metric['sql']}"
                )
                # Parse result as JSON if possible
                try:
                    parsed_data = json.loads(data)
                except Exception:
                    parsed_data = [{"result": data}]

                metrics_with_data["metrics"].append({
                    **metric,
                    "data": parsed_data
                })
            except Exception as e:
                print(f"Failed to fetch {metric['metric']}: {e}")

        return metrics_with_data

    async def _generate_html(self, metrics_data: Dict[str, Any]) -> str:
        """Generate HTML dashboard from metrics"""
        # Simple HTML template - will be replaced with AI generation
        metrics_html = ""
        for metric in metrics_data.get("metrics", []):
            metric_name = metric.get("metric", "Unknown")
            metric_value = (
                metric.get("data", [{}])[0].get("result", "N/A")
            )
            metrics_html += f'''
            <div class="metric">
                <div class="metric-title">{metric_name}</div>
                <div class="metric-value">{metric_value}</div>
            </div>'''

        html_template = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    margin: 20px; 
                    background: #f5f5f5;
                }}
                .metric {{ 
                    background: white; 
                    padding: 20px; 
                    margin: 15px 0; 
                    border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }}
                .metric-title {{ 
                    font-weight: bold; 
                    color: #333; 
                    margin-bottom: 10px;
                }}
                .metric-value {{ 
                    font-size: 28px; 
                    color: #007acc; 
                    font-weight: bold;
                }}
                h1 {{
                    color: #333;
                    text-align: center;
                    margin-bottom: 30px;
                }}
            </style>
        </head>
        <body>
            <h1>📊 Database Dashboard</h1>
            <div class="metrics">{metrics_html}
            </div>
        </body>
        </html>
        """

        return html_template.strip()
