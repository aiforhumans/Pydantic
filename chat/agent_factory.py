#!/usr/bin/env python3
"""
Modular Agent Factory
Create and manage PydanticAI agents with configurable options
"""
from typing import Dict, Any, Optional, Callable
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from agent_config import AgentConfig, get_agent_config, apply_rules

class AgentFactory:
    """Factory class for creating configured PydanticAI agents"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tools: Dict[str, Callable] = {}
        
    def create_agent(
        self, 
        config: AgentConfig, 
        agent_id: Optional[str] = None
    ) -> Agent:
        """Create an agent from configuration"""
        
        # Create the model
        model = OpenAIModel(
            config.model_name,
            provider=OpenAIProvider(
                base_url=config.base_url,
                api_key=config.api_key
            )
        )
        
        # Create the agent
        agent = Agent(
            model,
            deps_type=config.deps_type,
            output_type=config.output_type,
            system_prompt=config.system_prompt
        )
        
        # Store the agent if ID is provided
        if agent_id:
            self.agents[agent_id] = agent
            
        return agent
    
    def create_from_preset(
        self, 
        preset_name: str, 
        rule_set: Optional[str] = None,
        agent_id: Optional[str] = None
    ) -> Agent:
        """Create an agent from a preset configuration"""
        config = get_agent_config(preset_name)
        
        if rule_set:
            config = apply_rules(config, rule_set)
            
        return self.create_agent(config, agent_id)
    
    def register_tool(self, name: str, tool_func: Callable):
        """Register a tool function"""
        self.tools[name] = tool_func
    
    def add_tool_to_agent(self, agent: Agent, tool_name: str):
        """Add a registered tool to an agent"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not registered")
        
        # Add the tool as a decorator
        tool_func = self.tools[tool_name]
        agent.tool(tool_func)
        
    def get_agent(self, agent_id: str) -> Agent:
        """Get a stored agent by ID"""
        if agent_id not in self.agents:
            raise ValueError(f"Agent '{agent_id}' not found")
        return self.agents[agent_id]
    
    def list_agents(self) -> list:
        """List all stored agent IDs"""
        return list(self.agents.keys())

# Global factory instance
factory = AgentFactory()

# Tool functions
async def roulette_wheel_tool(ctx: RunContext[int], square: int) -> str:
    """Roulette wheel tool - check if square is winner"""
    winning_number = ctx.deps
    result = 'winner' if square == winning_number else 'loser'
    print(f"🎰 Roulette spin: Player bet {square}, winning number is {winning_number} -> {result}")
    return result

async def weather_tool(ctx: RunContext[dict], location: str) -> str:
    """Mock weather tool"""
    weather_data = {
        "New York": {"temp": 22, "condition": "Sunny", "humidity": 65},
        "London": {"temp": 15, "condition": "Cloudy", "humidity": 78},
        "Tokyo": {"temp": 18, "condition": "Rainy", "humidity": 85},
        "default": {"temp": 20, "condition": "Clear", "humidity": 60}
    }
    
    data = weather_data.get(location.title(), weather_data["default"])
    result = f"Weather in {location}: {data['temp']}°C, {data['condition']}, Humidity: {data['humidity']}%"
    
    # Store in context
    if 'weather_queries' not in ctx.deps:
        ctx.deps['weather_queries'] = []
    ctx.deps['weather_queries'].append({"location": location, "data": data})
    
    return result

async def time_tool(ctx: RunContext[dict]) -> str:
    """Get current time tool"""
    from datetime import datetime
    now = datetime.now()
    result = f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    
    if 'time_queries' not in ctx.deps:
        ctx.deps['time_queries'] = []
    ctx.deps['time_queries'].append(now.isoformat())
    
    return result

async def calculator_tool(ctx: RunContext[dict], expression: str) -> str:
    """Simple calculator tool"""
    try:
        # Basic safety check - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/().= ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic math operations allowed"
        
        result = eval(expression)
        
        if 'calculations' not in ctx.deps:
            ctx.deps['calculations'] = []
        ctx.deps['calculations'].append({"expression": expression, "result": result})
        
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

# Register tools
factory.register_tool("roulette_wheel", roulette_wheel_tool)
factory.register_tool("weather", weather_tool)
factory.register_tool("time", time_tool)
factory.register_tool("calculator", calculator_tool)

def quick_agent(preset: str, rules: Optional[str] = None, tools: Optional[list] = None) -> Agent:
    """Quick function to create a configured agent"""
    agent = factory.create_from_preset(preset, rules)
    
    if tools:
        for tool_name in tools:
            factory.add_tool_to_agent(agent, tool_name)
    
    return agent
