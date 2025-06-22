#!/usr/bin/env python3
"""
Advanced Agent with streaming and async iteration
Demonstrates different ways to run agents
"""
import asyncio
from pydantic_ai import Agent
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

# Create agent
agent = Agent(
    model,
    system_prompt="You are a knowledgeable assistant that provides detailed explanations."
)

async def demo_run_methods():
    """Demonstrate different ways to run an agent"""
    print("🚀 Agent Run Methods Demo")
    print("=" * 40)
    
    # Method 1: Synchronous run
    print("\n1️⃣ Synchronous Run:")
    try:
        result_sync = agent.run_sync('What is the capital of Italy?')
        print(f"Result: {result_sync.output}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 2: Asynchronous run
    print("\n2️⃣ Asynchronous Run:")
    try:
        result = await agent.run('What is the capital of France?')
        print(f"Result: {result.output}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Method 3: Streaming run
    print("\n3️⃣ Streaming Run:")
    try:
        async with agent.run_stream('What is the capital of the UK?') as response:
            result = await response.get_output()
            print(f"Streamed Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

async def demo_agent_iteration():
    """Demonstrate agent graph iteration"""
    print("\n🔄 Agent Iteration Demo")
    print("=" * 40)
    
    try:
        nodes = []
        # Begin an AgentRun, which is an async-iterable over the nodes
        async with agent.iter('What is machine learning?') as agent_run:
            async for node in agent_run:
                # Each node represents a step in the agent's execution
                nodes.append(node)
                print(f"Node: {type(node).__name__}")
        
        print(f"\nTotal nodes processed: {len(nodes)}")
        print(f"Final result: {agent_run.result.output}")
        
    except Exception as e:
        print(f"Error: {e}")

async def interactive_chat():
    """Interactive chat using async agent"""
    print("\n💬 Interactive Async Chat")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    messages = []  # Store conversation history
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        try:
            # Run with conversation history
            result = await agent.run(user_input, message_history=messages)
            print(f"\nAgent: {result.output}")
            
            # Add to conversation history
            messages.extend(result.new_messages())
            
        except Exception as e:
            print(f"Error: {e}")

async def main():
    """Main function to run all demos"""
    await demo_run_methods()
    await demo_agent_iteration()
    await interactive_chat()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure LM Studio is running with your model loaded!")
