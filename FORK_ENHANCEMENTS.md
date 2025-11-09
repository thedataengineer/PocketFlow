# PocketFlow Fork - LLM Provider Enhancements

This fork extends PocketFlow with flexible, multi-provider LLM support across all cookbook examples.

## What's New

### 🎯 Core Feature: Unified LLM Provider Interface

Switch between LLM providers **without changing code** - just set environment variables:

```bash
# Use Ollama (default)
python examples/pocketflow-chat/main.py

# Use OpenAI
export LLM_PROVIDER="openai"
export OPENAI_API_KEY="sk-..."
python examples/pocketflow-chat/main.py

# Use Anthropic
export LLM_PROVIDER="anthropic"
export ANTHROPIC_API_KEY="sk-ant-..."
python examples/pocketflow-chat/main.py
```

### 📚 Supported Providers

| Provider | Default Model | Free | Setup |
|----------|--------------|------|-------|
| **Ollama** | llama3.2:3b | ✅ | Local |
| **OpenAI** | gpt-4o-mini | ❌ | API key |
| **Anthropic** | claude-3-5-sonnet | ❌ | API key |
| **Azure OpenAI** | gpt-4 | ❌ | Enterprise |

### 📦 What Changed

**New Files**:
- `cookbook/llm_config_shared.py` - Centralized LLM configuration factory
- `cookbook/LLM_PROVIDER_GUIDE.md` - Complete documentation
- `cookbook/QUICK_START.md` - Quick reference card
- `.github/FORK_SETUP.md` - Fork maintenance guide

**Updated Files**: 24 cookbook examples
- All examples now use the shared config module
- Backward compatible - old examples still work
- No changes to core framework

**Branch**: `feature/flexible-llm-providers`

### 🚀 Quick Start

```bash
# 1. Install dependencies
cd cookbook/pocketflow-chat
pip install -r requirements.txt

# 2. Run with Ollama (requires: ollama serve)
python main.py

# 3. Or use OpenAI
export LLM_PROVIDER=openai
export OPENAI_API_KEY=sk-...
python main.py
```

For more: See `cookbook/QUICK_START.md`

### 🛠️ Features

- ✅ **Environment Variable Configuration** - No code changes needed
- ✅ **Factory Pattern** - Clean client creation for each provider
- ✅ **Default Fallbacks** - Sensible defaults for each provider
- ✅ **Error Handling** - Clear messages for missing keys/models
- ✅ **Documentation** - Comprehensive guides for each provider
- ✅ **Examples** - 24+ cookbook examples ready to use
- ✅ **Backward Compatible** - Original repo functionality unchanged

### 📖 Documentation

1. **For Quick Setup**: Read `cookbook/QUICK_START.md`
2. **For Complete Guide**: Read `cookbook/LLM_PROVIDER_GUIDE.md`
3. **For Fork Maintenance**: Read `.github/FORK_SETUP.md`

### 💻 Technical Details

**Architecture**:
```
Examples Layer (cookbook/)
    ↓
llm_config_shared.py (LLMConfig + LLMFactory)
    ↓
Provider Clients (OpenAI SDK, Anthropic SDK, etc.)
    ↓
LLM APIs (Ollama, OpenAI, Anthropic, Azure)

Core Framework (pocketflow/) - UNCHANGED
```

**Integration Pattern**:
```python
# In any example's utils.py
from llm_config_shared import call_llm, LLMConfig

def call_llm(prompt, config=None):
    config = config or LLMConfig()  # Auto-loads from env
    return shared_call_llm([{"role": "user", "content": prompt}], config)
```

### 🔄 Updating Examples

To update any example to use this feature:

```python
import sys
from pathlib import Path

# Add import path
sys.path.insert(0, str(Path(__file__).parent.parent))
from llm_config_shared import call_llm, LLMConfig

# Use it
config = LLMConfig()
response = call_llm(messages, config)
```

### 🐛 Known Limitations

- Streaming not fully abstracted (provider-specific in some examples)
- Structured output support varies by provider
- Vision models not yet abstracted
- Tools/function calling patterns differ between providers

### 📝 Environment Variables Reference

```bash
# Common
LLM_PROVIDER          # ollama, openai, anthropic, azure
LLM_MODEL            # Model ID/name
LLM_API_KEY          # Generic API key
LLM_BASE_URL         # Custom endpoint

# OpenAI-specific
OPENAI_API_KEY       # Alternative to LLM_API_KEY

# Anthropic-specific
ANTHROPIC_API_KEY    # Alternative to LLM_API_KEY

# Azure-specific
AZURE_API_KEY        # Alternative to LLM_API_KEY
AZURE_ENDPOINT       # Azure resource URL
```

### 🤝 Contributing Back

To submit to original repo:

1. Ensure you're on `feature/flexible-llm-providers`
2. Create PR to `The-Pocket/PocketFlow` with this branch
3. Include documentation links
4. Reference this fork

```bash
# Check difference from upstream
git log upstream/main..feature/flexible-llm-providers
```

### 🔗 Related Repositories

- **Original**: https://github.com/The-Pocket/PocketFlow
- **Upstream**: Keep synced with `git fetch upstream`

### 📊 Test Results

All 24+ examples tested with Ollama llama3.2:3b ✅

```bash
# Test basic functionality
cd cookbook/pocketflow-chat
python main.py <<< $'Hello!\nexit'
```

### 🎓 Learning Resources

- Ollama: https://ollama.ai
- OpenAI API: https://platform.openai.com/docs
- Anthropic API: https://docs.anthropic.com
- Azure OpenAI: https://learn.microsoft.com/en-us/azure/ai-services/openai/

### 📄 License

Same as PocketFlow (original repository license applies)

### 🎯 Next Steps

- [ ] Test all 24+ examples with different providers
- [ ] Add streaming abstractions
- [ ] Add vision/tool abstractions
- [ ] Submit PR to original repo
- [ ] Monitor upstream changes and rebase as needed

---

**Commit**: `ea3838c` - Feature/flexible-llm-providers branch
**Last Updated**: 2025-01-09
