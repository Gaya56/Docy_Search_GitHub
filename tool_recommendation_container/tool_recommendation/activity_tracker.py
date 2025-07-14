"""
Real-time activity tracking for all system operations
"""
from datetime import datetime
from typing import Dict, List, Optional, Any
import asyncio
import json


class ActivityTracker:
    """Track all system activities in real-time"""
    
    def __init__(self):
        self.current_activity: Optional[Dict[str, Any]] = None
        self.activity_log: List[Dict[str, Any]] = []
        self.resource_access = {
            "files": [],
            "websites": [],
            "repos": [],
            "api_calls": {"brave": 0, "github": 0, "openai": 0, "gemini": 0}
        }
        self._activity_id = 0
    
    async def start_activity(self, tool_name: str, params: Dict[str, Any]) -> int:
        """Start tracking a new activity"""
        self._activity_id += 1
        
        activity = {
            "id": self._activity_id,
            "tool": tool_name,
            "action": self._get_action_description(tool_name, params),
            "params": params,
            "start_time": datetime.now(),
            "time_str": datetime.now().strftime("%H:%M:%S"),
            "status": "running",
            "progress": 0.0,
            "details": {}
        }
        
        self.current_activity = activity
        self.activity_log.append(activity)
        
        # Track resource access
        self._track_resource_access(tool_name, params)
        
        return self._activity_id
    
    async def update_activity(self, activity_id: int, progress: float, details: Optional[Dict] = None):
        """Update activity progress"""
        if self.current_activity and self.current_activity["id"] == activity_id:
            self.current_activity["progress"] = progress
            if details:
                self.current_activity["details"].update(details)
    
    async def complete_activity(self, activity_id: int, result: Optional[str] = None):
        """Mark activity as complete"""
        if self.current_activity and self.current_activity["id"] == activity_id:
            self.current_activity["status"] = "complete"
            self.current_activity["progress"] = 1.0
            self.current_activity["end_time"] = datetime.now()
            self.current_activity["duration"] = (
                self.current_activity["end_time"] - self.current_activity["start_time"]
            ).total_seconds()
            if result:
                self.current_activity["result_preview"] = result[:100] + "..." if len(result) > 100 else result
    
    def _get_action_description(self, tool_name: str, params: Dict[str, Any]) -> str:
        """Generate human-readable action description"""
        descriptions = {
            'search_tools': f"🔍 Searching: {params.get('query', '')[:30]}...",
            'search_web': f"🌐 Web search: {params.get('query', '')[:30]}...",
            'analyze_tools': "🤖 Analyzing search results",
            'get_installation_guide': f"📋 Getting install guide: {params.get('tool_name', '')}",
            'compare_tools': f"⚖️ Comparing: {params.get('tool_names', '')}",
            'search_github_repositories': f"🐙 GitHub search: {params.get('query', '')}",
            'get_repository_structure': f"📁 Exploring: {params.get('repo_full_name', '')}",
            'get_file_from_repository': f"📄 Reading: {params.get('file_path', '')}",
            'save_memory': "💾 Saving to memory",
            'retrieve_memories': "🧠 Loading memories"
        }
        return descriptions.get(tool_name, f"🔧 {tool_name}")
    
    def _track_resource_access(self, tool_name: str, params: Dict[str, Any]):
        """Track what resources are being accessed"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Track file access
        if "file_path" in params:
            self.resource_access["files"].append({
                "path": params["file_path"],
                "time": timestamp,
                "tool": tool_name
            })
        
        # Track website access
        if tool_name in ["search_web", "search_tools"]:
            self.resource_access["websites"].append({
                "query": params.get("query", ""),
                "time": timestamp,
                "results": params.get("num_results", 5)
            })
            self.resource_access["api_calls"]["brave"] += 1
        
        # Track GitHub access
        if "github" in tool_name.lower():
            repo = params.get("repo_full_name", params.get("query", ""))
            self.resource_access["repos"].append({
                "repo": repo,
                "time": timestamp,
                "action": tool_name
            })
            self.resource_access["api_calls"]["github"] += 1
        
        # Track AI API calls
        if tool_name == "analyze_tools":
            self.resource_access["api_calls"]["gemini"] += 1
        elif tool_name == "save_memory":
            self.resource_access["api_calls"]["openai"] += 1
    
    def get_activity_summary(self) -> Dict[str, Any]:
        """Get summary of all activities"""
        return {
            "current": self.current_activity,
            "recent": self.activity_log[-10:],
            "resources": self.resource_access,
            "total_activities": len(self.activity_log)
        }


# Global instance
activity_tracker = ActivityTracker()