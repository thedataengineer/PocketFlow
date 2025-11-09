from llm_config import LLMConfig, LLMFactory, LLMProvider

def call_llm(messages, config: LLMConfig = None):
    """
    Call LLM with flexible provider support.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        config: LLMConfig instance (uses default if None)
    
    Returns:
        str: LLM response text
    """
    if config is None:
        config = LLMConfig()
    
    client = LLMFactory.create_client(config)
    
    if config.provider == LLMProvider.OPENAI.value or config.provider == LLMProvider.OLLAMA.value or config.provider == LLMProvider.AZURE.value:
        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            **config.extra_params
        )
        return response.choices[0].message.content
    
    elif config.provider == LLMProvider.ANTHROPIC.value:
        response = client.messages.create(
            model=config.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            **config.extra_params
        )
        return response.content[0].text
    
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")


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

