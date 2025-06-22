#!/usr/bin/env python3
"""
Simple Agent example using local LM Studio
"""
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Create an agent with local LM Studio model
model = OpenAIModel(
    'ibm/granite-3.2-8b',  # Your local model name
    provider=OpenAIProvider(
        base_url='http://localhost:1234/v1',
        api_key='lm-studio'
    ),
)

# Simple agent with system prompt
agent = Agent(
    model,
    system_prompt="You are a helpful AI assistant that provides clear and concise answers."
)

def main():
    print("🤖 Simple Agent Chat")
    print("Type 'quit' to exit")
    print("-" * 30)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        try:
            # Run the agent synchronously
            result = agent.run_sync(user_input)
            print(f"\nAgent: {result.data}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
