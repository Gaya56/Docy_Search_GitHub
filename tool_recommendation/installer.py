"""
Installation guide generator for recommended tools.
"""
import re
from typing import Dict, List, Optional
from .models import (
    ToolRecommendation, Platform, InstallationMethod, 
    InstallationGuide
)


class InstallationGuideGenerator:
    """
    Generates detailed installation guides for recommended tools.
    """
    
    def __init__(self):
        self.platform_commands = self._initialize_platform_commands()
        self.common_prerequisites = self._initialize_prerequisites()
    
    def generate_guide(
        self, 
        tool: ToolRecommendation, 
        platform: Platform,
        method: Optional[InstallationMethod] = None
    ) -> InstallationGuide:
        """
        Generate a detailed installation guide for a specific tool and platform.
        """
        # Determine best installation method if not specified
        if not method:
            method = self._determine_best_method(tool, platform)
        
        # Generate the guide
        guide = InstallationGuide(
            tool_name=tool.name,
            platform=platform,
            method=method,
            steps=self._generate_installation_steps(tool, platform, method),
            prerequisites=self._get_prerequisites(tool, platform, method),
            post_install_notes=self._get_post_install_notes(tool, platform),
            troubleshooting=self._get_troubleshooting_tips(tool, platform, method),
            verification_command=self._get_verification_command(tool, method)
        )
        
        return guide
    
    def _determine_best_method(
        self, 
        tool: ToolRecommendation, 
        platform: Platform
    ) -> InstallationMethod:
        """
        Determine the best installation method for a tool on a specific platform.
        """
        available_methods = tool.installation_methods.get(platform, [])
        
        if not available_methods:
            # Fallback based on platform
            fallback_methods = {
                Platform.LINUX: InstallationMethod.APT,
                Platform.MACOS: InstallationMethod.BREW,
                Platform.WINDOWS: InstallationMethod.BINARY,
                Platform.PYTHON: InstallationMethod.PIP,
                Platform.DOCKER: InstallationMethod.DOCKER
            }
            return fallback_methods.get(platform, InstallationMethod.SOURCE)
        
        # Priority order for different platforms
        priority_orders = {
            Platform.LINUX: [
                InstallationMethod.APT, InstallationMethod.SNAP, 
                InstallationMethod.PIP, InstallationMethod.DOCKER,
                InstallationMethod.BINARY, InstallationMethod.SOURCE
            ],
            Platform.MACOS: [
                InstallationMethod.BREW, InstallationMethod.PIP,
                InstallationMethod.BINARY, InstallationMethod.SOURCE
            ],
            Platform.WINDOWS: [
                InstallationMethod.PACKAGE_MANAGER, InstallationMethod.BINARY,
                InstallationMethod.PIP, InstallationMethod.SOURCE
            ]
        }
        
        priority = priority_orders.get(platform, available_methods)
        
        for method in priority:
            if method in available_methods:
                return method
        
        return available_methods[0]  # Return first available if no priority match
    
    def _generate_installation_steps(
        self, 
        tool: ToolRecommendation, 
        platform: Platform, 
        method: InstallationMethod
    ) -> List[str]:
        """
        Generate step-by-step installation instructions.
        """
        steps = []
        
        # Get custom command if available
        custom_key = f"{platform.value}_{method.value}"
        if custom_key in tool.installation_commands:
            command = tool.installation_commands[custom_key]
            steps.extend(self._format_custom_command_steps(command, method))
            return steps
        
        # Generate based on method
        if method == InstallationMethod.APT:
            steps = [
                "Update package list:",
                "sudo apt update",
                f"Install {tool.name}:",
                f"sudo apt install -y {self._normalize_package_name(tool.name)}"
            ]
        
        elif method == InstallationMethod.BREW:
            steps = [
                f"Install {tool.name} using Homebrew:",
                f"brew install {self._normalize_package_name(tool.name)}"
            ]
        
        elif method == InstallationMethod.PIP:
            steps = [
                f"Install {tool.name} using pip:",
                f"pip install {self._normalize_package_name(tool.name)}",
                "Or with user installation:",
                f"pip install --user {self._normalize_package_name(tool.name)}"
            ]
        
        elif method == InstallationMethod.DOCKER:
            steps = [
                f"Pull {tool.name} Docker image:",
                f"docker pull {self._normalize_docker_name(tool.name)}",
                f"Run {tool.name} container:",
                f"docker run -it {self._normalize_docker_name(tool.name)}"
            ]
        
        elif method == InstallationMethod.SNAP:
            steps = [
                f"Install {tool.name} using Snap:",
                f"sudo snap install {self._normalize_package_name(tool.name)}"
            ]
        
        elif method == InstallationMethod.NPM:
            steps = [
                f"Install {tool.name} globally using npm:",
                f"npm install -g {self._normalize_package_name(tool.name)}"
            ]
        
        elif method == InstallationMethod.BINARY:
            steps = [
                f"Download {tool.name} binary:",
                f"Visit: {tool.url}",
                "Download the appropriate binary for your system",
                "Extract the archive (if compressed)",
                "Move binary to a directory in your PATH:",
                f"sudo mv {tool.name} /usr/local/bin/",
                "Make executable:",
                f"sudo chmod +x /usr/local/bin/{tool.name}"
            ]
        
        elif method == InstallationMethod.SOURCE:
            steps = [
                f"Clone {tool.name} repository:",
                f"git clone {tool.github_url or tool.url}",
                f"cd {self._normalize_package_name(tool.name)}",
                "Follow build instructions in README.md",
                "Typically:",
                "make",
                "sudo make install"
            ]
        
        else:
            steps = [
                f"Visit the official {tool.name} website:",
                tool.url,
                "Follow the installation instructions for your platform"
            ]
        
        return steps
    
    def _format_custom_command_steps(
        self, 
        command: str, 
        method: InstallationMethod
    ) -> List[str]:
        """
        Format custom installation commands into steps.
        """
        steps = []
        
        # Split commands by common separators
        commands = re.split(r'[;&\n]', command)
        commands = [cmd.strip() for cmd in commands if cmd.strip()]
        
        for i, cmd in enumerate(commands):
            if cmd.startswith('sudo') or cmd.startswith('apt') or cmd.startswith('brew'):
                steps.append(f"Step {i+1}: Run the following command:")
                steps.append(cmd)
            else:
                steps.append(cmd)
        
        return steps
    
    def _get_prerequisites(
        self, 
        tool: ToolRecommendation, 
        platform: Platform, 
        method: InstallationMethod
    ) -> List[str]:
        """
        Get prerequisites for installation.
        """
        prerequisites = []
        
        # Method-specific prerequisites
        method_prereqs = self.common_prerequisites.get(method, [])
        prerequisites.extend(method_prereqs)
        
        # Platform-specific prerequisites
        if platform == Platform.LINUX:
            prerequisites.append("Administrative (sudo) privileges")
        elif platform == Platform.MACOS:
            if method == InstallationMethod.BREW:
                prerequisites.append("Homebrew package manager")
        elif platform == Platform.WINDOWS:
            prerequisites.append("Windows PowerShell or Command Prompt")
        
        # Language-specific prerequisites
        if tool.language:
            lang = tool.language.lower()
            if lang == "python":
                prerequisites.append("Python 3.6 or higher")
            elif lang == "node" or lang == "javascript":
                prerequisites.append("Node.js and npm")
            elif lang == "go":
                prerequisites.append("Go programming language")
            elif lang == "rust":
                prerequisites.append("Rust programming language")
        
        return list(set(prerequisites))  # Remove duplicates
    
    def _get_post_install_notes(
        self, 
        tool: ToolRecommendation, 
        platform: Platform
    ) -> List[str]:
        """
        Get post-installation notes and tips.
        """
        notes = []
        
        # Add PATH notes for binary installations
        if platform in [Platform.LINUX, Platform.MACOS]:
            notes.append("Ensure the installation directory is in your PATH")
        
        # Add documentation references
        if tool.documentation_url:
            notes.append(f"Read the documentation: {tool.documentation_url}")
        
        # Category-specific notes
        if tool.category.value == "cybersecurity":
            notes.append("Some security tools may require elevated privileges to run")
            notes.append("Check your system's security policies before use")
        
        return notes
    
    def _get_troubleshooting_tips(
        self, 
        tool: ToolRecommendation, 
        platform: Platform, 
        method: InstallationMethod
    ) -> Dict[str, str]:
        """
        Get common troubleshooting tips.
        """
        tips = {}
        
        # Method-specific troubleshooting
        if method == InstallationMethod.APT:
            tips["Package not found"] = "Try 'sudo apt update' first, or check if the package name is correct"
            tips["Permission denied"] = "Use 'sudo' before the apt command"
        
        elif method == InstallationMethod.PIP:
            tips["Permission denied"] = "Try 'pip install --user' or use a virtual environment"
            tips["Package not found"] = "Check the exact package name on PyPI"
        
        elif method == InstallationMethod.BREW:
            tips["Command not found"] = "Install Homebrew first: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
            tips["Formula not found"] = "Try 'brew search' to find the correct formula name"
        
        # Platform-specific troubleshooting
        if platform == Platform.LINUX:
            tips["Command not found after install"] = "Check if the binary is in your PATH, or restart your terminal"
        
        elif platform == Platform.WINDOWS:
            tips["Command not recognized"] = "Add the installation directory to your System PATH"
        
        return tips
    
    def _get_verification_command(
        self, 
        tool: ToolRecommendation, 
        method: InstallationMethod
    ) -> Optional[str]:
        """
        Get command to verify successful installation.
        """
        tool_name = self._normalize_package_name(tool.name)
        
        # Common verification patterns
        common_verifications = [
            f"{tool_name} --version",
            f"{tool_name} -v",
            f"{tool_name} version",
            f"{tool_name} --help"
        ]
        
        # Return the most likely verification command
        return common_verifications[0]
    
    def _normalize_package_name(self, name: str) -> str:
        """
        Normalize tool name for package managers.
        """
        # Convert to lowercase and replace spaces with hyphens
        normalized = name.lower().replace(" ", "-")
        # Remove special characters except hyphens and underscores
        normalized = re.sub(r'[^a-z0-9\-_]', '', normalized)
        return normalized
    
    def _normalize_docker_name(self, name: str) -> str:
        """
        Normalize tool name for Docker.
        """
        # Docker image names are usually lowercase
        return self._normalize_package_name(name)
    
    def _initialize_platform_commands(self) -> Dict[str, Dict[str, str]]:
        """
        Initialize platform-specific command templates.
        """
        return {
            Platform.LINUX.value: {
                InstallationMethod.APT.value: "sudo apt update && sudo apt install -y {package}",
                InstallationMethod.SNAP.value: "sudo snap install {package}",
                InstallationMethod.PIP.value: "pip install {package}"
            },
            Platform.MACOS.value: {
                InstallationMethod.BREW.value: "brew install {package}",
                InstallationMethod.PIP.value: "pip install {package}"
            },
            Platform.WINDOWS.value: {
                InstallationMethod.PIP.value: "pip install {package}"
            }
        }
    
    def _initialize_prerequisites(self) -> Dict[InstallationMethod, List[str]]:
        """
        Initialize common prerequisites for installation methods.
        """
        return {
            InstallationMethod.APT: ["Ubuntu/Debian-based Linux distribution"],
            InstallationMethod.BREW: ["macOS", "Homebrew package manager"],
            InstallationMethod.PIP: ["Python 3.x", "pip package manager"],
            InstallationMethod.NPM: ["Node.js", "npm package manager"],
            InstallationMethod.DOCKER: ["Docker installed and running"],
            InstallationMethod.SOURCE: ["Git", "Build tools (gcc, make)"],
            InstallationMethod.SNAP: ["Linux distribution with snap support"]
        }
