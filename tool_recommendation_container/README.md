# 🔧 Tool Recommendation System - Docker Container

A powerful AI-powered tool recommendation system packaged as a Docker container for easy integration into any chatbot or application.

## 🏗️ System Overview

This container packages the entire `tool_recommendation` directory into a standalone microservice that provides:

- **AI-Powered Tool Discovery**: Search and analyze tools using multiple APIs
- **GitHub Integration**: Repository search, code analysis, and file exploration  
- **Web Search**: Brave Search API integration for finding tools
- **Code Analysis**: Repository quality assessment and dependency analysis
- **Python REPL**: Execute Python code and create visualizations
- **Database Queries**: Natural language to SQL conversion
- **Real-time Activity Tracking**: Monitor all operations and resource usage

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd tool_recommendation_container
cp .env.example .env
```

### 2. Configure API Keys

Edit `.env` file with your API keys:

```bash
# Required
BRAVE_API_KEY=your_brave_api_key_here
GOOGLE_API_KEY=your_google_api_key_here

# Optional but recommended
GITHUB_TOKEN=your_github_token_here
OPENAI_API_KEY=your_openai_api_key_here
PERPLEXITY_API_KEY=your_perplexity_api_key_here
```

### 3. Start the Container

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or using Docker directly
docker build -t tool-recommendation .
docker run -p 8000:8000 --env-file .env tool-recommendation
```

### 4. Test the Service

```bash
# Health check
curl http://localhost:8000/health

# List available tools
curl http://localhost:8000/tools

# Search for tools
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "search_tools", "parameters": {"query": "web development"}}'
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information and status |
| `/health` | GET | Health check for monitoring |
| `/tools` | GET | List all available tools |
| `/execute` | POST | Execute a tool with parameters |
| `/activity` | GET | Get activity status and logs |
| `/streamlit-integration` | POST | Optimized endpoint for Streamlit |

### Available Tools

#### 🔍 **Tool Search & Analysis**
- `search_tools(query, category)` - Search for development tools
- `analyze_tools(search_results, requirements)` - AI analysis of tools
- `get_installation_guide(tool_name, os_type)` - Installation instructions
- `compare_tools(tool_names)` - Compare multiple tools

#### 🌐 **Web Search**
- `search_web(query, num_results)` - Brave Search API integration

#### 🐙 **GitHub Integration**
- `search_github_repositories(query, language, limit)` - Find repositories
- `get_repository_structure(repo_full_name)` - Explore repo structure
- `get_file_from_repository(repo_full_name, file_path)` - Get file contents

#### 🔬 **Code Analysis**
- `analyze_repository(repo_url_or_path)` - Full repository analysis
- `get_code_quality_metrics(repo_path)` - Code quality assessment

#### 🐍 **Python Tools**
- `python_repl(code)` - Execute Python code
- `data_visualization(code)` - Create matplotlib visualizations

#### 🗃️ **Database Tools**
- `natural_language_query(question)` - Convert natural language to SQL
- `execute_sql_query(query)` - Execute safe SQL queries

#### 🤖 **AI Search**
- `perplexity_search(query, focus, max_results)` - Perplexity AI search

## 🔌 Integration with Your Streamlit App

### Installation

```bash
pip install requests streamlit
```

### Simple Integration

```python
import streamlit as st
import sys
sys.path.append('path/to/tool_recommendation_container')

from client import StreamlitToolClient

# Initialize client
client = StreamlitToolClient("http://localhost:8000")

# Check connection
if not client.client.health_check():
    st.error("Tool Recommendation Service not available!")
    st.stop()

# Chat interface
if prompt := st.chat_input("What tools are you looking for?"):
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        response = client.get_tool_recommendation(prompt)
        st.write(response)
```

### Advanced Integration

```python
from client import ToolRecommendationClient

client = ToolRecommendationClient("http://localhost:8000")

# Search for tools
search_results = client.search_tools("machine learning frameworks", "ai")

# Get AI analysis
analysis = client.analyze_tools(search_results, "I need something for NLP")

# Search GitHub
github_results = client.search_github("transformer models", "python", 10)

# Execute Python code
code_result = client.execute_python("print('Hello from container!')")
```

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BRAVE_API_KEY` | ✅ | Brave Search API key |
| `GOOGLE_API_KEY` | ✅ | Google Gemini API key |
| `GITHUB_TOKEN` | ⚠️ | GitHub API token (recommended) |
| `OPENAI_API_KEY` | ⚠️ | OpenAI API key (for embeddings) |
| `PERPLEXITY_API_KEY` | ❌ | Perplexity API key (optional) |
| `DB_PATH` | ❌ | SQLite database path |
| `SIMILARITY_THRESHOLD` | ❌ | Memory similarity threshold |

### Docker Volumes

- `/app/data` - Persistent storage for databases and logs
- `/app/logs` - Application logs (optional)

## 📊 Monitoring & Debugging

### Activity Tracking

```bash
# Get current activity status
curl http://localhost:8000/activity
```

Response includes:
- Current running activity
- Recent activity history
- Resource usage statistics
- API call counts

### Health Monitoring

```bash
# Health check
curl http://localhost:8000/health

# Service info
curl http://localhost:8000/
```

### Logs

```bash
# View container logs
docker-compose logs -f tool-recommendation

# Or with Docker
docker logs -f <container-id>
```

## 🛠️ Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server directly
python server.py

# Or with uvicorn
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

### Testing

```bash
# Test the client
python client.py

# Test individual tools
python -c "
from client import ToolRecommendationClient
client = ToolRecommendationClient()
print(client.search_tools('web frameworks'))
"
```

## 🔒 Security Considerations

1. **API Keys**: Store securely in `.env` file, never commit to git
2. **Network**: Run container on internal network in production
3. **SQL Safety**: Only SELECT operations allowed in SQL tools
4. **Resource Limits**: Set appropriate memory/CPU limits in production

## 📈 Performance

- **Startup Time**: ~10-15 seconds
- **Memory Usage**: ~200-500MB depending on active tools
- **Response Time**: 1-30 seconds depending on tool complexity
- **Concurrent Requests**: Supports multiple concurrent requests

## 🆘 Troubleshooting

### Common Issues

1. **"Tool Recommendation Server is not available"**
   - Check if container is running: `docker ps`
   - Check logs: `docker-compose logs`
   - Verify port 8000 is not in use

2. **"API Key not found" errors**
   - Check `.env` file has correct API keys
   - Restart container after updating environment

3. **Slow responses**
   - Some tools (especially AI analysis) take 10-30 seconds
   - Check network connectivity for API calls
   - Monitor activity endpoint for progress

4. **Tool execution fails**
   - Check tool parameters match expected format
   - View activity logs for detailed error information

### Debug Mode

```bash
# Run with debug logging
docker-compose up --build

# Or set environment
export LOG_LEVEL=debug
python server.py
```

## 🚢 Production Deployment

### Docker Compose Production

```yaml
version: '3.8'
services:
  tool-recommendation:
    build: .
    restart: unless-stopped
    environment:
      - LOG_LEVEL=info
    volumes:
      - tool_data:/app/data
    networks:
      - internal
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: tool-recommendation
spec:
  replicas: 2
  selector:
    matchLabels:
      app: tool-recommendation
  template:
    metadata:
      labels:
        app: tool-recommendation
    spec:
      containers:
      - name: tool-recommendation
        image: tool-recommendation:latest
        ports:
        - containerPort: 8000
        env:
        - name: BRAVE_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: brave-api-key
```

## 📝 License

[Include your license information here]

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

- GitHub Issues: [Link to your issues page]
- Documentation: [Link to full docs]
- Discord/Slack: [Community links]
