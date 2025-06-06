# Development Tool Recommendation System - Usage Guide

This document demonstrates how to use the intelligent tool recommendation system with **enterprise-grade async memory capabilities** and **dual interface options**.

## 🚀 Getting Started

### Choose Your Interface

#### 🌐 **Web Interface (Recommended)**
```bash
streamlit run main_ui.py --server.port 8555
# Open: http://localhost:8555
```
- Beautiful chat interface with memory management
- Real-time memory statistics and health monitoring
- Async memory operations for responsive UI
- Session persistence across browser sessions
- Memory maintenance controls in sidebar

#### 🖥️ **Command Line Interface**
```bash
python app.py
```
- Terminal-based interaction with async memory integration
- Fire-and-forget memory saves for improved performance
- Same memory system and functionality as web interface
- Great for scriptable workflows and automation

## 🧠 **Enterprise Memory System (Phase 1 Complete)**

The system now features production-grade memory capabilities:

### **Async Memory Operations**
- **Non-blocking Saves**: Memory operations don't freeze the UI
- **Real-time Performance**: ~1-3ms memory save initiation vs ~5-15ms blocking saves
- **Concurrent Safety**: Multiple operations can run simultaneously
- **Error Recovery**: Comprehensive retry mechanisms and fallbacks

### **Memory Intelligence Features**
- **Context Continuity**: Builds on previous conversations with semantic search
- **Personalized Recommendations**: Learns from your tech stack preferences and feedback
- **Session Persistence**: Maintains history across application restarts  
- **Smart Context Loading**: Automatically references relevant past discussions
- **Memory Lifecycle**: Compression and archival for long-term storage optimization

### **Memory Management (Web Interface)**
Available in the Streamlit sidebar:
- **Memory Statistics**: Total memories, recent activity, database health
- **Memory Search**: Find specific past conversations
- **Maintenance Controls**: Database cleanup and optimization
- **Session Info**: Current user session and memory status

## Overview

The tool recommendation system provides:
- **🧠 Enterprise Memory**: Production-grade async memory with OpenAI embeddings
- **🚀 Performance**: Non-blocking memory operations for responsive UI
- **🔍 Semantic Search**: Find relevant past conversations automatically
- **👥 Multi-User**: Proper user isolation and session management
- **📊 Analytics**: Memory statistics and database health monitoring
- **🔄 Migration**: Automatic updates for existing installations
- **Live Tool Search**: Using Brave API for current tool discovery
- **AI-Powered Analysis**: Gemini AI evaluates tools for relevance, reliability, and ease of use
- **Installation Guides**: Automatic generation of installation instructions
- **Comparative Analysis**: Side-by-side tool comparisons
- **Task-Specific Recommendations**: Curated tool suggestions for specific development workflows

## Available Functions

### Core Tool Recommendation Functions

All functions now benefit from async memory integration and contextual awareness from previous conversations:

### 1. `search_tools(query, category)`
Search for tools with intelligent categorization and memory-enhanced recommendations.

**Enhanced with Memory Context:**
- Remembers your preferred tool types and past searches
- Avoids suggesting tools you've already rejected
- Builds on previous technology stack discussions

**Example Queries:**
```
search_tools("React component library", "web")
search_tools("mobile app framework", "mobile")
search_tools("database management", "database")
search_tools("CI/CD pipeline", "devops")
```

### 2. `analyze_tools(search_results, requirements)`
AI analysis and ranking of search results.

**Example:**
```
analyze_tools("[search results from previous query]", "Need tools for full-stack web development, beginner-friendly")
```

### 3. `get_installation_guide(tool_name, os_type)`
Generate comprehensive installation instructions.

**Example:**
```
get_installation_guide("Node.js", "ubuntu")
get_installation_guide("Docker", "linux")
get_installation_guide("VS Code", "windows")
```

### 4. `recommend_tools_for_task(task_description, skill_level)`
Get curated tool recommendations for specific tasks.

**Example:**
```
recommend_tools_for_task("building a React web application", "intermediate")
recommend_tools_for_task("mobile app development for iOS and Android", "beginner")
recommend_tools_for_task("DevOps automation and deployment", "advanced")
```

### 5. `compare_tools(tool_names)`
Detailed side-by-side comparison of multiple tools.

**Example:**
```
compare_tools("React, Vue.js, Angular")
compare_tools("Docker, Podman, LXC")
compare_tools("PostgreSQL, MySQL, MongoDB")
```

## Usage in Chat Interface

### Basic Tool Discovery
```
User: "I need tools for React web development"
Bot: I'll search for React development tools and provide recommendations...
[Uses search_tools and analyze_tools automatically]
```

### Installation Help
```
User: "How do I install Node.js on Ubuntu?"
Bot: I'll generate an installation guide for Node.js on Ubuntu...
[Uses get_installation_guide automatically]
```

### Task-Specific Recommendations
```
User: "What tools should a beginner use for web development?"
Bot: I'll recommend beginner-friendly web development tools...
[Uses recommend_tools_for_task with skill_level="beginner"]
```

### Tool Comparison
```
User: "Compare React vs Vue.js for frontend development"
Bot: I'll provide a detailed comparison of React and Vue.js...
[Uses compare_tools automatically]
```

## Advanced Features

### Category-Based Search
The system supports intelligent categorization:
- **web**: Web development frameworks and tools
- **mobile**: Mobile app development platforms
- **desktop**: Desktop application frameworks
- **database**: Database management systems
- **devops**: DevOps and deployment tools
- **testing**: Testing frameworks and tools
- **design**: Design and UI/UX tools
- **data**: Data science and analytics tools
- **ai**: AI and machine learning frameworks
- **game**: Game development engines and tools
- **security**: Security tools and libraries
- **productivity**: Development productivity tools

### AI-Powered Analysis Criteria
Tools are evaluated based on:
1. **Relevance** (1-10 score)
2. **Reliability and maturity**
3. **Installation complexity** (Easy/Medium/Hard)
4. **Community support**
5. **Documentation quality**
6. **Security and trust factors**

### Multi-Platform Support
The system provides recommendations for:
- Different operating systems (Windows, macOS, Linux)
- Various development environments
- Cloud-based and local development tools

## Example Workflows

### 1. Full-Stack Web Development
```
1. "What tools do I need for full-stack web development?"
2. "Compare React vs Vue.js vs Angular"
3. "How do I set up a Node.js development environment?"
4. "Recommend database options for a web application"
```

### 2. Mobile App Development
```
1. "I need tools for cross-platform mobile development"
2. "What's the best alternative to native iOS/Android development?"
3. "Compare React Native vs Flutter vs Xamarin"
4. "Install guide for setting up Flutter development"
```

### 3. DevOps and Deployment
```
1. "Set up a complete CI/CD pipeline"
2. "Best containerization tools for microservices"
3. "Compare Docker vs Podman for container management"
4. "Recommend monitoring tools for production applications"
```

## Configuration

Ensure your `.env` file contains:
```
BRAVE_API_KEY=your_brave_search_api_key
GOOGLE_API_KEY=your_gemini_api_key
AI_MODEL=gemini  # or openai, claude, deepseek
```

## Benefits

1. **Always Current**: Live search ensures recommendations include latest tools
2. **AI-Driven**: Intelligent analysis beyond simple search results
3. **Practical Focus**: Installation guides and real-world usage
4. **Skill-Aware**: Recommendations adapted to user experience level
5. **Development-Focused**: Tailored for software development workflows
6. **Extensible**: Modular architecture allows easy addition of new capabilities
