import sys
from pathlib import Path

# Add parent directory to path to import shared config
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_config_shared import call_llm as shared_call_llm, LLMConfig

def call_llm(prompt, config: LLMConfig = None):
    """Call LLM with prompt string"""
    messages = [{"role": "user", "content": prompt}]
    return shared_call_llm(messages, config)

# Example usage
if __name__ == "__main__":
    config = LLMConfig()
    print(f"Using {config.provider} with model {config.model}")
    print(call_llm("Tell me a short joke", config))
