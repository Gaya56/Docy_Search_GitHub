from fastmcp import FastMCP
from dotenv import load_dotenv
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
import tempfile
import shutil

# Import activity tracking with graceful fallback
try:
    from .activity_tracker import activity_tracker
    TRACKING_AVAILABLE = True
except ImportError:
    TRACKING_AVAILABLE = False
    print("Activity tracking not available - running without tracking")

load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP(
    name="code_analyzer",
    version="1.0.0",
    description="Analyze external repositories for code quality and structure"
)


class RepositoryAnalyzer:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        
    def clone_repo_if_needed(self, repo_url_or_path: str) -> Optional[str]:
        """Clone repository if it's a URL, return local path"""
        if repo_url_or_path.startswith(('http://', 'https://', 'git@')):
            # It's a URL, need to clone
            temp_dir = tempfile.mkdtemp(prefix="code_analysis_")
            try:
                result = subprocess.run([
                    'git', 'clone', '--depth', '1', repo_url_or_path, temp_dir
                ], capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    return temp_dir
                else:
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    return None
            except (subprocess.TimeoutExpired, 
                   subprocess.CalledProcessError):
                shutil.rmtree(temp_dir, ignore_errors=True)
                return None
        else:
            # It's a local path
            if Path(repo_url_or_path).exists():
                return repo_url_or_path
            return None
    
    def get_repo_summary(self) -> Dict[str, Any]:
        """Get basic repository information"""
        info = {
            "name": self.repo_path.name,
            "total_files": 0,
            "has_readme": False,
            "has_git": (self.repo_path / ".git").exists(),
            "languages": {},
            "structure": []
        }
        
        # Count files and detect languages
        for file_path in self.repo_path.rglob("*"):
            if file_path.is_file():
                info["total_files"] += 1
                ext = file_path.suffix.lower()
                if ext:
                    info["languages"][ext] = info["languages"].get(ext, 0) + 1
        
        # Check for README
        readme_files = ["README.md", "readme.md", "README.txt", "README"]
        for readme in readme_files:
            if (self.repo_path / readme).exists():
                info["has_readme"] = True
                break
        
        # Get top-level structure
        for item in self.repo_path.iterdir():
            if item.name.startswith('.'):
                continue
            info["structure"].append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file"
            })
        
        return info
    
    def analyze_dependencies(self) -> Dict[str, Any]:
        """Analyze project dependencies across different languages"""
        deps = {
            "language": "unknown",
            "package_managers": [],
            "dependencies": []
        }
        
        # Python
        py_files = ["requirements.txt", "pyproject.toml", "setup.py", 
                   "Pipfile", "conda.yml"]
        for py_file in py_files:
            if (self.repo_path / py_file).exists():
                deps["language"] = "python"
                deps["package_managers"].append(py_file)
                
                if py_file == "requirements.txt":
                    try:
                        with open(self.repo_path / py_file, 'r') as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith("#"):
                                    deps["dependencies"].append(line.split('==')[0])
                    except Exception:
                        pass
        
        # JavaScript/Node.js
        if (self.repo_path / "package.json").exists():
            deps["language"] = "javascript"
            deps["package_managers"].append("package.json")
            try:
                with open(self.repo_path / "package.json", 'r') as f:
                    package_data = json.load(f)
                    if "dependencies" in package_data:
                        deps["dependencies"].extend(
                            package_data["dependencies"].keys())
            except Exception:
                pass
        
        # Java/Maven
        if (self.repo_path / "pom.xml").exists():
            deps["language"] = "java"
            deps["package_managers"].append("maven")
        
        # Java/Gradle
        gradle_files = ["build.gradle", "build.gradle.kts"]
        for gradle_file in gradle_files:
            if (self.repo_path / gradle_file).exists():
                deps["language"] = "java"
                deps["package_managers"].append("gradle")
                break
        
        return deps
    
    def analyze_code_quality(self) -> Dict[str, Any]:
        """Basic code quality analysis"""
        quality = {
            "total_lines": 0,
            "code_files": 0,
            "large_files": [],
            "file_types": {}
        }
        
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', 
                          '.cs', '.rb', '.php', '.go', '.rs'}
        
        for file_path in self.repo_path.rglob("*"):
            if (file_path.is_file() and 
                file_path.suffix.lower() in code_extensions):
                
                quality["code_files"] += 1
                ext = file_path.suffix.lower()
                quality["file_types"][ext] = quality["file_types"].get(ext, 0) + 1
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = len(f.readlines())
                        quality["total_lines"] += lines
                        
                        if lines > 500:  # Flag large files
                            quality["large_files"].append({
                                "file": str(file_path.relative_to(self.repo_path)),
                                "lines": lines
                            })
                except Exception:
                    pass
        
        return quality


@mcp.tool()
async def analyze_repository(repo_url_or_path: str) -> str:
    """
    Analyze any repository's code quality, structure, and dependencies
    
    Args:
        repo_url_or_path: GitHub URL or local path to repository
    """
    activity_id = None
    temp_path = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="analyze_repository",
                params={"repo": repo_url_or_path[:100]}
            )
            await activity_tracker.update_activity(
                activity_id,
                progress=10,
                details={"status": "Cloning repository"}
            )
        
        # Clone or validate repository
        analyzer = RepositoryAnalyzer("/tmp")
        local_path = analyzer.clone_repo_if_needed(repo_url_or_path)
        
        if not local_path:
            error_msg = f"Could not access repository: {repo_url_or_path}"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
        # Remember if we need to clean up
        temp_path = (local_path if repo_url_or_path.startswith(
            ('http://', 'https://', 'git@')) else None)
        
        # Update analyzer with correct path
        analyzer = RepositoryAnalyzer(local_path)
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=40,
                details={"status": "Analyzing structure"}
            )
        
        # Run analysis
        repo_summary = analyzer.get_repo_summary()
        dependencies = analyzer.analyze_dependencies()
        code_quality = analyzer.analyze_code_quality()
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.update_activity(
                activity_id,
                progress=80,
                details={"status": "Formatting results"}
            )
        
        # Combine results
        analysis_result = {
            "repository_url": repo_url_or_path,
            "summary": repo_summary,
            "dependencies": dependencies,
            "code_quality": code_quality,
            "recommendations": generate_recommendations(
                repo_summary, dependencies, code_quality)
        }
        
        # Clean up temporary directory
        if temp_path:
            shutil.rmtree(temp_path, ignore_errors=True)
        
        # Complete activity tracking
        if TRACKING_AVAILABLE and activity_id:
            result_preview = (
                f"Analysis completed for {repo_summary['name']} "
                f"({dependencies['language']} project)"
            )
            await activity_tracker.complete_activity(
                activity_id, result=result_preview)
        
        return json.dumps(analysis_result, indent=2, default=str)
        
    except Exception as e:
        # Clean up on error
        if temp_path:
            shutil.rmtree(temp_path, ignore_errors=True)
        
        error_msg = f"Error analyzing repository: {str(e)}"
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Analysis failed: {str(e)[:50]}")
        
        return error_msg


@mcp.tool()
async def quick_repo_summary(repo_url_or_path: str) -> str:
    """
    Get a quick summary of any repository
    
    Args:
        repo_url_or_path: GitHub URL or local path to repository
    """
    activity_id = None
    temp_path = None
    
    try:
        # Start activity tracking
        if TRACKING_AVAILABLE:
            activity_id = await activity_tracker.start_activity(
                tool_name="quick_repo_summary",
                params={"repo": repo_url_or_path[:100]}
            )
        
        # Clone or validate repository
        analyzer = RepositoryAnalyzer("/tmp")
        local_path = analyzer.clone_repo_if_needed(repo_url_or_path)
        
        if not local_path:
            error_msg = f"Could not access repository: {repo_url_or_path}"
            if TRACKING_AVAILABLE and activity_id:
                await activity_tracker.complete_activity(
                    activity_id, result=error_msg)
            return error_msg
        
        temp_path = (local_path if repo_url_or_path.startswith(
            ('http://', 'https://', 'git@')) else None)
        
        analyzer = RepositoryAnalyzer(local_path)
        
        # Get basic info only
        repo_summary = analyzer.get_repo_summary()
        dependencies = analyzer.analyze_dependencies()
        
        summary = {
            "name": repo_summary["name"],
            "language": dependencies["language"],
            "total_files": repo_summary["total_files"],
            "has_readme": repo_summary["has_readme"],
            "main_languages": dict(list(repo_summary["languages"].items())[:5]),
            "package_managers": dependencies["package_managers"]
        }
        
        # Clean up
        if temp_path:
            shutil.rmtree(temp_path, ignore_errors=True)
        
        # Complete activity tracking
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Summary for {summary['name']}")
        
        return json.dumps(summary, indent=2)
        
    except Exception as e:
        # Clean up on error
        if temp_path:
            shutil.rmtree(temp_path, ignore_errors=True)
        
        error_msg = f"Error getting repository summary: {str(e)}"
        
        if TRACKING_AVAILABLE and activity_id:
            await activity_tracker.complete_activity(
                activity_id, result=f"Summary failed: {str(e)[:50]}")
        
        return error_msg


def generate_recommendations(repo_summary: Dict, dependencies: Dict, 
                           code_quality: Dict) -> List[Dict]:
    """Generate recommendations based on analysis"""
    recommendations = []
    
    # Check for README
    if not repo_summary["has_readme"]:
        recommendations.append({
            "type": "documentation",
            "priority": "high",
            "suggestion": "Add a README.md file to document the project"
        })
    
    # Check for large files
    if code_quality["large_files"]:
        recommendations.append({
            "type": "code_quality",
            "priority": "medium",
            "suggestion": (f"Consider refactoring {len(code_quality['large_files'])} "
                          f"large files (>500 lines)")
        })
    
    # Check for package management
    if dependencies["language"] != "unknown" and not dependencies["package_managers"]:
        recommendations.append({
            "type": "dependency_management",
            "priority": "medium",
            "suggestion": f"Add dependency management for {dependencies['language']} project"
        })
    
    return recommendations


if __name__ == "__main__":
    mcp.run()
