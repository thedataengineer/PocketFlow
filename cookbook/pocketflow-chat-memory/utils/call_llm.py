import sys
from pathlib import Path

# Add parent directory to path to import shared config
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from llm_config_shared import call_llm as shared_call_llm, LLMConfig

def call_llm(messages, config: LLMConfig = None):
    """Call LLM with message list"""
    return shared_call_llm(messages, config)

if __name__ == "__main__":
    # Test the LLM call
    config = LLMConfig()
    messages = [{"role": "user", "content": "In a few words, what's the meaning of life?"}]
    response = call_llm(messages, config)
    print(f"Using {config.provider} with model {config.model}")
    print(f"Prompt: {messages[0]['content']}")
    print(f"Response: {response}")
