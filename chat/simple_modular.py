#!/usr/bin/env python3
"""
Simple Modular Agent Example
Easy-to-use interface for creating configured agents
"""
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from pydantic_ai import Agent, RunContext
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider
except ImportError:
    print("❌ PydanticAI not available. Please install with: pip install pydantic-ai")
    sys.exit(1)

class SimpleAgentBuilder:
    """Simple class to build configured agents"""
    
    def __init__(self, model_name='ibm/granite-3.2-8b'):
        self.model_name = model_name
        self.base_url = 'http://localhost:1234/v1'
        self.api_key = 'lm-studio'
        
    def create_model(self):
        """Create the OpenAI model"""
        return OpenAIModel(
            self.model_name,
            provider=OpenAIProvider(
                base_url=self.base_url,
                api_key=self.api_key
            )
        )
    
    def roulette_agent(self, rules="enthusiastic"):
        """Create a roulette agent with configurable rules"""
        
        # Define different rule sets
        rule_sets = {
            "enthusiastic": {
                "prompt": (
                    "You are an enthusiastic roulette wheel operator! "
                    "Use the `roulette_wheel` function to check if customers win. "
                    "Be exciting and engaging! Celebrate wins and encourage on losses!"
                ),
                "temperature": 0.8
            },
            "professional": {
                "prompt": (
                    "You are a professional roulette operator. "
                    "Use the `roulette_wheel` function to check results. "
                    "Provide clear, factual information about wins and losses."
                ),
                "temperature": 0.4
            },
            "casual": {
                "prompt": (
                    "You're a friendly roulette operator. "
                    "Use the `roulette_wheel` function to check results. "
                    "Keep it fun and relaxed!"
                ),
                "temperature": 0.7
            }
        }
        
        rule_set = rule_sets.get(rules, rule_sets["enthusiastic"])
        
        agent = Agent(
            self.create_model(),
            deps_type=int,
            output_type=bool,
            system_prompt=rule_set["prompt"]
        )
        
        @agent.tool
        async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
            """Check if the square is a winner"""
            winning_number = ctx.deps
            result = 'winner' if square == winning_number else 'loser'
            print(f"🎰 Spin result: {square} vs {winning_number} -> {result}")
            return result
        
        return agent
    
    def assistant_agent(self, personality="helpful"):
        """Create an assistant agent with different personalities"""
        
        personalities = {
            "helpful": {
                "prompt": "You are a helpful AI assistant. Provide clear, accurate answers.",
                "temperature": 0.7
            },
            "creative": {
                "prompt": "You are a creative AI assistant. Be imaginative and inspiring!",
                "temperature": 0.9
            },
            "technical": {
                "prompt": "You are a technical expert. Provide detailed, accurate information.",
                "temperature": 0.3
            },
            "casual": {
                "prompt": "You're a friendly, casual AI. Keep things fun and relaxed!",
                "temperature": 0.8
            }
        }
        
        personality_config = personalities.get(personality, personalities["helpful"])
        
        return Agent(
            self.create_model(),
            system_prompt=personality_config["prompt"]
        )
    
    def multi_tool_agent(self, tools=None):
        """Create an agent with multiple tools"""
        if tools is None:
            tools = ["weather", "time", "calculator"]
        
        agent = Agent(
            self.create_model(),
            deps_type=dict,
            system_prompt=(
                "You are a multi-tool assistant. Use the available tools to help users. "
                "Always use tools when they can provide accurate information."
            )
        )
        
        if "weather" in tools:
            @agent.tool
            async def get_weather(ctx: RunContext[dict], location: str) -> str:
                """Get weather for a location"""
                weather_data = {
                    "New York": "22°C, Sunny",
                    "London": "15°C, Cloudy", 
                    "Tokyo": "18°C, Rainy",
                    "Paris": "20°C, Clear"
                }
                result = weather_data.get(location, "20°C, Clear")
                return f"Weather in {location}: {result}"
        
        if "time" in tools:
            @agent.tool
            async def get_time(ctx: RunContext[dict]) -> str:
                """Get current time"""
                from datetime import datetime
                return f"Current time: {datetime.now().strftime('%H:%M:%S')}"
        
        if "calculator" in tools:
            @agent.tool
            async def calculate(ctx: RunContext[dict], expression: str) -> str:
                """Simple calculator"""
                try:
                    result = eval(expression)
                    return f"{expression} = {result}"
                except:
                    return "Error: Invalid expression"
        
        return agent

def demo_simple_agents():
    """Demonstrate the simple agent builder"""
    print("🛠️ Simple Modular Agents Demo")
    print("=" * 40)
    
    builder = SimpleAgentBuilder()
    
    # Test different roulette agent rules
    print("\n🎰 Roulette Agents with Different Rules")
    print("-" * 40)
    
    rules_to_test = ["enthusiastic", "professional", "casual"]
    
    for rule in rules_to_test:
        print(f"\n📋 Testing '{rule}' rules:")
        try:
            agent = builder.roulette_agent(rules=rule)
            result = agent.run_sync("I'm betting on number 7!", deps=18)
            print(f"Result: {result.output} ({'🎉 Winner!' if result.output else '💔 Loser!'})")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test different assistant personalities
    print("\n🤖 Assistant Agents with Different Personalities")
    print("-" * 40)
    
    personalities = ["helpful", "creative", "technical", "casual"]
    
    for personality in personalities:
        print(f"\n🎭 Testing '{personality}' personality:")
        try:
            agent = builder.assistant_agent(personality=personality)
            result = agent.run_sync("What is machine learning?")
            print(f"Response: {result.output}")
        except Exception as e:
            print(f"Error: {e}")
    
    # Test multi-tool agent
    print("\n🔧 Multi-Tool Agent")
    print("-" * 40)
    
    try:
        agent = builder.multi_tool_agent()
        queries = [
            "What's the weather in Tokyo?",
            "What time is it?",
            "Calculate 15 + 27"
        ]
        
        for query in queries:
            print(f"\nQuery: {query}")
            result = agent.run_sync(query, deps={})
            print(f"Response: {result.output}")
            
    except Exception as e:
        print(f"Error: {e}")

def interactive_agent_builder():
    """Interactive agent builder"""
    print("\n🎮 Interactive Agent Builder")
    print("=" * 40)
    
    builder = SimpleAgentBuilder()
    
    while True:
        print("\nChoose an agent type:")
        print("1. Roulette Agent")
        print("2. Assistant Agent") 
        print("3. Multi-Tool Agent")
        print("4. Quit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "4":
            print("Goodbye! 👋")
            break
        
        elif choice == "1":
            print("\nRoulette Rules: enthusiastic, professional, casual")
            rules = input("Choose rules (default: enthusiastic): ").strip() or "enthusiastic"
            
            agent = builder.roulette_agent(rules)
            winning_number = int(input("Set winning number (1-36): ") or "18")
            
            while True:
                query = input("\nYour bet (or 'back' to menu): ").strip()
                if query.lower() == 'back':
                    break
                try:
                    result = agent.run_sync(query, deps=winning_number)
                    print(f"Result: {'🎉 Winner!' if result.output else '💔 Loser!'}")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif choice == "2":
            print("\nPersonalities: helpful, creative, technical, casual")
            personality = input("Choose personality (default: helpful): ").strip() or "helpful"
            
            agent = builder.assistant_agent(personality)
            
            while True:
                query = input("\nYour question (or 'back' to menu): ").strip()
                if query.lower() == 'back':
                    break
                try:
                    result = agent.run_sync(query)
                    print(f"Response: {result.output}")
                except Exception as e:
                    print(f"Error: {e}")
        
        elif choice == "3":
            agent = builder.multi_tool_agent()
            
            while True:
                query = input("\nYour request (or 'back' to menu): ").strip()
                if query.lower() == 'back':
                    break
                try:
                    result = agent.run_sync(query, deps={})
                    print(f"Response: {result.output}")
                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    try:
        demo_simple_agents()
        interactive_agent_builder()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure LM Studio is running with your model loaded!")
