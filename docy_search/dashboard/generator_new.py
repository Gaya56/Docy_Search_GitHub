# docy_search/dashboard/generator.py
"""Dashboard generation orchestration"""
import json
from typing import Dict, Any, Optional
from datetime import datetime

from docy_search.activity_tracker import activity_tracker
from docy_search.database import SQLAgent, MCPSQLConnection
from mcp import ClientSession
from pydantic_ai import Agent
from pydantic_ai.tools.mcp import MCPTools

from .prompts import ANALYZE_SCHEMA_PROMPT, GENERATE_HTML_PROMPT
from .validators import validate_schema_analysis, clean_json_response


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
            await activity_tracker.update_activity(activity_id, 0.2, {"status": "Analyzing schema"})
            schema_analysis = await self._analyze_database_schema()
            
            # Step 2: Fetch metric data
            await activity_tracker.update_activity(activity_id, 0.5, {"status": "Fetching metrics"})
            metrics_data = await self._fetch_metrics_data(schema_analysis)
            
            # Step 3: Generate HTML
            await activity_tracker.update_activity(activity_id, 0.8, {"status": "Generating HTML"})
            html_content = await self._generate_html(metrics_data)
            
            await activity_tracker.complete_activity(activity_id, "Dashboard generated")
            return html_content
            
        except Exception as e:
            await activity_tracker.complete_activity(activity_id, f"Failed: {str(e)}")
            raise
    
    async def _analyze_database_schema(self) -> Dict[str, Any]:
        """Analyze database and identify metrics"""
        async with await MCPSQLConnection.create_session() as (read, write):
            async with ClientSession(read, write) as session:
                mcp_tools = MCPTools(session=session)
                await mcp_tools.initialize()
                
                agent = Agent(
                    self.model,
                    tools=[mcp_tools],
                    system_prompt=ANALYZE_SCHEMA_PROMPT
                )
                
                result = await agent.run("Analyze the database schema")
                cleaned = clean_json_response(result.output)
                return validate_schema_analysis(cleaned)
    
    async def _fetch_metrics_data(self, schema_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute SQL queries for each metric"""
        metrics_with_data = {"metrics": []}
        
        for metric in schema_analysis["key_metrics"]:
            try:
                data = await self.sql_agent.query(f"Execute this SQL: {metric['sql']}")
                # Parse result as JSON if possible
                try:
                    parsed_data = json.loads(data)
                except:
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
        agent = Agent(
            self.model,
            system_prompt=GENERATE_HTML_PROMPT
        )
        
        result = await agent.run(json.dumps(metrics_data))
        
        # Clean HTML response
        html = result.output
        if "```html" in html:
            html = html.split("```html")[1].split("```")[0]
        
        return html.strip()
