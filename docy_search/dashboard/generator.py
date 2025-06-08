# docy_search/dashboard/generator.py
"""Dashboard generation logic"""
import asyncio
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

from docy_search.activity_tracker import activity_tracker
from docy_search.database import run_sql_query
from .prompts import ANALYZE_SCHEMA_PROMPT, GENERATE_HTML_PROMPT
from .validators import (
    validate_schema_analysis,
    clean_json_response,
    clean_html_response
)


class DashboardGenerator:
    """Generates AI-powered dashboards from database schemas"""
    
    def __init__(self, model):
        self.model = model
        
    async def analyze_database_schema(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Analyze database schema and identify key metrics"""
        activity_id = None
        
        try:
            # Start activity tracking
            activity_id = await activity_tracker.start_activity(
                "dashboard_schema_analysis",
                {"user_id": user_id}
            )
            
            # Get database schema
            schema_query = """
            SELECT 
                table_name,
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns 
            WHERE table_schema = DATABASE()
            ORDER BY table_name, ordinal_position
            """
            
            schema_result = await run_sql_query(
                f"Get database schema: {schema_query}",
                user_id
            )
            
            # Analyze schema with AI
            from docy_search.app import create_agent_with_context
            
            agent = create_agent_with_context(
                project_context="Database schema analysis for dashboard generation",
                user_id=user_id,
                selected_tools={"web_search": False, "python_tools": True}
            )
            
            prompt = f"""
            {ANALYZE_SCHEMA_PROMPT}
            
            Database Schema:
            {schema_result}
            """
            
            async with agent.run_mcp_servers():
                result = await agent.run(prompt)
                response = result.output
            
            # Clean and validate JSON response
            clean_response = clean_json_response(response)
            analysis_data = validate_schema_analysis(clean_response)
            
            await activity_tracker.complete_activity(
                activity_id, 
                f"Schema analyzed: {len(analysis_data.get('key_metrics', []))} metrics identified"
            )
            
            return analysis_data
            
        except Exception as e:
            if activity_id:
                await activity_tracker.complete_activity(
                    activity_id, f"Schema analysis failed: {str(e)[:100]}"
                )
            raise Exception(f"Schema analysis failed: {str(e)}")
    
    async def execute_metric_queries(self, metrics: List[Dict[str, Any]], 
                                   user_id: Optional[str] = None) -> Dict[str, Any]:
        """Execute SQL queries for each metric and collect data"""
        metric_data = {}
        
        for metric in metrics:
            try:
                metric_name = metric.get("metric", "unknown")
                sql_query = metric.get("sql", "")
                
                if not sql_query:
                    continue
                
                # Execute the metric query
                result = await run_sql_query(sql_query, user_id)
                
                metric_data[metric_name] = {
                    "data": result,
                    "description": metric.get("description", ""),
                    "visualization_type": metric.get("visualization_type", "table"),
                    "sql": sql_query
                }
                
            except Exception as e:
                # Store error but continue with other metrics
                metric_data[metric_name] = {
                    "error": str(e),
                    "description": metric.get("description", ""),
                    "visualization_type": "error",
                    "sql": sql_query
                }
        
        return metric_data
    
    async def generate_dashboard_html(self, analysis_data: Dict[str, Any], 
                                    metric_data: Dict[str, Any],
                                    user_id: Optional[str] = None) -> str:
        """Generate HTML dashboard from analysis and metric data"""
        activity_id = None
        
        try:
            # Start activity tracking
            activity_id = await activity_tracker.start_activity(
                "dashboard_html_generation",
                {"user_id": user_id, "domain": analysis_data.get("domain", "unknown")}
            )
            
            # Create AI agent for HTML generation
            from docy_search.app import create_agent_with_context
            
            agent = create_agent_with_context(
                project_context="HTML dashboard generation",
                user_id=user_id,
                selected_tools={"web_search": False, "python_tools": True}
            )
            
            # Prepare data summary for AI
            data_summary = {
                "domain": analysis_data.get("domain", "Business"),
                "metrics": []
            }
            
            for metric_name, data in metric_data.items():
                if "error" not in data:
                    data_summary["metrics"].append({
                        "name": metric_name,
                        "description": data["description"],
                        "type": data["visualization_type"],
                        "data_preview": str(data["data"])[:500] + "..." if len(str(data["data"])) > 500 else str(data["data"])
                    })
            
            prompt = f"""
            {GENERATE_HTML_PROMPT}
            
            Dashboard Data:
            {json.dumps(data_summary, indent=2)}
            
            Requirements:
            - Create a responsive dashboard with title "{analysis_data.get('domain', 'Business')} Dashboard"
            - Use Chart.js for visualizations
            - Use Tailwind CSS for styling
            - Include all metrics with appropriate chart types
            - Make it professional and modern
            - Include sample data if actual data is too complex to parse
            """
            
            async with agent.run_mcp_servers():
                result = await agent.run(prompt)
                html_response = result.output
            
            # Clean HTML response
            html_content = clean_html_response(html_response)
            
            # Ensure we have a complete HTML document
            if not html_content.strip().startswith('<!DOCTYPE') and not html_content.strip().startswith('<html'):
                html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis_data.get('domain', 'Business')} Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-6">{analysis_data.get('domain', 'Business')} Dashboard</h1>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {html_content}
        </div>
    </div>
</body>
</html>"""
            
            await activity_tracker.complete_activity(
                activity_id, f"HTML dashboard generated: {len(html_content)} characters"
            )
            
            return html_content
            
        except Exception as e:
            if activity_id:
                await activity_tracker.complete_activity(
                    activity_id, f"HTML generation failed: {str(e)[:100]}"
                )
            raise Exception(f"HTML generation failed: {str(e)}")
    
    async def generate_full_dashboard(self, user_id: Optional[str] = None) -> str:
        """Generate complete dashboard from database"""
        try:
            # Step 1: Analyze database schema
            analysis_data = await self.analyze_database_schema(user_id)
            
            # Step 2: Execute metric queries
            metrics = analysis_data.get("key_metrics", [])
            metric_data = await self.execute_metric_queries(metrics, user_id)
            
            # Step 3: Generate HTML dashboard
            html_content = await self.generate_dashboard_html(
                analysis_data, metric_data, user_id
            )
            
            return html_content
            
        except Exception as e:
            # Return error dashboard
            return self._generate_error_dashboard(str(e))
    
    def _generate_error_dashboard(self, error_message: str) -> str:
        """Generate error dashboard when generation fails"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Error</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <div class="container mx-auto p-6">
        <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            <h2 class="text-xl font-bold mb-2">Dashboard Generation Error</h2>
            <p class="mb-4">Unable to generate dashboard due to the following error:</p>
            <code class="block bg-red-200 p-2 rounded text-sm">{error_message}</code>
            <p class="mt-4 text-sm">Please check your database configuration and try again.</p>
        </div>
    </div>
</body>
</html>"""
