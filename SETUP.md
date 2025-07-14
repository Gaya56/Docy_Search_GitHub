# Setup Guide

## Prerequisites

- Python 3.8+
- OpenAI API key
- Optional: GitHub token, Notion API key, Brave Search API key

## Installation

```bash
# 1. Clone repository
git clone https://github.com/Gaya56/Docy_Search_GitHub.git
cd Docy_Search_GitHub

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
```

## Configuration

Edit `.env` file with your API keys:

```env
OPENAI_API_KEY=your_openai_key_here
GITHUB_TOKEN=your_github_token_here
NOTION_API_KEY=your_notion_key_here
BRAVE_API_KEY=your_brave_key_here
GOOGLE_API_KEY=your_google_key_here
```

## Running the Application

```bash
# 1. Start the MCP server (Terminal 1)
python server.py

# 2. Start the Streamlit UI (Terminal 2)
streamlit run app.py
```

## Usage

1. **Configure OpenAI API key** in the sidebar
2. **Connect to tool server** (should auto-connect to localhost:8947)
3. **Select MCP server** from dropdown (e.g., GitHub, Notion)
4. **Choose specific tool** from the server's available tools
5. **Enter parameters** and execute the tool

## Docker (Alternative)

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access the application
# Streamlit UI: http://localhost:8501
# API Server: http://localhost:8947
```

## Troubleshooting

- **Connection issues**: Ensure server is running on port 8947
- **API errors**: Check your API keys in `.env` file
- **Import errors**: Verify all dependencies are installed
- **Permission errors**: Make sure you have proper API permissions

## Example Usage

### GitHub Tools

- Select "GitHub" MCP server
- Choose "search_github_repositories"
- Enter: "python web frameworks"

### Notion Tools

- Select "Notion" MCP server
- Choose "search_notion_page"
- Enter: "machine learning notes"

### Tool Recommendation

- Select "Tool Recommendation" MCP server
- Choose "search_tools"
- Enter: "docker alternatives"
