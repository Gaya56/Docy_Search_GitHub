#!/usr/bin/env python3
"""
Simple Live Activity Demo
Tests real-time activity tracking in the UI
"""

import asyncio
import sys
import os
import time

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from activity_tracker import activity_tracker
from python_tools import python_repl

async def demo_live_activity():
    """Demo that creates activities for live UI testing"""
    
    print("🎬 Starting Live Activity Demo")
    print("=" * 50)
    print("🔧 Open Streamlit UI in another terminal: streamlit run main_ui.py")
    print("🔄 Watch the sidebar for live activity updates!")
    print("=" * 50)
    
    # Demo 1: Python execution
    print("\n1. 🐍 Testing Python execution with activity tracking...")
    result = await python_repl("print('Hello from live activity demo!')")
    print(f"   Result: {result.strip()}")
    
    # Wait between demos
    await asyncio.sleep(3)
    
    # Demo 2: Multiple activities in sequence
    print("\n2. 🔄 Creating sequence of activities...")
    
    for i in range(3):
        activity_id = await activity_tracker.start_activity(
            tool_name=f"demo_task_{i+1}",
            params={"task": f"Demo task {i+1}", "step": i+1}
        )
        
        # Simulate work with progress updates
        for progress in [25, 50, 75, 100]:
            await activity_tracker.update_activity(
                activity_id, 
                progress=progress, 
                details={"status": f"Processing step {progress//25}/4"}
            )
            await asyncio.sleep(0.5)  # Simulate work
        
        await activity_tracker.complete_activity(
            activity_id,
            result=f"Demo task {i+1} completed successfully"
        )
        
        print(f"   ✅ Completed demo task {i+1}")
        await asyncio.sleep(1)
    
    # Demo 3: Long running task
    print("\n3. ⏳ Simulating long-running task...")
    
    long_task_id = await activity_tracker.start_activity(
        tool_name="long_running_demo",
        params={"type": "simulation", "duration": "10 seconds"}
    )
    
    for i in range(10):
        progress = ((i + 1) * 10)
        await activity_tracker.update_activity(
            long_task_id,
            progress=progress,
            details={
                "status": f"Processing batch {i+1}/10",
                "elapsed": f"{i+1}s",
                "remaining": f"{10-(i+1)}s"
            }
        )
        print(f"   📊 Progress: {progress}%")
        await asyncio.sleep(1)
    
    await activity_tracker.complete_activity(
        long_task_id,
        result="Long-running simulation completed successfully"
    )
    
    print("\n4. 📊 Final activity summary:")
    summary = activity_tracker.get_activity_summary()
    print(f"   • Total activities: {summary['total_activities']}")
    print(f"   • Recent activities: {len(summary['recent'])}")
    print(f"   • Current status: {'Running' if summary.get('current') else 'Idle'}")
    
    print("\n🎉 Demo complete! Check the Streamlit UI for live updates.")
    return True

if __name__ == "__main__":
    print("🚀 Live Activity Tracking Demo")
    print("📖 Instructions:")
    print("   1. Run this demo: python demo_live_activity.py")
    print("   2. In another terminal: streamlit run main_ui.py")
    print("   3. Watch the sidebar refresh button and auto-refresh checkbox")
    print("   4. See live activity updates in real-time!")
    print()
    
    asyncio.run(demo_live_activity())
