# Streamlit Web Interface Guide

The Docy Search Tool Recommendation Assistant includes a beautiful, modern web interface built with Streamlit. This guide covers everything you need to know about using the **fully operational** web UI with integrated memory system.

## 🚀 Quick Start

### Launch the Web Interface

```bash
# Activate virtual environment (if using one)
source .venv/bin/activate

# Start the Streamlit app with recommended port
streamlit run main_ui.py --server.port 8555

# Default port option
streamlit run main_ui.py

# Headless mode (no browser opening)
streamlit run main_ui.py --server.headless true
```

**Access the App:**
- Open your browser to: `http://localhost:8555` (or 8501 for default)
- The interface will automatically load with your session and memory system

## 🎯 Features

### ✅ **WORKING: Chat Interface**
- **Real-time conversations** with the tool recommendation assistant
- **Memory persistence** - conversations remembered across sessions with OpenAI embeddings
- **Project context integration** - automatically loads your `project_context.md`
- **Message history** - scrollable chat with memory save indicators
- **Beautiful UI** - Modern chat bubbles with syntax highlighting

### ✅ **WORKING: Session Management**
- **Persistent user sessions** - maintains your identity across app restarts
- **Memory system status** - shows ✅ Active or ⚠️ Disabled in sidebar
- **Session ID display** - Shows first 8 characters of your persistent UUID
- **Port suggestions** - Random port recommendations for multi-user setups

### ✅ **WORKING: Memory Integration**
- **Real-time indicators** - "💾 Memory saved (ID: X)" messages
- **Context continuity** - Previous conversations enhance current responses
- **Semantic search** - Uses OpenAI embeddings for intelligent memory retrieval
- **Graceful degradation** - Works perfectly with or without memory system

## 🧠 Memory System Integration

The UI **fully integrates** with our operational memory system:

- ✅ **Automatic memory saving** for significant interactions (>100 chars)
- ✅ **Context loading** from previous conversations using semantic search
- ✅ **Session persistence** with UUID-based user identification
- ✅ **Memory indicators** showing when interactions are saved with IDs
- ✅ **OpenAI embeddings** working with `text-embedding-3-small`
- ✅ **Cross-session continuity** - memory works across browser restarts

## 🎨 UI Features

### ✅ **WORKING: Beautiful Interface**
- **Custom styling** for professional appearance  
- **Modern chat bubbles** with user/assistant differentiation
- **Syntax highlighting** for code blocks and commands
- **Responsive design** that works on desktop and mobile
- **Color-coded status indicators** for memory system
- **Smooth scrolling** and automatic message positioning

### ✅ **WORKING: Real-time Feedback**
- **Thinking indicators** - Shows "Thinking..." while AI processes
- **Memory save notifications** - Live feedback when memories are stored
- **Error handling** - Graceful error messages with retry guidance
- **Session status** - Visual confirmation of memory system state

## 🔧 Advanced Usage

### Multi-Session Support
```bash
# Run multiple instances on different ports for team use
streamlit run main_ui.py --server.port 8555  # User 1
streamlit run main_ui.py --server.port 8556  # User 2
streamlit run main_ui.py --server.port 8557  # User 3
```

### Development Mode
```bash
# Auto-reload on file changes (for developers)
streamlit run main_ui.py --server.port 8555 --server.runOnSave true
```

## 🛠 Troubleshooting

### Common Issues

**✅ Port Already in Use:**
```bash
# The UI suggests random ports automatically
# Or manually try: streamlit run main_ui.py --server.port 8556
```

**✅ Memory System Disabled:**
- Check that `OPENAI_API_KEY` is set in your `.env` file
- Verify the `data/` directory exists and is writable
- The app works without memory but won't have persistence

**✅ Slow Loading:**
- Check internet connection for API calls
- Ensure dependencies installed: `pip install -r requirements.txt`

## 📊 Success Examples

### ✅ Memory-Enhanced Conversations
```text
Session 1:
You: "I need React development tools"
Assistant: [Provides React tools and analysis]
💾 Memory saved (ID: 1)

Session 2 (same or different browser session):
You: "What about testing?"
Assistant: ✅ I remember you're working with React! Based on our previous discussion...
[Provides Jest, React Testing Library, Cypress for React]
💾 Memory saved (ID: 2)
```

### ✅ Real-time Status Updates
- **Sidebar**: Shows "✅ Memory system active" 
- **Session ID**: Displays "Session ID: fc1a4ccb..."
- **Port Helper**: Suggests "💡 Run with: `streamlit run main_ui.py --server.port 8567`"

## 🚀 Getting Started

**Ready to use the web interface?**

1. **Launch**: `streamlit run main_ui.py --server.port 8555`
2. **Open**: `http://localhost:8555` in your browser  
3. **Chat**: Start asking about development tools
4. **Watch**: See memory indicators as your conversation history builds

The web interface provides the same powerful tool recommendations as the command line version, but with a beautiful, user-friendly interface that makes it easy to build and reference your conversation history!
- **Responsive layout** with collapsible sidebar

### User Experience
- **Welcome message** for new users with examples
- **Loading spinners** during AI processing
- **Memory status indicators** on saved messages
- **Helpful tooltips** and usage suggestions

## 🔧 Development

### Port Management
The UI suggests random ports (8502-8599) to avoid conflicts when running multiple instances during development.

### Integration Points
- **Imports from app.py**: Uses existing `load_project_context`, `create_agent_with_context`
- **Memory integration**: Direct access to `memory_manager` from app.py
- **Model compatibility**: Works with all supported AI models (OpenAI, Claude, Gemini, DeepSeek)

## 🚦 Error Handling

The UI includes comprehensive error handling:
- **Import failures**: Graceful fallback if modules unavailable
- **Memory errors**: Non-blocking memory system failures
- **Agent errors**: User-friendly error messages
- **Session recovery**: Maintains state across page refreshes

## 💡 Usage Examples

### Basic Tool Discovery
```
User: "I need React development tools"
Assistant: [Searches and provides comprehensive React tool recommendations]
💾 Memory saved (ID: 123)
```

### Context-Aware Follow-ups
```
User: "What about testing?"
Assistant: [Remembers React context, suggests React-specific testing tools]
💾 Memory saved (ID: 124)
```

### GitHub Integration
```
User: "Show me the official React repository"
Assistant: I can search GitHub repositories... Continue? (y/n)
User: y
Assistant: [Displays React repository details and examples]
```

This UI provides a modern, user-friendly interface to our intelligent tool recommendation system while maintaining all the powerful features of the command-line version.
