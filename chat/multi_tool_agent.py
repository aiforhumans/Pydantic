#!/usr/bin/env python3
"""
Multi-Tool Agent - Demonstrates multiple tools and structured responses
"""
from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Setup local model
model = OpenAIModel(
    'ibm/granite-3.2-8b',
    provider=OpenAIProvider(
        base_url='http://localhost:1234/v1',
        api_key='lm-studio'
    ),
)

# Structured output models
class WeatherInfo(BaseModel):
    location: str
    temperature: int
    condition: str
    humidity: int

class TaskItem(BaseModel):
    id: int
    title: str
    completed: bool
    created_at: datetime

class AssistantResponse(BaseModel):
    message: str
    data: Dict
    tools_used: List[str]

# Create multi-tool agent with structured output
assistant_agent = Agent(
    model,
    deps_type=dict,  # Use dict to store various data
    output_type=AssistantResponse,
    system_prompt=(
        "You are a multi-functional assistant with access to weather, "
        "time, and task management tools. Always use the appropriate tools "
        "to provide accurate information."
    ),
)

@assistant_agent.tool
async def get_weather(ctx: RunContext[dict], location: str) -> str:
    """Get weather information for a location"""
    # Mock weather data - in real app, you'd call a weather API
    weather_data = {
        "New York": {"temp": 22, "condition": "Sunny", "humidity": 65},
        "London": {"temp": 15, "condition": "Cloudy", "humidity": 78},
        "Tokyo": {"temp": 18, "condition": "Rainy", "humidity": 85},
        "default": {"temp": 20, "condition": "Clear", "humidity": 60}
    }
    
    data = weather_data.get(location.title(), weather_data["default"])
    result = f"Weather in {location}: {data['temp']}°C, {data['condition']}, Humidity: {data['humidity']}%"
    
    # Store in context for structured output
    if 'tools_used' not in ctx.deps:
        ctx.deps['tools_used'] = []
    ctx.deps['tools_used'].append('get_weather')
    ctx.deps['weather_data'] = data
    
    return result

@assistant_agent.tool
async def get_current_time(ctx: RunContext[dict]) -> str:
    """Get the current date and time"""
    now = datetime.now()
    result = f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    if 'tools_used' not in ctx.deps:
        ctx.deps['tools_used'] = []
    ctx.deps['tools_used'].append('get_current_time')
    ctx.deps['current_time'] = now.isoformat()
    
    return result

@assistant_agent.tool
async def add_task(ctx: RunContext[dict], title: str) -> str:
    """Add a new task to the task list"""
    if 'tasks' not in ctx.deps:
        ctx.deps['tasks'] = []
    
    task_id = len(ctx.deps['tasks']) + 1
    new_task = {
        "id": task_id,
        "title": title,
        "completed": False,
        "created_at": datetime.now().isoformat()
    }
    
    ctx.deps['tasks'].append(new_task)
    
    if 'tools_used' not in ctx.deps:
        ctx.deps['tools_used'] = []
    ctx.deps['tools_used'].append('add_task')
    
    return f"Added task: '{title}' with ID {task_id}"

@assistant_agent.tool
async def list_tasks(ctx: RunContext[dict]) -> str:
    """List all tasks"""
    if 'tasks' not in ctx.deps:
        ctx.deps['tasks'] = []
    
    if not ctx.deps['tasks']:
        result = "No tasks found."
    else:
        task_list = []
        for task in ctx.deps['tasks']:
            status = "✅" if task['completed'] else "❌"
            task_list.append(f"{status} {task['id']}: {task['title']}")
        result = "Tasks:\n" + "\n".join(task_list)
    
    if 'tools_used' not in ctx.deps:
        ctx.deps['tools_used'] = []
    ctx.deps['tools_used'].append('list_tasks')
    
    return result

def test_multi_tool_agent():
    """Test the multi-tool agent"""
    print("🛠️ Multi-Tool Agent Demo")
    print("=" * 40)
    
    # Initialize context data
    context_data = {}
    
    # Test different queries
    queries = [
        "What's the weather like in New York?",
        "What time is it?",
        "Add a task to buy groceries",
        "Add a task to call mom",
        "Show me my tasks",
        "What's the weather in Tokyo and what time is it?"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}️⃣ Query: {query}")
        print("-" * 30)
        
        try:
            result = assistant_agent.run_sync(query, deps=context_data)
            
            print(f"Message: {result.data.message}")
            print(f"Tools used: {result.data.tools_used}")
            if result.data.data:
                print(f"Data: {result.data.data}")
                
        except Exception as e:
            print(f"Error: {e}")

def interactive_assistant():
    """Interactive multi-tool assistant"""
    print("\n🤖 Interactive Multi-Tool Assistant")
    print("Available commands:")
    print("- Ask about weather: 'weather in [location]'")
    print("- Get time: 'what time is it'")
    print("- Add task: 'add task [description]'")
    print("- List tasks: 'show tasks'")
    print("- Type 'quit' to exit")
    print("-" * 50)
    
    context_data = {}
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 🛠️")
            break
        
        if not user_input:
            continue
        
        try:
            result = assistant_agent.run_sync(user_input, deps=context_data)
            
            print(f"\n🤖 Assistant: {result.data.message}")
            if result.data.tools_used:
                print(f"🛠️ Tools used: {', '.join(result.data.tools_used)}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        test_multi_tool_agent()
        interactive_assistant()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure LM Studio is running with your model loaded!")
