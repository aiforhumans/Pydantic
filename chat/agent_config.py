#!/usr/bin/env python3
"""
Agent Configuration Module
Define different agent configurations and rules
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Configuration class for PydanticAI agents"""
    name: str
    system_prompt: str
    model_name: str = 'ibm/granite-3.2-8b'
    base_url: str = 'http://localhost:1234/v1'
    api_key: str = 'lm-studio'
    temperature: float = 0.7
    max_tokens: int = 500
    deps_type: type = int
    output_type: type = str
    tools_enabled: bool = True
    streaming_enabled: bool = False

# Predefined agent configurations
AGENT_CONFIGS = {
    "roulette": AgentConfig(
        name="Roulette Operator",
        system_prompt=(
            "You are an enthusiastic roulette wheel operator at a casino. "
            "Use the `roulette_wheel` function to check if customers win. "
            "Be engaging and entertaining in your responses! "
            "Always use the tool to check results before announcing winners."
        ),
        deps_type=int,
        output_type=bool,
        temperature=0.8,
        max_tokens=200
    ),
    
    "assistant": AgentConfig(
        name="General Assistant",
        system_prompt=(
            "You are a helpful and knowledgeable AI assistant. "
            "Provide clear, accurate, and concise responses. "
            "Always be polite and professional."
        ),
        temperature=0.7,
        max_tokens=300
    ),
    
    "creative": AgentConfig(
        name="Creative Writer",
        system_prompt=(
            "You are a creative writing assistant. "
            "Help users with storytelling, poetry, and creative content. "
            "Be imaginative and inspiring in your responses."
        ),
        temperature=0.9,
        max_tokens=600
    ),
    
    "technical": AgentConfig(
        name="Technical Expert",
        system_prompt=(
            "You are a technical expert specializing in programming and software development. "
            "Provide detailed, accurate technical explanations and code examples. "
            "Always include best practices and explain your reasoning."
        ),
        temperature=0.3,
        max_tokens=800
    ),
    
    "weather": AgentConfig(
        name="Weather Assistant",
        system_prompt=(
            "You are a weather information assistant. "
            "Use the available tools to provide accurate weather information. "
            "Always check the weather using tools before responding."
        ),
        deps_type=dict,
        output_type=dict,
        temperature=0.5,
        max_tokens=250
    ),
    
    "tutor": AgentConfig(
        name="Educational Tutor",
        system_prompt=(
            "You are a patient and encouraging educational tutor. "
            "Break down complex topics into simple, understandable parts. "
            "Ask questions to check understanding and provide examples."
        ),
        temperature=0.6,
        max_tokens=400
    )
}

# Rules and guidelines for different scenarios
AGENT_RULES = {
    "strict": {
        "temperature": 0.1,
        "max_tokens": 200,
        "additional_rules": [
            "Always be factual and precise",
            "Avoid speculation or uncertain information",
            "Keep responses concise and to the point"
        ]
    },
    
    "creative": {
        "temperature": 0.9,
        "max_tokens": 800,
        "additional_rules": [
            "Be imaginative and creative",
            "Use vivid descriptions and metaphors",
            "Encourage creative thinking"
        ]
    },
    
    "casual": {
        "temperature": 0.7,
        "max_tokens": 300,
        "additional_rules": [
            "Use a friendly, conversational tone",
            "Feel free to use humor when appropriate",
            "Be relatable and approachable"
        ]
    },
    
    "professional": {
        "temperature": 0.4,
        "max_tokens": 500,
        "additional_rules": [
            "Maintain a professional and formal tone",
            "Provide comprehensive and well-structured responses",
            "Include relevant details and context"
        ]
    }
}

def get_agent_config(config_name: str) -> AgentConfig:
    """Get a predefined agent configuration"""
    if config_name not in AGENT_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(AGENT_CONFIGS.keys())}")
    return AGENT_CONFIGS[config_name]

def apply_rules(config: AgentConfig, rule_set: str) -> AgentConfig:
    """Apply a rule set to an agent configuration"""
    if rule_set not in AGENT_RULES:
        raise ValueError(f"Unknown rule set: {rule_set}. Available: {list(AGENT_RULES.keys())}")
    
    rules = AGENT_RULES[rule_set]
    
    # Create a copy of the config
    new_config = AgentConfig(
        name=config.name,
        system_prompt=config.system_prompt,
        model_name=config.model_name,
        base_url=config.base_url,
        api_key=config.api_key,
        temperature=rules.get("temperature", config.temperature),
        max_tokens=rules.get("max_tokens", config.max_tokens),
        deps_type=config.deps_type,
        output_type=config.output_type,
        tools_enabled=config.tools_enabled,
        streaming_enabled=config.streaming_enabled
    )
    
    # Append additional rules to system prompt
    if "additional_rules" in rules:
        additional_rules = "\n\nAdditional Guidelines:\n"
        for rule in rules["additional_rules"]:
            additional_rules += f"- {rule}\n"
        new_config.system_prompt += additional_rules
    
    return new_config

def create_custom_config(
    name: str,
    system_prompt: str,
    **kwargs
) -> AgentConfig:
    """Create a custom agent configuration"""
    return AgentConfig(
        name=name,
        system_prompt=system_prompt,
        **kwargs
    )

def list_available_configs() -> List[str]:
    """List all available agent configurations"""
    return list(AGENT_CONFIGS.keys())

def list_available_rules() -> List[str]:
    """List all available rule sets"""
    return list(AGENT_RULES.keys())
