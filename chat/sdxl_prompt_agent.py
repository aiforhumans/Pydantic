#!/usr/bin/env python3
"""
SDXL Prompt Agent
Generate positive and negative prompts for Stable Diffusion XL.
"""
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider


class SDXLPrompts(BaseModel):
    """Structured output for SDXL prompts."""
    prompt: str
    negative_prompt: str


# Configure the local model (LM Studio)
model = OpenAIModel(
    'ibm/granite-3.2-8b',
    provider=OpenAIProvider(
        base_url='http://localhost:1234/v1',
        api_key='lm-studio'
    ),
)

# Create the SDXL prompt agent
sdxl_agent = Agent(
    model,
    output_type=SDXLPrompts,
    system_prompt=(
        "You are an expert Stable Diffusion XL prompt engineer. "
        "Given a user description, craft a vivid positive prompt and a concise "
        "negative prompt. Always respond with JSON using the fields 'prompt' "
        "and 'negative_prompt'."
    ),
)


def interactive_prompting() -> None:
    """Interactive prompt generation loop."""
    print("\U0001f3a8 SDXL Prompt Generator")
    print("Type 'quit' to exit")
    print("-" * 30)

    while True:
        user_input = input("\nDescribe the image: ").strip()

        if user_input.lower() in {'quit', 'exit', 'q'}:
            print("Goodbye! \U0001f5bc")
            break

        if not user_input:
            continue

        try:
            result = sdxl_agent.run_sync(user_input)
            print(f"\nPositive: {result.data.prompt}")
            print(f"Negative: {result.data.negative_prompt}")
        except Exception as exc:
            print(f"Error: {exc}")


if __name__ == '__main__':
    interactive_prompting()
