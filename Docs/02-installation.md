# Installation & Setup Guide

## 📋 Requirements

### System Requirements
- **Python**: 3.11 or higher
- **Operating System**: Windows, macOS, or Linux
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 500MB free space

### API Keys (Optional but Recommended)
- **Required for Full Functionality**:
  - `OPENAI_API_KEY` - For AI analysis and embeddings
  - `BRAVE_API_KEY` - For web search capabilities
- **Optional**:
  - `ANTHROPIC_API_KEY` - For Claude model access
  - `GOOGLE_API_KEY` - For Gemini model access
  - `GITHUB_TOKEN` - For enhanced GitHub API limits
  - `DEEPSEEK_API_KEY` - For DeepSeek model access

## 🚀 Quick Installation

### Option 1: UV Package Manager (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Docy_Search_GitHub.git
cd Docy_Search_GitHub

# 2. Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
# or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 3. Install dependencies
uv sync

# 4. Set up environment variables (optional)
cp .env.example .env
# Edit .env with your API keys
```

### Option 2: Traditional Pip Installation
```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Docy_Search_GitHub.git
cd Docy_Search_GitHub

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables (optional)
cp .env.example .env
# Edit .env with your API keys
```

## 🔧 Configuration

### Environment Variables Setup

Create a `.env` file in the project root:

```env
# AI Model API Keys
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-api-key
DEEPSEEK_API_KEY=sk-your-deepseek-key

# Search and Integration
BRAVE_API_KEY=your-brave-search-key
GITHUB_TOKEN=ghp_your-github-token

# Optional Configuration
AI_MODEL=openai  # Default model: openai, claude, gemini, deepseek
DATABASE_PATH=docy_search.db  # Default database location
```

### API Key Setup Instructions

#### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to "API Keys" in the dashboard
4. Click "Create new secret key"
5. Copy and paste into your `.env` file

#### Brave Search API Key
1. Visit [Brave Search API](https://brave.com/search/api/)
2. Sign up for a free account
3. Create a new subscription (free tier available)
4. Copy your subscription token
5. Add to `.env` as `BRAVE_API_KEY`

#### Additional API Keys
- **Anthropic**: [Console](https://console.anthropic.com/)
- **Google**: [AI Studio](https://aistudio.google.com/)
- **GitHub**: [Personal Access Tokens](https://github.com/settings/tokens)
- **DeepSeek**: [Platform](https://platform.deepseek.com/)

## 🏃 Running the Application

### Web Interface (Recommended)
```bash
# With UV
uv run streamlit run docy_search/main_ui.py

# With Python
python -m streamlit run docy_search/main_ui.py

# Custom port
streamlit run docy_search/main_ui.py --server.port 8502
```

Access the application at: http://localhost:8501

### Command Line Interface
```bash
# With UV
uv run python docy_search/app.py

# With Python
python docy_search/app.py
```

### Database Utilities
```bash
# View chat history
python scripts/view_chats.py

# Interactive database browser
python scripts/database_explorer.py
```

## 🛠 Development Setup

### For Contributors

```bash
# 1. Clone and setup as above
git clone https://github.com/yourusername/Docy_Search_GitHub.git
cd Docy_Search_GitHub

# 2. Install with development dependencies
uv sync --group dev
# or: pip install -e ".[dev]"

# 3. Install pre-commit hooks
pre-commit install

# 4. Run tests
pytest

# 5. Run linting
flake8 docy_search/
black docy_search/
```

### Project Scripts
The `pyproject.toml` defines convenient entry points:

```bash
# CLI interface
docy-cli

# Web interface  
docy-web
```

## 🔍 Verification

### Check Installation
```bash
# Test basic imports
python -c "import docy_search; print('✅ Installation successful')"

# Test database creation
python -c "from docy_search.database.db_manager import get_db_manager; db = get_db_manager(); print('✅ Database ready')"

# Test UI components
python -c "import streamlit; print('✅ Streamlit ready')"
```

### Test API Connections
```bash
# Launch the web interface
streamlit run docy_search/main_ui.py

# In the UI:
# 1. Go to sidebar → Tool Selection
# 2. Click "Test Connection" for SQL Database
# 3. Verify API keys in the configuration banner
```

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# If you get module import errors:
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# or on Windows:
set PYTHONPATH=%PYTHONPATH%;%cd%
```

#### Database Permissions
```bash
# If database creation fails:
chmod 755 .
mkdir -p data
chmod 755 data
```

#### Port Already in Use
```bash
# If port 8501 is busy:
streamlit run docy_search/main_ui.py --server.port 8502
```

#### Missing Dependencies
```bash
# If packages are missing:
pip install --upgrade -r requirements.txt

# For UV users:
uv sync --refresh
```

### Performance Issues

#### Memory Usage
- **Reduce concurrent MCP servers**: Disable unused tools in the sidebar
- **Clear chat history**: Use the "Clear Conversation" button
- **Restart application**: Memory usage will reset

#### API Rate Limits
- **GitHub**: Increase limits with a GitHub token
- **OpenAI**: Monitor usage in the sidebar cost tracker
- **Brave Search**: Free tier has 2000 queries/month

### Error Messages

#### "MCP server is not running"
- **Solution**: Wait a few seconds for servers to initialize
- **Alternative**: Restart the application

#### "API key not found"
- **Solution**: Check your `.env` file configuration
- **Note**: Basic functionality works without API keys

#### "Database not available"
- **Solution**: Check file permissions in the project directory
- **Alternative**: Restart with administrator/sudo privileges

## 📚 Next Steps

After installation:

1. **Read the [Overview](./01-overview.md)** to understand the application
2. **Explore [Components Guide](./04-components.md)** to learn about modules
3. **Check [API Reference](./03-api-reference.md)** for detailed function docs
4. **Review [Configuration](./05-configuration.md)** for customization options

## 🆘 Getting Help

- **Documentation**: Check the other docs in this folder
- **Issues**: Create an issue on GitHub
- **Community**: Join discussions in the repository
- **Logs**: Check the console output for detailed error messages

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
uv sync
# or: pip install --upgrade -r requirements.txt

# Update database schema (automatic)
python docy_search/main_ui.py
```
