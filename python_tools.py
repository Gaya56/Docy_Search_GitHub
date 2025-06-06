from mcp.server.fastmcp import FastMCP
import io
import base64
import matplotlib.pyplot as plt
import sys
from io import StringIO
import traceback

# Import activity tracking with graceful fallback
try:
    from activity_tracker import activity_tracker
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    print("Activity tracking not available - running without tracking")

mcp = FastMCP("python_tools")

class PythonREPL:
    def run(self, code):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        
        try:
            exec(code, globals())
            sys.stdout = old_stdout
            return redirected_output.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            return f"Error: {str(e)}\n{traceback.format_exc()}"

repl = PythonREPL()

@mcp.tool()
async def python_repl(code: str) -> str:
    """Execute Python code."""
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="python_repl",
                params={"code_preview": code[:100] + "..." if len(code) > 100 else code}
            )
            await activity_tracker.update_activity(activity_id, progress=50, details={"status": "Executing Python code"})
        
        result = repl.run(code)
        
        # Complete activity tracking with success
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"Python code executed: {len(code)} chars -> {len(result)} chars output"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return result
    except Exception as e:
        error_msg = f"Error executing Python code: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"Python execution error: {str(e)[:100]}")
        return error_msg

@mcp.tool()
async def data_visualization(code: str) -> str:
    """Execute Python code. Use matplotlib for visualization."""
    activity_id = None
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="data_visualization",
                params={"code_preview": code[:100] + "..." if len(code) > 100 else code}
            )
            await activity_tracker.update_activity(activity_id, progress=30, details={"status": "Executing visualization code"})
        
        repl.run(code)
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(activity_id, progress=70, details={"status": "Generating chart image"})
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_str = base64.b64encode(buf.getvalue()).decode()
        plt.close()  # Close the figure to free memory
        
        # Complete activity tracking with success
        if TRACKING_AVAILABLE and activity_id:
            result_preview = f"Generated visualization chart from {len(code)} chars of code"
            await activity_tracker.complete_activity(activity_id, result=result_preview)
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        error_msg = f"Error creating chart: {str(e)}"
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(activity_id, result=f"Visualization error: {str(e)[:100]}")
        return error_msg

if __name__ == "__main__":
    mcp.run()