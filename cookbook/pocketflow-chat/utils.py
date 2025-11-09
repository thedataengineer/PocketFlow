import sys
from pathlib import Path

# Add parent directory to path to import shared config
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_config_shared import call_llm as shared_call_llm, LLMConfig

def call_llm(messages, config: LLMConfig = None):
    """
    Call LLM with flexible provider support.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        config: LLMConfig instance (uses default if None)
    
    Returns:
        str: LLM response text
    """
    return shared_call_llm(messages, config)


if __name__ == "__main__":
    # Test with default config
    config = LLMConfig()
    messages = [{"role": "user", "content": "In a few words, what's the meaning of life?"}]
    
    print(f"Using provider: {config.provider}")
    print(f"Using model: {config.model}")
    response = call_llm(messages, config)
    print(f"Prompt: {messages[0]['content']}")
    print(f"Response: {response}")
    
    # Example: Override with OpenAI
    # config = LLMConfig(provider="openai", model="gpt-4o")
    # response = call_llm(messages, config)
    
    # Example: Use Anthropic
    # config = LLMConfig(provider="anthropic", model="claude-3-5-sonnet-20241022")
    # response = call_llm(messages, config)

