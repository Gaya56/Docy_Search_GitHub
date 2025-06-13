# 🔍 MCP Perplexity WebSearch Integration

## Overview

Add Perplexity AI web search capabilities to the Docy Search tool recommendation system via MCP (Model Context Protocol) server integration.

## Implementation Location

**Target Directory**: `/workspaces/Docy_Search_GitHub/docy_search/tool_recommendation/`

## Requirements

### Core Functionality

- [ ] **Create `perplexity_search.py`** - Main MCP server implementation
- [ ] **Integrate Perplexity API** - Web search and AI-powered responses
- [ ] **Add to MCP server registry** - Register with existing MCP infrastructure
- [ ] **Implement search result processing** - Parse and format search results
- [ ] **Add cost tracking** - Monitor API usage and costs

### Technical Specifications

#### File Structure
```text
docy_search/tool_recommendation/
├── __init__.py
├── activity_tracker.py
├── brave_search.py
├── github_mcp_server.py
├── mcp_server.py
├── models.py
├── perplexity_search.py    # <- NEW FILE
└── python_tools.py
```

#### API Integration

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

#### Phase 1: Core Implementation (Week 1)
- Create basic MCP server structure
- Implement Perplexity API client
- Add basic search functionality
- Create unit tests

#### Phase 2: Integration (Week 2)
- Integrate with existing MCP infrastructure
- Add UI components for search
- Implement memory integration
- Add cost tracking

#### Phase 3: Enhancement (Week 3)
- Add advanced search features
- Implement error handling
- Add comprehensive testing
- Create documentation

#### Phase 4: Optimization (Week 4)
- Performance optimization
- Security hardening
- User experience improvements
- Production deployment preparation

### Success Metrics

- [ ] **API Response Time** < 2 seconds average
- [ ] **Search Accuracy** > 85% user satisfaction
- [ ] **Error Rate** < 5% of total requests
- [ ] **Cost Efficiency** within budget constraints
- [ ] **User Adoption** > 70% of active users utilize search

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
