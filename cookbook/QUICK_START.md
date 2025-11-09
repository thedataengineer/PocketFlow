# Quick Start: Using Different LLM Providers

## TL;DR - Copy & Paste

### Use Ollama (Default, Free, Local)
```bash
cd pocketflow-chat
python main.py
```

### Use OpenAI
```bash
export LLM_PROVIDER="openai"
export OPENAI_API_KEY="sk-your-key-here"
cd pocketflow-chat
python main.py
```

### Use Anthropic (Claude)
```bash
export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
cd pocketflow-chat
python main.py
```

### Use Azure OpenAI
```bash
export LLM_PROVIDER="azure"
export AZURE_API_KEY="your-key"
export AZURE_ENDPOINT="https://your-resource.openai.azure.com/"
cd pocketflow-chat
python main.py
```

## One-Time Setup

### For Ollama
```bash
# Install Ollama from https://ollama.ai
# Pull a model
ollama pull llama3.2
# Start server (runs in background)
ollama serve
```

### For OpenAI
1. Get API key from https://platform.openai.com/api-keys
2. No installation needed, just use `export OPENAI_API_KEY="sk-..."`

### For Anthropic
1. Get API key from https://console.anthropic.com
2. No installation needed, just use `export ANTHROPIC_API_KEY="sk-ant-..."`

## Change Model

```bash
# OpenAI - use different model
export LLM_MODEL="gpt-4o-mini"

# Ollama - use different model
export LLM_MODEL="mistral"
ollama pull mistral

# Anthropic - use different model
export LLM_MODEL="claude-3-haiku-20240307"
```

## Verify Setup

```bash
# Test which provider you're using
python -c "
from llm_config_shared import LLMConfig
c = LLMConfig()
print(f'Provider: {c.provider}')
print(f'Model: {c.model}')
"
```

## Common Issues

| Problem | Solution |
|---------|----------|
| `Connection refused` on Ollama | Run `ollama serve` |
| `Invalid API key` | Check your key, no trailing spaces |
| `Model not found` | Pull it: `ollama pull llama3.2` |
| `Rate limit exceeded` | Wait or use different provider |

## Cost Comparison

- **Ollama**: Free (runs locally)
- **OpenAI**: ~$0.15/1M input tokens, ~$0.60/1M output tokens
- **Anthropic**: ~$0.80/1M input tokens, ~$2.40/1M output tokens

For quick testing, use Ollama. For production, use OpenAI or Anthropic.

## Full Guide

See `LLM_PROVIDER_GUIDE.md` for complete documentation.
