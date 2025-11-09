# Fork Setup Guide

This is a forked repository of [The-Pocket/PocketFlow](https://github.com/The-Pocket/PocketFlow) with enhancements for flexible LLM provider support.

## Feature Branch

All changes are in the `feature/flexible-llm-providers` branch:

```bash
git checkout feature/flexible-llm-providers
```

To keep this separate from the original repo:

```bash
# Set original as upstream
git remote add upstream https://github.com/The-Pocket/PocketFlow.git

# Verify remotes
git remote -v
# origin   = your fork
# upstream = original repo

# Keep your main branch synced with upstream
git checkout main
git fetch upstream
git rebase upstream/main

# Feature branch stays independent
git checkout feature/flexible-llm-providers
```

## Changes Made

See commit: `ea3838c`

**Files Added**:
- `cookbook/llm_config_shared.py` - Shared LLM provider configuration
- `cookbook/LLM_PROVIDER_GUIDE.md` - Complete usage guide
- `cookbook/QUICK_START.md` - Quick reference
- `cookbook/pocketflow-chat/llm_config.py` - Chat-specific config (optional)

**Files Modified**: 24 cookbook examples updated to use shared config

**Core Framework**: No changes (all cookbook layer)

## Using This Fork

### Setup Your Own Fork

1. Fork on GitHub: https://github.com/The-Pocket/PocketFlow
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/PocketFlow.git
   ```
3. Add upstream:
   ```bash
   cd PocketFlow
   git remote add upstream https://github.com/The-Pocket/PocketFlow.git
   ```
4. Pull feature branch:
   ```bash
   git fetch origin feature/flexible-llm-providers
   git checkout feature/flexible-llm-providers
   ```

### Sync with Upstream

```bash
# Fetch latest from original repo
git fetch upstream

# Rebase feature branch on latest main
git checkout feature/flexible-llm-providers
git rebase upstream/main

# Push to your fork
git push origin feature/flexible-llm-providers
```

## Contributing Back

To submit these changes to the original repo:

1. Create a pull request from your fork's `feature/flexible-llm-providers` to `The-Pocket/PocketFlow`'s `main`
2. Include the commit message and references to:
   - `cookbook/LLM_PROVIDER_GUIDE.md`
   - `cookbook/QUICK_START.md`

## Branch Strategy

```
origin/main (your fork)
├── main
│   └── (synced with upstream/main)
└── feature/flexible-llm-providers
    └── (your enhancements)
```

## Directory Structure

```
PocketFlow/
├── pocketflow/          # Core framework (UNCHANGED)
├── cookbook/
│   ├── llm_config_shared.py           # NEW: Shared config
│   ├── LLM_PROVIDER_GUIDE.md           # NEW: Full guide
│   ├── QUICK_START.md                  # NEW: Quick reference
│   ├── pocketflow-chat/
│   │   ├── llm_config.py               # NEW: Local config (optional)
│   │   ├── main.py
│   │   └── utils.py                    # MODIFIED: Uses shared config
│   ├── pocketflow-agent/
│   │   └── utils.py                    # MODIFIED: Uses shared config
│   ├── pocketflow-hello-world/
│   │   └── utils/call_llm.py          # MODIFIED: Uses shared config
│   └── ... (other examples updated)
└── .github/
    └── FORK_SETUP.md                   # THIS FILE
```

## Git Commands Quick Reference

```bash
# Check which branch you're on
git branch

# Switch to feature branch
git checkout feature/flexible-llm-providers

# See what's different from upstream
git log upstream/main..feature/flexible-llm-providers

# Sync with upstream
git fetch upstream
git rebase upstream/main

# Push to your fork
git push origin feature/flexible-llm-providers
```

## Next Steps

1. **Test**: Run examples with different LLM providers
2. **Document**: Update your README if needed
3. **Share**: Push to your fork, create PR to original repo
4. **Maintain**: Keep feature branch synced with upstream/main
