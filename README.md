# Pydantic AI with Custom OpenAI Clients

This repository demonstrates various ways to use Pydantic AI with custom OpenAI clients, including local servers like LM Studio.

## Installation

```bash
pip install pydantic-ai[openai]
# or
pip install pydantic-ai-slim openai
```

## Examples

### 1. Basic OpenAI Client (Direct)

```python
from openai import OpenAI

# Point to your local LM Studio server
client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="lm-studio"
)

completion = client.chat.completions.create(
    model="ibm/granite-3.2-8b",
    messages=[
        {"role": "system", "content": "Always answer in rhymes."},
        {"role": "user", "content": "Introduce yourself."}
    ],
    temperature=0.7,
)

print(completion.choices[0].message.content)
```

### 2. Pydantic AI with OpenAI Provider

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Method 1: Using base_url and api_key
model = OpenAIModel(
    'ibm/granite-3.2-8b',
    provider=OpenAIProvider(
        base_url='http://localhost:1234/v1',
        api_key='lm-studio'
    )
)

agent = Agent(model, system_prompt="You are a helpful assistant.")
result = agent.run_sync("Hello!")
print(result.data)
```

### 3. Pydantic AI with Custom AsyncOpenAI Client

```python
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Create custom async client
custom_client = AsyncOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    timeout=30.0
)

# Use custom client with Pydantic AI
model = OpenAIModel(
    'ibm/granite-3.2-8b',
    provider=OpenAIProvider(openai_client=custom_client)
)

agent = Agent(model)
result = agent.run_sync("Tell me a joke!")
print(result.data)
```

### 4. Azure OpenAI Integration

```python
from openai import AsyncAzureOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

client = AsyncAzureOpenAI(
    azure_endpoint='https://your-resource.openai.azure.com/',
    api_version='2024-07-01-preview',
    api_key='your-api-key',
)

model = OpenAIModel(
    'gpt-4o',
    provider=OpenAIProvider(openai_client=client),
)

agent = Agent(model)
```

### 5. OpenAI Responses API

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel

# Basic Responses API
model = OpenAIResponsesModel('gpt-4o')
agent = Agent(model)
result = agent.run_sync('What is AI?')
print(result.data)
```

### 6. OpenAI Responses API with Built-in Tools

```python
from openai.types.responses import WebSearchToolParam
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel, OpenAIResponsesModelSettings

model_settings = OpenAIResponsesModelSettings(
    openai_builtin_tools=[WebSearchToolParam(type='web_search_preview')],
)

model = OpenAIResponsesModel('gpt-4o')
agent = Agent(model=model, model_settings=model_settings)

result = agent.run_sync('What is the weather in Tokyo?')
print(result.data)
```

### 7. Custom Model Profile

```python
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.profiles._json_schema import InlineDefsJsonSchemaTransformer
from pydantic_ai.profiles.openai import OpenAIModelProfile
from pydantic_ai.providers.openai import OpenAIProvider

model = OpenAIModel(
    'model_name',
    provider=OpenAIProvider(
        base_url='https://api.provider.com/v1',
        api_key='your-api-key'
    ),
    profile=OpenAIModelProfile(
        json_schema_transformer=InlineDefsJsonSchemaTransformer,
        openai_supports_strict_tool_definition=False
    )
)

agent = Agent(model)
```

## OpenAI-Compatible Providers

Many providers are compatible with the OpenAI API:

- **LM Studio** (local): `http://localhost:1234/v1`
- **Ollama** (local): `http://localhost:11434/v1`  
- **DeepSeek**: Available through OpenAI-compatible endpoint
- **OpenRouter**: Access to various models
- **Together AI**: Multiple open-source models
- **Groq**: Fast inference for Llama, Mixtral, etc.

## Built-in Provider Support

Some providers have dedicated support in Pydantic AI:

```python
# Shorthand syntax for supported providers
agent = Agent("deepseek:deepseek-chat")
agent = Agent("openrouter:google/gemini-2.5-pro-preview")
```

## Environment Variables

Set your API keys using environment variables:

```bash
export OPENAI_API_KEY="your-openai-key"
export DEEPSEEK_API_KEY="your-deepseek-key"
export OPENROUTER_API_KEY="your-openrouter-key"
```

## Files in this Repository

- `app.py` - Main example with both direct OpenAI and Pydantic AI usage
- `pydantic_ai_example.py` - Focused Pydantic AI examples
- `responses_api_example.py` - OpenAI Responses API examples
- `README.md` - This documentation

## Running the Examples

1. Start LM Studio and load a model
2. Run the examples:
   ```bash
   python app.py
   python pydantic_ai_example.py
   python responses_api_example.py
   ```

## Troubleshooting

- Ensure your local server (LM Studio) is running
- Check that the model name matches what's available in your server
- Verify the base_url and port are correct
- For timeout issues, increase the timeout parameter

## Learn More

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [LM Studio Documentation](https://lmstudio.ai/docs)
