# Streamlit UI Usage Guide

## 🚀 Quick Start

Run the Streamlit web interface:

```bash
# Default port (8501)
streamlit run main_ui.py

# Custom port for development
streamlit run main_ui.py --server.port 8555

# Headless mode (no browser opening)
streamlit run main_ui.py --server.headless true
```

## 🎯 Features

### Chat Interface
- **Real-time conversations** with the tool recommendation assistant
- **Memory persistence** - conversations remembered across sessions
- **Project context integration** - automatically loads your `project_context.md`
- **Message history** - scrollable chat with memory indicators

### Session Management
- **Persistent user sessions** - maintains your identity across app restarts
- **Memory system status** - shows if intelligent memory is active
- **Conversation metrics** - displays message count and session info

### Controls
- **Clear conversation** - reset chat history without losing memory
- **Project context preview** - view loaded project details
- **Development helpers** - suggested ports for multi-instance testing

## 🧠 Memory System Integration

The UI fully integrates with our memory system:

- ✅ **Automatic memory saving** for significant interactions (>100 chars)
- ✅ **Context loading** from previous conversations
- ✅ **Session persistence** with UUID-based user identification
- ✅ **Memory indicators** showing when interactions are saved
- ✅ **Graceful degradation** if memory system is disabled

## 🎨 UI Features

### Styling
- **Custom CSS** for professional appearance
- **Gradient headers** and styled components
- **Color-coded status indicators** for memory system
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
