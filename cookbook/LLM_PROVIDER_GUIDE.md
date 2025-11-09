# LLM Provider Configuration Guide

This guide explains how to use multiple LLM providers and models across PocketFlow cookbook examples.

## Overview

The cookbook now supports flexible LLM provider configuration through:
- **llm_config_shared.py**: Centralized configuration module in the cookbook root
- **Environment variables**: Easy configuration without code changes
- **Direct configuration**: Programmatic LLM provider selection

## Supported Providers

### 1. Ollama (Default, Local, Free)
**Best for**: Local development, privacy-focused, no API costs

```bash
# Setup
ollama pull llama3.2
ollama serve

# Environment variables
export LLM_PROVIDER="ollama"
export LLM_MODEL="llama3.2:3b"
# No API key needed
```

**Available models**: llama3.2, llama2, mistral, neural-chat, dolphin-mixtral, etc.

### 2. OpenAI
**Best for**: High-quality responses, production use

```bash
# Environment variables
export LLM_PROVIDER="openai"
export LLM_MODEL="gpt-4o"
export OPENAI_API_KEY="sk-..."
```

**Available models**: gpt-4o, gpt-4-turbo, gpt-3.5-turbo, gpt-4

### 3. Anthropic (Claude)
**Best for**: Safer outputs, excellent reasoning

```bash
# Environment variables
export LLM_PROVIDER="anthropic"
export LLM_MODEL="claude-3-5-sonnet-20241022"
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Available models**: claude-3-5-sonnet-20241022, claude-3-opus-20240229, claude-3-haiku-20240307

### 4. Azure OpenAI
**Best for**: Enterprise customers, compliance requirements

```bash
# Environment variables
export LLM_PROVIDER="azure"
export LLM_MODEL="gpt-4"
export AZURE_API_KEY="your-key"
export AZURE_ENDPOINT="https://your-resource.openai.azure.com/"
```

## Usage Examples

### In Python Code

#### Default Configuration (Ollama)
```python
from llm_config_shared import call_llm, LLMConfig

# Uses default Ollama setup
response = call_llm([{"role": "user", "content": "Hello"}])
```

#### Custom Configuration
```python
from llm_config_shared import call_llm, LLMConfig

# Use OpenAI
config = LLMConfig(provider="openai", model="gpt-4o")
response = call_llm([{"role": "user", "content": "Hello"}], config)

# Use Anthropic
config = LLMConfig(provider="anthropic", model="claude-3-5-sonnet-20241022")
response = call_llm([{"role": "user", "content": "Hello"}], config)

# Use Azure
config = LLMConfig(
    provider="azure",
    model="gpt-4",
    api_key="your-key",
    base_url="https://your-resource.openai.azure.com/"
)
response = call_llm([{"role": "user", "content": "Hello"}], config)
```

#### With Custom Parameters
```python
config = LLMConfig(
    provider="openai",
    model="gpt-4o",
    temperature=0.5,
    max_tokens=1024
)
response = call_llm(messages, config)
```

### Running Examples

#### Example 1: Chat with Ollama (Default)
```bash
cd pocketflow-chat
python main.py
```

#### Example 2: Chat with OpenAI
```bash
export LLM_PROVIDER="openai"
export OPENAI_API_KEY="sk-..."
cd pocketflow-chat
python main.py
```

#### Example 3: Chat with Anthropic
```bash
export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-ant-..."
cd pocketflow-chat
python main.py
```

## Integration in Your Examples

### Template: Adding Multi-Provider Support

```python
# In your utils.py or call_llm.py
import sys
from pathlib import Path

# Import shared config
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_config_shared import call_llm as shared_call_llm, LLMConfig

def call_llm(messages, config: LLMConfig = None):
    """Your wrapper function"""
    if config is None:
        config = LLMConfig()
    return shared_call_llm(messages, config)

# Usage in main code
if __name__ == "__main__":
    config = LLMConfig()  # Reads from env or uses defaults
    print(f"Using {config.provider} with {config.model}")
    response = call_llm(messages, config)
```

## Updating Existing Examples

All examples have been updated to support multiple providers. To use a non-default provider:

1. Set environment variables:
   ```bash
   export LLM_PROVIDER="anthropic"
   export ANTHROPIC_API_KEY="your-key"
   ```

2. Run the example:
   ```bash
   python main.py
   ```

## Troubleshooting

### "Connection refused" for Ollama
- Ensure Ollama is running: `ollama serve`
- Check endpoint: `curl http://localhost:11434`

### OpenAI API key not working
- Verify key format: `sk-...`
- Check in OpenAI dashboard that key is active
- Verify no trailing whitespace: `echo -n $OPENAI_API_KEY`

### Model not found error
- Check available models: `ollama list` (for Ollama)
- Verify model name in environment variable
- For Ollama, pull first: `ollama pull llama3.2`

### Rate limiting
- Check provider rate limits
- Increase `max_tokens` cautiously
- Implement request delays if needed

## Environment Variable Reference

| Variable | Default | Description |
|----------|---------|-------------|
| LLM_PROVIDER | ollama | Provider name |
| LLM_MODEL | llama3.2:3b | Model identifier |
| LLM_API_KEY | (none) | Generic API key |
| LLM_BASE_URL | (provider-specific) | Custom endpoint |
| OPENAI_API_KEY | (none) | OpenAI API key |
| ANTHROPIC_API_KEY | (none) | Anthropic API key |
| AZURE_API_KEY | (none) | Azure API key |
| AZURE_ENDPOINT | (none) | Azure endpoint URL |

## Performance Comparison

| Provider | Speed | Quality | Cost | Setup |
|----------|-------|---------|------|-------|
| Ollama (llama3.2) | Fast | Good | Free | Easy (local) |
| OpenAI (gpt-4o) | Moderate | Excellent | $$$ | API key |
| Anthropic (Claude) | Moderate | Excellent | $$$ | API key |
| Azure OpenAI | Moderate | Excellent | $$$ | Enterprise |

## Adding New Providers

To add support for another provider:

1. Add provider enum to `LLMProvider`
2. Add defaults in `LLMConfig._set_provider_defaults()`
3. Add client creation in `LLMFactory.create_client()`
4. Add message format handling in `call_llm()` function
5. Update this guide

## Tips & Best Practices

- **Development**: Use Ollama for cost-effective testing
- **Testing**: Use smaller models (llama3.2:3b) for faster feedback
- **Production**: Use OpenAI or Anthropic for reliability
- **Cost control**: Monitor token usage, set `max_tokens`
- **Quality**: Tune `temperature` for your use case (lower = more deterministic)
- **Privacy**: Use Ollama when data sensitivity is high

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review provider-specific documentation
3. Check environment variables: `env | grep LLM`
4. Test with Ollama as baseline
