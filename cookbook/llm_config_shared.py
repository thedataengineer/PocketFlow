"""
Shared LLM Provider Configuration Module

Place this file in the cookbook root directory and import it from individual examples.
Examples can do: from sys import path; path.insert(0, '..'); from llm_config_shared import *
"""

import os
from typing import Optional, Dict, Any
from enum import Enum


class LLMProvider(Enum):
    """Supported LLM providers"""
    OLLAMA = "ollama"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    AZURE = "azure"


class LLMConfig:
    """Configuration for LLM provider and model"""
    
    def __init__(
        self,
        provider: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        """
        Initialize LLM configuration.
        
        Args:
            provider: LLM provider (ollama, openai, anthropic, azure)
            model: Model name/ID
            api_key: API key for the provider
            base_url: Base URL for the API endpoint
            **kwargs: Additional provider-specific parameters (temperature, max_tokens, etc.)
        """
        self.provider = provider or os.getenv("LLM_PROVIDER", "ollama")
        self.model = model or os.getenv("LLM_MODEL", "")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "")
        self.base_url = base_url or os.getenv("LLM_BASE_URL", "")
        self.temperature = float(kwargs.get("temperature", 0.7))
        self.max_tokens = int(kwargs.get("max_tokens", 2048))
        self.extra_params = {k: v for k, v in kwargs.items() 
                            if k not in ["temperature", "max_tokens"]}
        
        self._set_provider_defaults()
    
    def _set_provider_defaults(self):
        """Set provider-specific default values"""
        if self.provider == LLMProvider.OLLAMA.value:
            self.base_url = self.base_url or "http://localhost:11434/v1"
            self.api_key = self.api_key or "ollama"
            self.model = self.model or "llama3.2:3b"
        
        elif self.provider == LLMProvider.OPENAI.value:
            self.base_url = self.base_url or "https://api.openai.com/v1"
            self.api_key = self.api_key or os.getenv("OPENAI_API_KEY", "")
            self.model = self.model or "gpt-4o-mini"
        
        elif self.provider == LLMProvider.ANTHROPIC.value:
            self.api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY", "")
            self.model = self.model or "claude-3-5-sonnet-20241022"
        
        elif self.provider == LLMProvider.AZURE.value:
            self.base_url = self.base_url or os.getenv("AZURE_ENDPOINT", "")
            self.api_key = self.api_key or os.getenv("AZURE_API_KEY", "")
            self.model = self.model or "gpt-4"


class LLMFactory:
    """Factory for creating LLM clients"""
    
    @staticmethod
    def create_client(config: LLMConfig):
        """
        Create appropriate LLM client based on provider.
        
        Args:
            config: LLMConfig instance
            
        Returns:
            LLM client instance
        """
        if config.provider == LLMProvider.OLLAMA.value:
            from openai import OpenAI
            return OpenAI(api_key=config.api_key, base_url=config.base_url)
        
        elif config.provider == LLMProvider.OPENAI.value:
            from openai import OpenAI
            return OpenAI(api_key=config.api_key)
        
        elif config.provider == LLMProvider.ANTHROPIC.value:
            from anthropic import Anthropic
            return Anthropic(api_key=config.api_key)
        
        elif config.provider == LLMProvider.AZURE.value:
            from openai import AzureOpenAI
            return AzureOpenAI(
                api_key=config.api_key,
                api_version="2024-02-15-preview",
                azure_endpoint=config.base_url
            )
        
        else:
            raise ValueError(f"Unsupported provider: {config.provider}")


def call_llm(messages, config: LLMConfig = None) -> str:
    """
    Universal LLM call function supporting multiple providers.
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        config: LLMConfig instance (uses default if None)
    
    Returns:
        str: LLM response text
    """
    if config is None:
        config = LLMConfig()
    
    client = LLMFactory.create_client(config)
    
    # OpenAI-compatible providers (OpenAI, Ollama, Azure)
    if config.provider in [LLMProvider.OPENAI.value, LLMProvider.OLLAMA.value, LLMProvider.AZURE.value]:
        response = client.chat.completions.create(
            model=config.model,
            messages=messages,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            **config.extra_params
        )
        return response.choices[0].message.content
    
    # Anthropic provider
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


def get_default_config() -> LLMConfig:
    """Get default LLM configuration from environment"""
    return LLMConfig()
