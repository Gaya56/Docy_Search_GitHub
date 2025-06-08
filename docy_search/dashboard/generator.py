"""Dashboard generation orchestration"""
import asyncio
import json
from typing import Any, Dict, Optional

from docy_search.activity_tracker import activity_tracker
from docy_search.database import SQLAgent
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
        self.sql_agent = SQLAgent(model)

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
        """Analyze database with retry logic"""
        async def analyze():
            # Mock schema analysis - can be replaced with actual AI analysis
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

        return await retry_on_failure(analyze)

    async def _fetch_metrics_data(
        self, schema_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute SQL queries for each metric with retry logic"""
        async def fetch_single_metric(metric):
            """Fetch data for a single metric with retry"""
            async def fetch():
                data = await self.sql_agent.query(
                    f"Execute this SQL: {metric['sql']}"
                )
                # Parse result as JSON if possible
                try:
                    parsed_data = json.loads(data)
                except Exception:
                    parsed_data = [{"result": data}]
                return parsed_data

            return await retry_on_failure(fetch)

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

        html_template = f"""<!DOCTYPE html>
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
</html>"""

        return html_template
