# Working examples with local LM Studio server
from openai import OpenAI
import httpx
import asyncio

print("=== Testing OpenAI Client Direct ===")

# Create client with proper timeout settings
client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio",
    timeout=30.0  # 30 second timeout
)

print("Client created successfully!")

try:
    print("Listing available models...")
    models = client.models.list()
    print("Available models:")
    for model in models.data:
        print(f"  - {model.id}")
    
    print("\nMaking chat completion request...")
    completion = client.chat.completions.create(
        model="ibm/granite-3.2-8b",
        messages=[
            {"role": "system", "content": "Always answer in rhymes."},
            {"role": "user", "content": "Introduce yourself."}
        ],
        temperature=0.7,
        max_tokens=100
    )
    
    print("✅ OpenAI Direct Response:")
    print(completion.choices[0].message.content)
    
except Exception as e:
    print(f"❌ Error with OpenAI client: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*50)
print("=== Testing Pydantic AI with Custom OpenAI Client ===")

try:
    from openai import AsyncOpenAI
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIModel
    from pydantic_ai.providers.openai import OpenAIProvider
    
    # Method 1: Using OpenAIProvider with base_url and api_key
    print("Method 1: Using OpenAIProvider with base_url...")
    model1 = OpenAIModel(
        'ibm/granite-3.2-8b',
        provider=OpenAIProvider(
            base_url='http://localhost:1234/v1',
            api_key='lm-studio'
        )
    )
    
    agent1 = Agent(model1, system_prompt="Always answer in rhymes.")
    result1 = agent1.run_sync("Introduce yourself in one sentence.")
    print("✅ Method 1 Response:")
    print(result1.data)
    
    print("\n" + "-"*30)
    print("Method 2: Using custom AsyncOpenAI client...")
    
    # Method 2: Using custom AsyncOpenAI client
    custom_client = AsyncOpenAI(
        base_url="http://localhost:1234/v1",
        api_key="lm-studio",
        timeout=30.0
    )
    
    model2 = OpenAIModel(
        'ibm/granite-3.2-8b',
        provider=OpenAIProvider(openai_client=custom_client)
    )
    
    agent2 = Agent(model2, system_prompt="Always answer in rhymes.")
    result2 = agent2.run_sync("Tell me about artificial intelligence briefly.")
    print("✅ Method 2 Response:")
    print(result2.data)
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure pydantic-ai is properly installed")
    
except Exception as e:
    print(f"❌ Error with Pydantic AI: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Script completed!")
