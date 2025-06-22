#!/usr/bin/env python3
"""
Roulette Wheel Agent - Advanced example with tools and structured output
Based on the PydanticAI documentation example
"""
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

# Create roulette agent with dependencies and structured output
roulette_agent = Agent(
    model,
    deps_type=int,  # The winning number as dependency
    output_type=bool,  # Return True for winner, False for loser
    system_prompt=(
        'You are a roulette wheel operator. Use the `roulette_wheel` function to '
        'check if the customer has won based on the number they provide. '
        'Be enthusiastic and engaging in your responses!'
    ),
)

@roulette_agent.tool
async def roulette_wheel(ctx: RunContext[int], square: int) -> str:
    """Check if the square is a winner"""
    winning_number = ctx.deps
    result = 'winner' if square == winning_number else 'loser'
    print(f"🎰 Roulette spin: Player bet {square}, winning number is {winning_number} -> {result}")
    return result

def test_roulette():
    """Test the roulette agent"""
    print("🎰 Roulette Wheel Agent Test")
    print("=" * 40)
    
    success_number = 18  # The winning number
    
    # Test case 1: Winning bet
    print("\n🎲 Test 1: Betting on 18 (winning number)")
    try:
        result = roulette_agent.run_sync(
            'Put my money on square eighteen', 
            deps=success_number
        )
        print(f"Result: {result.output} ({'🎉 Winner!' if result.output else '💔 Loser!'})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test case 2: Losing bet
    print("\n🎲 Test 2: Betting on 5 (losing number)")
    try:
        result = roulette_agent.run_sync(
            'I bet five is the winner', 
            deps=success_number
        )
        print(f"Result: {result.output} ({'🎉 Winner!' if result.output else '💔 Loser!'})")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test case 3: Interactive mode
    print("\n🎲 Interactive Mode:")
    print("Enter a number to bet on (1-36), or 'quit' to exit")
    
    while True:
        user_input = input("\nYour bet: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("Thanks for playing! 🎰")
            break
        
        try:
            bet_number = int(user_input)
            if 1 <= bet_number <= 36:
                result = roulette_agent.run_sync(
                    f'I am betting on number {bet_number}',
                    deps=success_number
                )
                print(f"Result: {result.output} ({'🎉 Winner!' if result.output else '💔 Loser!'})")
            else:
                print("Please enter a number between 1 and 36")
        except ValueError:
            print("Please enter a valid number")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_roulette()
