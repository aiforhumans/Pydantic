# PydanticAI Agent Examples

This folder contains comprehensive examples of PydanticAI Agents working with your local LM Studio server.

## Files Overview

### 1. `simple_agent.py` - Basic Agent
- Simple agent with system prompt
- Basic synchronous chat interface
- Good starting point for beginners

### 2. `roulette_agent.py` - Agent with Tools & Structured Output
- Demonstrates `deps_type` and `output_type`
- Shows how to create custom tools with `@agent.tool`
- Uses `RunContext` for dependency injection
- Based on the official PydanticAI documentation example

### 3. `advanced_agent.py` - Multiple Run Methods
- Shows different ways to run agents:
  - `agent.run_sync()` - Synchronous
  - `agent.run()` - Asynchronous  
  - `agent.run_stream()` - Streaming
  - `agent.iter()` - Graph iteration
- Demonstrates conversation history
- Shows low-level graph node inspection

### 4. `multi_tool_agent.py` - Multi-Tool Assistant
- Multiple tools (weather, time, tasks)
- Structured output with Pydantic models
- Context sharing between tools
- Interactive assistant interface

### 5. `sdxl_prompt_agent.py` - SDXL Prompt Generator
- Generates Stable Diffusion XL prompts
- Returns positive and negative prompts using structured output

## How to Run

Make sure LM Studio is running with your model loaded, then:

```bash
# Simple agent
python simple_agent.py

# Roulette game
python roulette_agent.py

# Advanced features demo
python advanced_agent.py

# Multi-tool assistant
python multi_tool_agent.py
# SDXL prompt generator
python sdxl_prompt_agent.py
```

## Key Concepts Demonstrated

### Agent Components
- **System prompts** - Instructions for the LLM
- **Function tools** - Functions the LLM can call
- **Structured output** - Type-safe responses
- **Dependencies** - Shared context and data
- **Model settings** - Configuration options

### Agent Types
```python
# Generic agent types
Agent[deps_type, output_type]

# Examples:
Agent[int, bool]           # Takes int deps, returns bool
Agent[dict, str]           # Takes dict deps, returns string
Agent[None, CustomModel]   # No deps, returns custom Pydantic model
```

### Running Agents
1. **Synchronous**: `agent.run_sync(message)`
2. **Asynchronous**: `await agent.run(message)`
3. **Streaming**: `async with agent.run_stream(message)`
4. **Graph iteration**: `async with agent.iter(message)`

### Tools
```python
@agent.tool
async def my_tool(ctx: RunContext[DepsType], param: str) -> str:
    """Tool description for the LLM"""
    # Access dependencies via ctx.deps
    return "tool result"
```

### Structured Output
```python
class MyOutput(BaseModel):
    message: str
    confidence: float

agent = Agent(model, output_type=MyOutput)
result = agent.run_sync("query")  # result.data is MyOutput instance
```

## Local Model Configuration

All examples use your local LM Studio configuration:

```python
model = OpenAIModel(
    'ibm/granite-3.2-8b',  # Your loaded model
    provider=OpenAIProvider(
        base_url='http://localhost:1234/v1',
        api_key='lm-studio'
    ),
)
```

## Troubleshooting

- Ensure LM Studio is running and model is loaded
- Check that port 1234 is correct for your setup
- Verify the model name matches what's loaded in LM Studio
- Use `curl http://localhost:1234/v1/models` to see available models

## Next Steps

- Experiment with different system prompts
- Create your own custom tools
- Try different structured output types
- Combine multiple agents for complex workflows
- Add error handling and validation
- Implement conversation persistence

These examples provide a solid foundation for building sophisticated AI applications with PydanticAI and your local LLM!
