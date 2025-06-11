import os
import asyncio
from contextlib import nullcontext
from dotenv import load_dotenv # Add this import
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.google import GoogleModel

# MEMORY INTEGRATION START
import uuid
from datetime import datetime
from docy_search.memory.memory_manager import MemoryManager
# MEMORY INTEGRATION END

load_dotenv() # Call this at the beginning of your script

def load_project_context():
    """Load project context from project_context.md file"""
    context_file = "project_context.md"
    if os.path.exists(context_file):
        try:
            with open(context_file, 'r', encoding='utf-8') as f:
                context = f.read()
            print("📋 Project context loaded successfully!")
            return context
        except Exception as e:
            print(f"⚠️ Warning: Could not load project context - {e}")
            return ""
    else:
        print(f"ℹ️ No project context file found. Create '{context_file}' to provide project details.")
        return ""

def get_model_from_name(model_name):
    """Create a model instance based on the model name"""
    if model_name == "claude":
        return AnthropicModel(model_name="claude-3-opus-20240229")
    elif model_name == "gemini":
        return GoogleModel(model_name="gemini-1.5-flash")
    elif model_name == "deepseek":
        return OpenAIModel(
            model_name="deepseek-chat"
            # Note: Base URL configuration may need to be handled differently
        )
    else:  # Default to openai
        return OpenAIModel(model_name="gpt-4o-mini")

# Use model based on environment variable
model_type = os.getenv("AI_MODEL", "openai").lower()

model = get_model_from_name(model_type)

# MEMORY INTEGRATION START
# Initialize memory manager with the current model
memory_manager = None
try:
    memory_manager = MemoryManager(db_path="data/memories.db", model=model)
    print("💾 Memory system initialized successfully!")
except Exception as e:
    print(f"⚠️ Memory system disabled: {e}")
# MEMORY INTEGRATION END

# Tool Server Mapping - Maps tool keys to MCP server instances
TOOL_SERVER_MAP = {
    "web_search": lambda: MCPServerStdio('uv', ['run', 'python', '-m', 'docy_search.tool_recommendation.brave_search'], tool_prefix="web"),
    # Temporarily disabled due to aiohttp dependency conflicts
    # "github_search": lambda: MCPServerStdio('uv', ['run', 'python', '-m', 'docy_search.tool_recommendation.github_mcp_server']),
    "python_tools": lambda: MCPServerStdio('uv', ['run', 'python', '-m', 'docy_search.tool_recommendation.python_tools'], tool_prefix="py"),
    "tool_recommend": lambda: MCPServerStdio('uv', ['run', 'python', '-m', 'docy_search.tool_recommendation.mcp_server'], tool_prefix="rec"),
    "data_viz": lambda: MCPServerStdio('uv', ['run', 'python', '-m', 'docy_search.tool_recommendation.python_tools'], tool_prefix="viz")  # Same server, different prefix
}

# Define the Agent with filtered MCP servers
def create_agent_with_context(project_context="", user_id=None, model_name=None, selected_tools=None):
    # Get the appropriate model
    if model_name:
        agent_model = get_model_from_name(model_name)
    else:
        agent_model = model  # Use the default global model
    
    # Filter MCP servers based on selection
    if selected_tools is None:
        selected_tools = list(TOOL_SERVER_MAP.keys())  # All tools by default
    
    mcp_servers = []
    for tool_key in selected_tools:
        if tool_key in TOOL_SERVER_MAP:
            mcp_servers.append(TOOL_SERVER_MAP[tool_key]())
    
    context_section = ""
    if project_context.strip():
        context_section = f"""
**PROJECT CONTEXT**
The user has provided the following information about their current project:

{project_context}

Use this context to provide more targeted and relevant tool recommendations. Reference their current stack, challenges, goals, and constraints when making suggestions.

---

"""
    
    # MEMORY INTEGRATION START
    # Load relevant memories if user_id and memory_manager are available
    if user_id and memory_manager:
        try:
            memories = memory_manager.retrieve_memories(
                user_id=user_id,
                limit=5,
                category="tool_recommendation"
            )
            if memories and memories != "No previous interactions found.":
                context_section += f"""
**PREVIOUS INTERACTIONS**
Here are relevant previous interactions with this user:

{memories}

Use these memories to provide more personalized recommendations based on past discussions.

---

"""
        except Exception as e:
            print(f"⚠️ Could not load memories: {e}")
    # MEMORY INTEGRATION END
    
    system_prompt = f"""{context_section}You are an intelligent tool recommendation assistant specializing in:

**TOOL RECOMMENDATION & DISCOVERY**
Your primary purpose is to help developers, engineers, and technical professionals discover, analyze, and implement the best tools for their projects and workflows.

CORE CAPABILITIES:
- Search for tools using live web data via Brave API
- Analyze tool quality, reliability, and suitability using AI
- Provide comprehensive installation guides for recommended tools
- Compare multiple tools side-by-side with detailed analysis
- Recommend complete tool workflows for specific tasks and projects
- Support all development categories: web, mobile, desktop, database, devops, testing, design, data science, AI/ML, game development, security, productivity
- Access GitHub repositories to find official code, examples, and implementation details

GITHUB INTEGRATION:
When users ask about specific tools or need implementation examples, you can:
- Search GitHub for official repositories
- Find and display relevant code examples
- Show repository structure and key files
- Provide direct links to GitHub repositories
- Find implementation tutorials and examples

**IMPORTANT**: Before accessing GitHub repositories, you MUST ask for user permission with this exact phrase:
"I can search GitHub repositories for [specific purpose]. This will access public GitHub data to find official repositories and code examples. Continue? (y/n)"

Only proceed with GitHub searches after explicit user confirmation.

RECOMMENDATION APPROACH:
When users ask about tools, provide comprehensive recommendations with:
- Relevance scoring and detailed reasoning
- Installation complexity assessment (Easy/Medium/Hard)
- Community support and documentation evaluation
- Cost considerations (free vs paid options)
- Performance and scalability analysis
- Integration capabilities with other tools
- Learning curve assessment based on user skill level
- Official GitHub repositories and code examples (with permission)

INTERACTION STYLE:
- Always ask clarifying questions about project requirements, skill level, and constraints
- Provide actionable, practical recommendations
- Include installation guides and getting-started tips
- Suggest tool combinations and workflows when relevant
- Consider budget constraints and open-source alternatives

Your goal is to accelerate development productivity by connecting users with the perfect tools for their specific needs."""

    return Agent(
        agent_model,  # Use the selected model instead of global model
        mcp_servers=mcp_servers,  # Use filtered servers
        retries=3,
        system_prompt=system_prompt
    )

# Main async function
async def main():
    # Load project context
    project_context = load_project_context()
    
    # MEMORY INTEGRATION START
    # Generate or retrieve user session ID
    user_id = None
    if memory_manager:
        user_session_file = ".user_session"
        if os.path.exists(user_session_file):
            with open(user_session_file, 'r') as f:
                user_id = f.read().strip()
        else:
            user_id = str(uuid.uuid4())
            with open(user_session_file, 'w') as f:
                f.write(user_id)
        print(f"🔑 User session: {user_id[:8]}...")
    # MEMORY INTEGRATION END
    
    # Create agent with context
    agent = create_agent_with_context(project_context, user_id)
    
    # Re-enable MCP servers with fixed paths
    async with agent.run_mcp_servers():
        print("🔧 Tool Recommendation Assistant Ready! Type 'exit' to quit.\n")
        
        if project_context.strip():
            print("✅ I have your project context loaded and ready to help!")
            print("Ask me anything about tools for your specific project.\n")
        else:
            print("I can help you find the best tools for any development project!")
            print("Try asking me about:")
            print("- 'I need tools for web development'")
            print("- 'Compare React vs Vue.js'")
            print("- 'How do I set up Docker on Ubuntu?'")
            print("- 'What are the best tools for data analysis?'\n")
        
        conversation = []
        
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break
            
            conversation.append({"role": "user", "content": user_input})
            
            # Build context from recent conversation
            context = "Recent conversation:\n"
            context += "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation[-6:]])
            
            result = await agent.run(f"{context}\n\nCurrent message: {user_input}")
            print(f"\nAssistant: {result.output}\n")
            
            conversation.append({"role": "assistant", "content": result.output})
            
            # MEMORY INTEGRATION START
            # Save significant interactions to memory if available
            if memory_manager and user_id and len(result.output) > 100:
                try:
                    # Create a summary of the interaction
                    memory_content = f"User asked: {user_input[:200]}\nAssistant provided: {result.output[:500]}"
                    if len(result.output) > 500:
                        memory_content += "..."
                    
                    # Save memory asynchronously for better UI responsiveness
                    memory_id = memory_manager.save_memory_async(
                        user_id=user_id,
                        content=memory_content,
                        metadata={
                            "timestamp": datetime.now().isoformat(),
                            "user_input_length": len(user_input),
                            "response_length": len(result.output),
                            "category": "tool_recommendation"
                        },
                        category="tool_recommendation"
                    )
                    print(f"💾 Memory saved asynchronously")
                except Exception as e:
                    print(f"⚠️ Could not save memory: {e}")
            # MEMORY INTEGRATION END

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())