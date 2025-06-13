# 🔍 MCP Perplexity WebSearch Integration

## Overview

Add Perplexity AI web search capabilities to the Docy Search tool recommendation system by cloning an existing MCP Perplexity server repository and integrating it into our tool recommendation system.

## Implementation Approach

**Method**: Clone existing MCP Perplexity repository and integrate into our system
**Target Directory**: `/workspaces/Docy_Search_GitHub/docy_search/tool_recommendation/`

## Repository Integration Plan

## Repository Integration Plan

### Step 1: Repository Selection & Cloning

- [ ] **Identify suitable MCP Perplexity repository** from GitHub/community sources
- [ ] **Clone repository** to temporary location for evaluation
- [ ] **Review code quality** and compatibility with our system
- [ ] **Check license compatibility** for integration
- [ ] **Evaluate dependencies** and potential conflicts

### Step 2: Integration Process  

- [ ] **Clone repository** into `/workspaces/Docy_Search_GitHub/docy_search/tool_recommendation/mcp_perplexity/`
- [ ] **Adapt import structure** to match our project layout
- [ ] **Update configuration** to use our settings system
- [ ] **Modify MCP server registration** to integrate with existing infrastructure
- [ ] **Add to tool recommendation registry** in our main system

### Step 3: Directory Structure After Integration

```text
docy_search/tool_recommendation/
├── __init__.py
├── activity_tracker.py
├── brave_search.py
├── github_mcp_server.py
├── mcp_server.py
├── models.py
├── python_tools.py
└── mcp_perplexity/              # <- CLONED REPOSITORY
    ├── __init__.py
    ├── server.py
    ├── client.py
    ├── config.py
    ├── models.py
    └── utils.py
```

## Integration Requirements

## Integration Requirements

### Adaptation Tasks

- [ ] **Update import paths** to match our project structure
- [ ] **Integrate with existing configuration** system (`config/settings.py`)
- [ ] **Adapt MCP server registration** to work with our `mcp_server.py`
- [ ] **Update dependencies** in `requirements.txt` and `pyproject.toml`
- [ ] **Modify error handling** to use our logging system
- [ ] **Add cost tracking integration** with existing memory/cost_tracker.py

### Configuration Integration

- [ ] **Add Perplexity settings** to `config/settings.py`
- [ ] **Environment variable setup** for API keys and configuration
- [ ] **Update .env.example** with required Perplexity variables
- [ ] **Add configuration validation** for required settings

### API Integration

- **Perplexity API Endpoint**: `https://api.perplexity.ai/chat/completions`
- **Authentication**: API key via environment variable `PERPLEXITY_API_KEY`
- **Models**: Support for `llama-3.1-sonar-small-128k-online`, `llama-3.1-sonar-large-128k-online`
- **Rate Limiting**: Implement proper rate limiting and error handling

#### MCP Server Implementation

```python
# Example structure for perplexity_search.py
class PerplexitySearchServer:
    def __init__(self):
        self.api_key = os.getenv('PERPLEXITY_API_KEY')
        self.base_url = 'https://api.perplexity.ai'
        
    async def search(self, query: str, model: str = "llama-3.1-sonar-small-128k-online"):
        """Perform web search with AI-powered responses"""
        pass
        
    async def get_search_results(self, query: str, max_results: int = 10):
        """Get structured search results"""
        pass
```

### Integration Points

#### 1. MCP Server Registration

- Add to `mcp_server.py` registry
- Include in tool recommendation logic
- Add to activity tracking system

#### 2. UI Integration

- Add Perplexity search option to web interface
- Display search results with proper formatting
- Show source citations and confidence scores

#### 3. Memory Integration

- Store search queries and results in memory system
- Enable semantic search over past Perplexity results
- Track search performance and user preferences

### Configuration

#### Environment Variables

```bash
# Add to .env or environment
PERPLEXITY_API_KEY=your_perplexity_api_key_here
PERPLEXITY_MODEL=llama-3.1-sonar-small-128k-online
PERPLEXITY_MAX_RESULTS=10
PERPLEXITY_TIMEOUT=30
```

#### Settings Integration

Add to `config/settings.py`:

```python
# Perplexity API Configuration
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
PERPLEXITY_BASE_URL = 'https://api.perplexity.ai'
PERPLEXITY_DEFAULT_MODEL = 'llama-3.1-sonar-small-128k-online'
PERPLEXITY_MAX_RESULTS = int(os.getenv('PERPLEXITY_MAX_RESULTS', 10))
PERPLEXITY_TIMEOUT = int(os.getenv('PERPLEXITY_TIMEOUT', 30))
```

### Features to Implement

#### Core Search Features

- [ ] **Real-time web search** with current information
- [ ] **AI-powered summaries** of search results
- [ ] **Source citation** and credibility scoring
- [ ] **Multi-language support** for global queries
- [ ] **Search result filtering** by date, domain, content type

#### Advanced Features

- [ ] **Search result clustering** for related topics
- [ ] **Fact-checking integration** for information verification
- [ ] **Trend analysis** for emerging topics
- [ ] **Personalized search** based on user history
- [ ] **Search result export** in multiple formats

#### Error Handling

- [ ] **API rate limit handling** with exponential backoff
- [ ] **Network error recovery** with retry logic
- [ ] **Invalid query handling** with user feedback
- [ ] **API key validation** and rotation support
- [ ] **Graceful degradation** when service is unavailable

### Testing Requirements

#### Unit Tests

- [ ] Test API client initialization and configuration
- [ ] Test search query processing and validation
- [ ] Test result parsing and formatting
- [ ] Test error handling scenarios
- [ ] Test rate limiting and retry logic

#### Integration Tests

- [ ] Test MCP server integration
- [ ] Test UI component integration
- [ ] Test memory system integration
- [ ] Test cost tracking integration
- [ ] Test end-to-end search workflows

### Documentation

#### API Documentation

- [ ] Document Perplexity search endpoints
- [ ] Document configuration options
- [ ] Document error codes and handling
- [ ] Document rate limits and quotas

#### User Documentation

- [ ] Add search usage examples
- [ ] Document best practices for queries
- [ ] Explain result interpretation
- [ ] Troubleshooting guide

### Implementation Timeline

#### Phase 1: Repository Integration (Week 1)

- Clone and evaluate MCP Perplexity repository
- Integrate into tool_recommendation directory structure
- Update import paths and dependencies
- Basic functionality testing

#### Phase 2: System Integration (Week 2)

- Integrate with existing MCP infrastructure
- Add UI components for search functionality
- Implement memory and cost tracking integration
- Add configuration management

#### Phase 3: Enhancement & Testing (Week 3)

- Add advanced search features and error handling
- Implement comprehensive testing suite
- Add performance optimization
- Create documentation and usage examples

#### Phase 4: Production Readiness (Week 4)

- Performance optimization and security hardening
- User experience improvements and feedback integration
- Production deployment preparation
- Monitoring and alerting setup

### Success Metrics

- [ ] **API Response Time** < 2 seconds average
- [ ] **Search Accuracy** > 85% user satisfaction
- [ ] **Error Rate** < 5% of total requests
- [ ] **Cost Efficiency** within budget constraints
- [ ] **User Adoption** > 70% of active users utilize search

## Repository Cloning & Setup Commands

### Prerequisites

```bash
# Ensure we're in the correct directory
cd /workspaces/Docy_Search_GitHub/docy_search/tool_recommendation
```

### Cloning Process

```bash
# Option 1: Clone a specific MCP Perplexity repository (example)
git clone https://github.com/[owner]/mcp-perplexity-server.git mcp_perplexity

# Option 2: If using Git submodule for easier management
git submodule add https://github.com/[owner]/mcp-perplexity-server.git mcp_perplexity

# Navigate to cloned directory
cd mcp_perplexity

# Install dependencies if needed
pip install -r requirements.txt
```

### Post-Clone Integration Steps

```bash
# 1. Update our main requirements.txt
echo "# Perplexity MCP Server dependencies" >> ../../requirements.txt
cat mcp_perplexity/requirements.txt >> ../../requirements.txt

# 2. Create integration wrapper
touch ../perplexity_integration.py

# 3. Update our MCP server registry
# (Manual edit required in mcp_server.py)
```

### Repository Candidates

Popular MCP Perplexity repositories to consider:
- `modelcontextprotocol/servers` (official MCP servers collection)
- Community-maintained Perplexity MCP implementations
- Custom Perplexity API wrappers with MCP support

**Note**: Replace `[owner]/mcp-perplexity-server` with the actual repository URL once identified.

## Dependencies

### Required Packages

```text
# Add to requirements.txt
perplexity-api>=1.0.0  # If official client exists
httpx>=0.24.0          # For async HTTP requests
pydantic>=2.0.0        # For data validation
tenacity>=8.0.0        # For retry logic
```

### Optional Enhancements

```text
# Optional packages for advanced features
beautifulsoup4>=4.12.0  # For web scraping if needed
nltk>=3.8.0             # For text processing
spacy>=3.7.0            # For NLP features
```

## Notes

- Ensure compliance with Perplexity AI's terms of service
- Monitor API costs and implement usage limits
- Consider caching strategies for frequently searched queries
- Plan for API version updates and migration paths
- Implement proper logging for debugging and monitoring
