# Modular PydanticAI Agents

This directory now contains a modular system for creating and configuring PydanticAI agents with different rules, personalities, and capabilities.

## 📁 New Modular Files

### Core Modules
- **`agent_config.py`** - Configuration definitions and presets
- **`agent_factory.py`** - Advanced factory for creating agents
- **`simple_modular.py`** - Simple, easy-to-use interface ⭐ **START HERE**

### Original Examples  
- **`roulette_agent.py`** - Original roulette example
- **`advanced_agent.py`** - Run methods demonstration
- **`multi_tool_agent.py`** - Multi-tool assistant
- **`simple_agent.py`** - Basic agent example

## 🚀 Quick Start

### Option 1: Simple Modular Interface (Recommended)
```bash
python simple_modular.py
```

This gives you:
- **Roulette agents** with different rules (enthusiastic, professional, casual)
- **Assistant agents** with different personalities (helpful, creative, technical, casual)
- **Multi-tool agents** with weather, time, and calculator tools
- **Interactive builder** to test configurations

### Option 2: Advanced Configuration System
```bash
python modular_demo.py  # If imports work
```

## 🎛️ Configuration Options

### Roulette Agent Rules
```python
builder = SimpleAgentBuilder()

# Enthusiastic operator (default)
agent = builder.roulette_agent(rules="enthusiastic")

# Professional operator  
agent = builder.roulette_agent(rules="professional")

# Casual operator
agent = builder.roulette_agent(rules="casual")
```

### Assistant Personalities
```python
# Helpful assistant (default)
agent = builder.assistant_agent(personality="helpful")

# Creative assistant
agent = builder.assistant_agent(personality="creative")

# Technical expert
agent = builder.assistant_agent(personality="technical")

# Casual friend
agent = builder.assistant_agent(personality="casual")
```

### Multi-Tool Agents
```python
# All tools (default: weather, time, calculator)
agent = builder.multi_tool_agent()

# Specific tools only
agent = builder.multi_tool_agent(tools=["weather", "time"])
```

## 🎯 Usage Examples

### Roulette with Different Rules
```python
builder = SimpleAgentBuilder()

# Enthusiastic operator
agent = builder.roulette_agent("enthusiastic")
result = agent.run_sync("I'm betting on 7!", deps=18)
# Response: Exciting and encouraging

# Professional operator  
agent = builder.roulette_agent("professional")
result = agent.run_sync("I'm betting on 7!", deps=18)
# Response: Factual and clear
```

### Assistant with Different Personalities
```python
# Creative assistant
agent = builder.assistant_agent("creative")
result = agent.run_sync("Write about AI")
# Response: Imaginative and inspiring

# Technical expert
agent = builder.assistant_agent("technical")  
result = agent.run_sync("Explain neural networks")
# Response: Detailed and precise
```

## 🔧 Customization

### Easy Customization in `simple_modular.py`

1. **Add new roulette rules:**
```python
rule_sets = {
    "your_rule": {
        "prompt": "Your custom prompt here",
        "temperature": 0.6
    }
}
```

2. **Add new personalities:**
```python
personalities = {
    "your_personality": {
        "prompt": "Your personality prompt",
        "temperature": 0.8
    }
}
```

3. **Add new tools:**
```python
@agent.tool
async def your_tool(ctx: RunContext[dict], param: str) -> str:
    """Your custom tool"""
    return "Tool result"
```

## 💡 Key Benefits

✅ **Easy Configuration** - Just specify rules/personality
✅ **Reusable Components** - Mix and match different settings
✅ **Type Safety** - Proper type hints and structured output
✅ **Tool Management** - Easy tool registration and usage
✅ **Interactive Testing** - Built-in interactive modes
✅ **Preset Management** - Predefined configurations
✅ **Rule Application** - Apply behavioral rules to any agent

## 🎮 Interactive Mode

Run `python simple_modular.py` and use the interactive mode to:
- Test different agent configurations
- Compare personalities side-by-side  
- Experiment with tool combinations
- See how rules affect behavior

## 📊 Configuration Matrix

| Agent Type | Rules/Personality | Temperature | Use Case |
|------------|------------------|-------------|----------|
| Roulette | Enthusiastic | 0.8 | Fun gaming |
| Roulette | Professional | 0.4 | Serious gaming |
| Assistant | Creative | 0.9 | Writing tasks |
| Assistant | Technical | 0.3 | Programming help |
| Multi-tool | Default | 0.7 | General assistance |

Start with `simple_modular.py` to explore the modular system! 🎉
