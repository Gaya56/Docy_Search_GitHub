# Intelligent Tool Recommendation System

This repository contains an intelligent, context-aware tool recommendation system designed to help developers discover, analyze, and implement the best technical tools for their specific projects. The system combines live web search (via Brave API), AI-powered analysis (via Gemini API), and GitHub repository integration to provide comprehensive tool recommendations with installation guides and official source code access. Built on a clean, modular architecture using Pydantic AI and the Model Context Protocol (MCP), it reads your project context from a markdown file to provide personalized suggestions based on your tech stack, budget constraints, and development goals. The chatbot interface asks for permission before accessing external APIs, searches for relevant tools, ranks them by relevance and reliability, finds their official GitHub repositories, and provides complete setup instructions - transforming the often overwhelming process of tool selection into an intelligent, streamlined workflow that understands your specific development needs.

## 🚀 Key Features

### Tool Recommendation Engine

- **Live Web Search**: Uses Brave API for current tool discovery
- **AI-Powered Analysis**: Gemini AI evaluates tools for relevance, reliability, and ease of use
- **Smart Rankings**: Tools ranked based on multiple criteria including community support and security
- **Installation Guides**: Automatic generation of official installation instructions
- **Comparative Analysis**: Side-by-side tool comparisons
- **Task-Specific Recommendations**: Curated suggestions for specific development workflows

### GitHub Integration

- **Repository Discovery**: Search for official GitHub repositories of recommended tools
- **Code Examples**: Access real implementation examples and setup files
- **Project Structure Analysis**: View repository structure and key files
- **Direct Links**: Get direct links to GitHub repositories and documentation
- **Permission-Based Access**: Secure GitHub integration with user consent

### Development Tool Discovery

- **Multi-Category Support**: Web development, mobile apps, desktop applications, databases, DevOps, testing, design, data science, AI/ML, game development, security, and productivity tools
- **Framework Recommendations**: React, Vue.js, Angular, Django, Flask, Express.js, and more
- **Tool Comparison**: Side-by-side analysis of similar tools
- **Technology Stack Guidance**: Complete toolchain recommendations for specific project types

### Project Context Awareness

- **Smart Context Loading**: Automatically loads your project details from `project_context.md`
- **Targeted Recommendations**: Suggests tools based on your specific tech stack, challenges, and goals
- **Budget-Aware Suggestions**: Considers your budget constraints and preferences
- **Skill-Level Appropriate**: Recommendations matched to your experience level

### Multi-AI Support

- **OpenAI GPT Models** (default)
- **Anthropic Claude**
- **Google Gemini**
- **DeepSeek** (via OpenAI API)

## 🛠 Architecture

Built on **Pydantic AI** and **Model Context Protocol (MCP)** for clean, modular design:

```text
app.py                          # Main chat interface with project context loading
tool_recommendation/
└── mcp_server.py              # 🆕 Intelligent tool discovery & analysis
github_mcp_server.py           # 🆕 GitHub repository integration
brave_search.py                # Brave API integration
python_tools.py                # Data processing utilities
project_context.md             # Your project details (auto-loaded)
```

**Current Status:** Fully operational system with intelligent tool recommendation, GitHub integration, multi-AI support, interactive chat with permission prompts, project context awareness, and comprehensive development tool analysis capabilities.

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Docy_Search

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file with your API keys:

```env
# Required for tool recommendation system
BRAVE_API_KEY=your_brave_search_api_key
GOOGLE_API_KEY=your_gemini_api_key

# Required for GitHub integration
GITHUB_TOKEN=your_github_token

# Optional: Choose your preferred AI model
AI_MODEL=gemini  # Options: openai, claude, gemini, deepseek

# Add other API keys as needed
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_claude_key
```

### 3. Set Up Project Context (Optional)

Create a `project_context.md` file with details about your project:

```bash
# Copy the example and customize it
cp project_context_example.md project_context.md
# Edit with your project details
nano project_context.md
```

The assistant will automatically load this context and provide more targeted recommendations based on your specific project, tech stack, and goals.

### 4. Test the System

```bash
# Test tool recommendation functionality
python tests/test_tool_recommendation.py

# Test GitHub integration
python tests/test_github_server.py

# Run demo examples
python demos/demo_tool_recommendation.py

# Start the interactive chat
python app.py
```

## 💡 Usage Examples

### Tool Discovery & Recommendations

```text
User: "I need tools for React web development"
Bot: I'll search for React development tools and analyze the best options...

User: "Compare Vue.js vs Angular"
Bot: I'll provide a detailed comparison of these JavaScript frameworks...

User: "How do I set up a Django project?"
Bot: I'll generate step-by-step setup instructions for Django development...
```

### GitHub Integration

```text
User: "Find the official React repository and show me setup examples"
Bot: I can search GitHub repositories for React setup examples. This will access public GitHub data to find official repositories and code examples. Continue? (y/n)

User: "y"
Bot: [Shows React repository details, stars, and relevant setup files]
```

### Development Workflows

```text
User: "What's the best database for a Node.js project?"
Bot: I'll recommend databases that work well with Node.js and provide setup guides...

User: "Set up a complete full-stack development environment"
Bot: I'll suggest tools and provide setup instructions for frontend, backend, and database tools...
```

### Project Context-Aware Recommendations

```text
User: "What tools would be best for this project?"
Bot: ✅ I have your project context loaded and ready to help!
     Based on your task management app with React + Node.js + PostgreSQL...
     [Provides targeted recommendations for your specific stack and challenges]
```

## 🔧 Advanced Features

### Tool Categories

- **Web Development**: React, Vue.js, Angular, Django, Flask, Express.js
- **Mobile Development**: React Native, Flutter, Xamarin, Ionic
- **Desktop Applications**: Electron, Tauri, Qt, .NET
- **Databases**: PostgreSQL, MongoDB, Redis, MySQL, SQLite
- **DevOps**: Docker, Kubernetes, Jenkins, GitLab CI, Terraform
- **Testing**: Jest, Pytest, Selenium, Cypress, Postman
- **Design**: Figma, Sketch, Adobe XD, Canva, GIMP
- **Data Science**: Pandas, NumPy, Jupyter, Tableau, Power BI
- **AI/ML**: TensorFlow, PyTorch, Scikit-learn, Keras
- **Game Development**: Unity, Unreal Engine, Godot, Phaser
- **Security**: OWASP tools, security scanners, encryption libraries
- **Productivity**: VS Code, Git, Slack, Notion, Trello

### AI-Powered Analysis

Each tool recommendation includes:

- **Relevance Score** (1-10)
- **Reliability Assessment**
- **Installation Complexity** (Easy/Medium/Hard)
- **Community Support Rating**
- **Security & Trust Evaluation**
- **Use Case Scenarios**

### Integration Benefits

- **Live Data**: Always current tool information via Brave Search
- **Smart Analysis**: AI evaluates beyond simple search results
- **Practical Focus**: Real installation guides and usage tips
- **Skill-Adaptive**: Recommendations match user experience level
- **Development-Focused**: Tailored for software development workflows

## 📁 File Structure

```text
Docy_Search/
├── app.py                              # Main application with context loading
├── github_mcp_server.py               # GitHub repository integration
├── brave_search.py                    # Search API integration
├── python_tools.py                    # Utility functions
├── project_context.md                 # Your project details (auto-loaded)
├── requirements.txt                   # Dependencies
├── .env                              # API keys (create this)
├── tool_recommendation/
│   ├── mcp_server.py                 # Core recommendation engine
│   ├── search_engine.py              # Search functionality
│   ├── analyzer.py                   # AI analysis tools
│   ├── installer.py                  # Installation guides
│   ├── core.py                       # Core logic
│   └── models.py                     # Data models
├── tests/
│   ├── test_tool_recommendation.py   # Tool recommendation tests
│   └── test_github_server.py         # GitHub integration tests
├── demos/
│   ├── demo_tool_recommendation.py   # Demo script
│   └── demo_tool_recommendation_fixed.py
└── Docs/
    ├── Tool_Recommendation_Guide.md   # Detailed usage guide
    ├── IMPLEMENTATION_SUMMARY.md      # Technical implementation details
    ├── project_context_example.md     # Example project context
    └── Workflow.md                    # Development workflow
```

## 🤝 Contributing

This project uses a modular MCP (Model Context Protocol) architecture. To add new functionality:

1. Create new MCP server in appropriate directory
2. Follow the existing pattern (see `tool_recommendation/mcp_server.py` or `github_mcp_server.py`)
3. Add server to `app.py`
4. Update system prompt if needed

### Key Components:

- **MCP Servers**: Modular tools for specific functionality (tool search, GitHub integration, etc.)
- **Project Context**: Automatic loading of user project details for targeted recommendations
- **Permission System**: User consent required for external API calls (GitHub, web search)
- **Multi-AI Support**: Flexible AI model selection for different use cases

For detailed usage examples, see `Docs/Tool_Recommendation_Guide.md`.

## 🎯 System Capabilities

### ✅ Fully Implemented Features:

- **🔍 Tool Discovery**: Live web search with AI-powered analysis
- **📊 Smart Rankings**: Multi-criteria tool evaluation and comparison
- **📚 Installation Guides**: Automatic generation of setup instructions
- **🐙 GitHub Integration**: Repository search, code examples, and project analysis
- **🎯 Context Awareness**: Project-specific recommendations based on your details
- **🔐 Permission System**: Secure API access with user consent
- **🤖 Multi-AI Support**: OpenAI, Claude, Gemini, and DeepSeek compatibility
- **📱 Category Support**: Web, mobile, desktop, database, DevOps, testing, design, data science, AI/ML, game development, security, productivity

### 🚀 Ready to Use:

Your intelligent development assistant is ready to help with tool discovery, GitHub repository analysis, and project-specific recommendations. Simply run `python app.py` and start asking questions about development tools!

