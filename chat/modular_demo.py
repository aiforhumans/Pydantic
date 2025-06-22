#!/usr/bin/env python3
"""
Modular Roulette Agent Example
Using the new configurable agent system
"""
from agent_factory import factory, quick_agent
from agent_config import get_agent_config, apply_rules, list_available_configs, list_available_rules

def demo_modular_roulette():
    """Demonstrate the modular roulette agent"""
    print("🎰 Modular Roulette Agent Demo")
    print("=" * 50)
    
    # Method 1: Using preset configuration
    print("\n1️⃣ Using Preset Configuration")
    agent1 = quick_agent("roulette", tools=["roulette_wheel"])
    
    success_number = 18
    
    try:
        result = agent1.run_sync(
            "I'm betting on number 18!",
            deps=success_number
        )
        print(f"Result: {result.output}")
        print(f"Winner: {'🎉 Yes!' if result.output else '💔 No!'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 2: Using preset with rules
    print("\n2️⃣ Using Preset with Professional Rules")
    agent2 = quick_agent("roulette", rules="professional", tools=["roulette_wheel"])
    
    try:
        result = agent2.run_sync(
            "What are my chances with number 7?",
            deps=success_number
        )
        print(f"Result: {result.output}")
        print(f"Winner: {'🎉 Yes!' if result.output else '💔 No!'}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 3: Using preset with creative rules
    print("\n3️⃣ Using Preset with Creative Rules")
    agent3 = quick_agent("roulette", rules="creative", tools=["roulette_wheel"])
    
    try:
        result = agent3.run_sync(
            "I'm feeling lucky with number 25!",
            deps=success_number
        )
        print(f"Result: {result.output}")
        print(f"Winner: {'🎉 Yes!' if result.output else '💔 No!'}")
    except Exception as e:
        print(f"Error: {e}")

def interactive_config_demo():
    """Interactive demo showing configuration options"""
    print("\n🎛️ Interactive Configuration Demo")
    print("=" * 50)
    
    print("Available presets:", list_available_configs())
    print("Available rules:", list_available_rules())
    
    while True:
        print("\n" + "-" * 30)
        preset = input("Choose preset (or 'quit'): ").strip()
        
        if preset.lower() in ['quit', 'exit', 'q']:
            break
            
        if preset not in list_available_configs():
            print("Invalid preset. Try again.")
            continue
        
        rules = input("Choose rules (optional, press Enter to skip): ").strip()
        if rules and rules not in list_available_rules():
            print("Invalid rules, using default.")
            rules = None
        
        # Create agent based on preset
        if preset == "roulette":
            agent = quick_agent(preset, rules, tools=["roulette_wheel"])
            deps = 18  # winning number
        elif preset == "weather":
            agent = quick_agent(preset, rules, tools=["weather", "time"])
            deps = {}
        else:
            agent = quick_agent(preset, rules)
            deps = None
        
        # Test the agent
        query = input("Enter your query: ").strip()
        if not query:
            continue
            
        try:
            if deps is not None:
                result = agent.run_sync(query, deps=deps)
            else:
                result = agent.run_sync(query)
            print(f"\n🤖 Response: {result.output}")
        except Exception as e:
            print(f"Error: {e}")

def showcase_all_presets():
    """Showcase all available agent presets"""
    print("\n🎭 All Agent Presets Showcase")
    print("=" * 50)
    
    test_queries = {
        "assistant": "What is artificial intelligence?",
        "creative": "Write a short poem about coding.",
        "technical": "Explain how recursion works.",
        "tutor": "How do I learn programming?",
        "weather": "What's the weather like in Tokyo?",
        "roulette": "I'm betting on lucky number 13!"
    }
    
    for preset_name in list_available_configs():
        print(f"\n🎯 {preset_name.upper()} AGENT")
        print("-" * 25)
        
        try:
            # Special handling for different agent types
            if preset_name == "roulette":
                agent = quick_agent(preset_name, tools=["roulette_wheel"])
                result = agent.run_sync(test_queries[preset_name], deps=18)
            elif preset_name == "weather":
                agent = quick_agent(preset_name, tools=["weather"])
                result = agent.run_sync(test_queries[preset_name], deps={})
            else:
                agent = quick_agent(preset_name)
                result = agent.run_sync(test_queries[preset_name])
            
            print(f"Query: {test_queries[preset_name]}")
            print(f"Response: {result.output}")
            
        except Exception as e:
            print(f"Error with {preset_name}: {e}")

if __name__ == "__main__":
    try:
        demo_modular_roulette()
        showcase_all_presets()
        interactive_config_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure LM Studio is running with your model loaded!")
