# docy_search/dashboard/prompts.py
"""Dashboard generation prompts"""

ANALYZE_SCHEMA_PROMPT = """Analyze the database schema and provide a JSON report:

1. Identify the domain (sales, HR, inventory, etc.)
2. List key metrics/KPIs for this domain
3. For each metric provide:
   - name
   - description
   - visualization_type (bar_chart, line_chart, pie_chart, table)
   - sql query

Return ONLY valid JSON:
{
  "domain": "identified domain",
  "key_metrics": [
    {
      "metric": "name",
      "description": "what it shows",
      "visualization_type": "chart_type",
      "sql": "SELECT..."
    }
  ]
}"""

GENERATE_HTML_PROMPT = """Create a responsive HTML dashboard using:
- Chart.js for visualizations
- Tailwind CSS for styling
- The provided metrics data

Include:
- Header with dashboard title
- Grid layout for charts
- Responsive design for mobile/desktop
- Loading states for charts
- Error handling

Return ONLY the complete HTML document with embedded CSS and JavaScript.
Make it professional and modern looking."""
