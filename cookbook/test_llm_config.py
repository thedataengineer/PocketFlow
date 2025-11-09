"""
Tests for LLM Configuration Module

Run with: python -m pytest test_llm_config.py -v
Or: python test_llm_config.py
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from llm_config_shared import LLMConfig, LLMProvider, LLMFactory, call_llm


class TestLLMConfig(unittest.TestCase):
    """Test LLMConfig initialization and validation"""
    
    def setUp(self):
        """Clear environment variables before each test"""
        for key in ["LLM_PROVIDER", "LLM_MODEL", "LLM_API_KEY", "LLM_BASE_URL", 
                    "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "AZURE_API_KEY"]:
            os.environ.pop(key, None)
    
    def test_default_ollama_config(self):
        """Test default Ollama configuration"""
        config = LLMConfig()
        self.assertEqual(config.provider, "ollama")
        self.assertEqual(config.model, "llama3.2:3b")
        self.assertEqual(config.base_url, "http://localhost:11434/v1")
        self.assertEqual(config.api_key, "ollama")
    
    def test_openai_config_from_env(self):
        """Test OpenAI configuration from environment variables"""
        os.environ["LLM_PROVIDER"] = "openai"
        os.environ["OPENAI_API_KEY"] = "sk-test-key"
        
        config = LLMConfig()
        self.assertEqual(config.provider, "openai")
        self.assertEqual(config.api_key, "sk-test-key")
        self.assertEqual(config.model, "gpt-4o-mini")
    
    def test_anthropic_config(self):
        """Test Anthropic configuration"""
        os.environ["LLM_PROVIDER"] = "anthropic"
        os.environ["ANTHROPIC_API_KEY"] = "sk-ant-test"
        
        config = LLMConfig()
        self.assertEqual(config.provider, "anthropic")
        self.assertEqual(config.api_key, "sk-ant-test")
        self.assertEqual(config.model, "claude-3-5-sonnet-20241022")
    
    def test_azure_config(self):
        """Test Azure configuration"""
        os.environ["LLM_PROVIDER"] = "azure"
        os.environ["AZURE_API_KEY"] = "azure-key"
        os.environ["AZURE_ENDPOINT"] = "https://test.openai.azure.com/"
        
        config = LLMConfig()
        self.assertEqual(config.provider, "azure")
        self.assertEqual(config.api_key, "azure-key")
        self.assertEqual(config.base_url, "https://test.openai.azure.com/")
        self.assertEqual(config.model, "gpt-4")
    
    def test_missing_openai_api_key(self):
        """Test that missing OpenAI API key raises error"""
        os.environ["LLM_PROVIDER"] = "openai"
        with self.assertRaises(ValueError) as ctx:
            LLMConfig()
        self.assertIn("API key", str(ctx.exception))
    
    def test_missing_anthropic_api_key(self):
        """Test that missing Anthropic API key raises error"""
        os.environ["LLM_PROVIDER"] = "anthropic"
        with self.assertRaises(ValueError) as ctx:
            LLMConfig()
        self.assertIn("API key", str(ctx.exception))
    
    def test_missing_model(self):
        """Test that missing model raises error"""
        config = LLMConfig(provider="ollama")
        config.model = ""
        with self.assertRaises(ValueError) as ctx:
            config._validate_credentials()
        self.assertIn("Model not specified", str(ctx.exception))
    
    def test_temperature_validation(self):
        """Test temperature value validation and clamping"""
        # Valid temperature
        config = LLMConfig(temperature=0.5)
        self.assertEqual(config.temperature, 0.5)
        
        # Out of range - should clamp
        config = LLMConfig(temperature=3.0)
        self.assertEqual(config.temperature, 2.0)
        
        config = LLMConfig(temperature=-0.5)
        self.assertEqual(config.temperature, 0.0)
    
    def test_invalid_temperature_type(self):
        """Test that invalid temperature type is handled"""
        config = LLMConfig(temperature="not_a_number")
        self.assertEqual(config.temperature, 0.7)  # Should use default
    
    def test_azure_api_version_config(self):
        """Test Azure API version configuration"""
        config = LLMConfig(provider="ollama")  # Use ollama to avoid key validation
        self.assertEqual(config.azure_api_version, "2024-02-15-preview")
        
        config = LLMConfig(
            provider="ollama",
            azure_api_version="2024-01-01-preview"
        )
        self.assertEqual(config.azure_api_version, "2024-01-01-preview")
    
    def test_custom_parameters(self):
        """Test custom parameters are preserved"""
        config = LLMConfig(
            temperature=0.5,
            max_tokens=500,
            top_p=0.9
        )
        self.assertEqual(config.temperature, 0.5)
        self.assertEqual(config.max_tokens, 500)
        self.assertIn("top_p", config.extra_params)
        self.assertEqual(config.extra_params["top_p"], 0.9)


class TestLLMFactory(unittest.TestCase):
    """Test LLMFactory client creation"""
    
    def test_unsupported_provider(self):
        """Test that unsupported provider raises error"""
        config = LLMConfig(provider="ollama")
        config.provider = "unsupported_provider"
        
        with self.assertRaises(ValueError):
            LLMFactory.create_client(config)


class TestCallLLM(unittest.TestCase):
    """Test call_llm function"""
    
    def setUp(self):
        """Clear environment before each test"""
        for key in ["LLM_PROVIDER", "LLM_MODEL", "LLM_API_KEY"]:
            os.environ.pop(key, None)
    
    @patch('llm_config_shared.LLMFactory.create_client')
    def test_call_llm_with_default_config(self, mock_create_client):
        """Test call_llm with default configuration"""
        # Mock the OpenAI client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        mock_create_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Test"}]
        response = call_llm(messages)
        
        self.assertEqual(response, "Test response")
        mock_client.chat.completions.create.assert_called_once()
    
    @patch('llm_config_shared.LLMFactory.create_client')
    def test_call_llm_anthropic(self, mock_create_client):
        """Test call_llm with Anthropic provider"""
        os.environ["LLM_PROVIDER"] = "anthropic"
        os.environ["ANTHROPIC_API_KEY"] = "test-key"
        
        # Mock the Anthropic client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.content = [MagicMock()]
        mock_response.content[0].text = "Anthropic response"
        mock_client.messages.create.return_value = mock_response
        mock_create_client.return_value = mock_client
        
        messages = [{"role": "user", "content": "Test"}]
        config = LLMConfig()
        response = call_llm(messages, config)
        
        self.assertEqual(response, "Anthropic response")
        mock_client.messages.create.assert_called_once()
    
    def test_call_llm_missing_config(self):
        """Test that call_llm creates default config when none provided"""
        with patch('llm_config_shared.LLMFactory.create_client') as mock_create:
            mock_client = MagicMock()
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.content = "Test"
            mock_client.chat.completions.create.return_value = mock_response
            mock_create.return_value = mock_client
            
            messages = [{"role": "user", "content": "Test"}]
            call_llm(messages)  # No config provided
            
            # Should create a default config
            mock_create.assert_called_once()


class TestIntegration(unittest.TestCase):
    """Integration tests for configuration"""
    
    def setUp(self):
        """Clear environment"""
        for key in ["LLM_PROVIDER", "LLM_MODEL", "LLM_API_KEY", "LLM_BASE_URL",
                    "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "AZURE_API_KEY", "AZURE_ENDPOINT"]:
            os.environ.pop(key, None)
    
    def test_environment_variable_precedence(self):
        """Test that explicit parameters override environment variables"""
        os.environ["LLM_PROVIDER"] = "openai"
        os.environ["OPENAI_API_KEY"] = "env-key"
        
        # Explicit parameter should override
        config = LLMConfig(
            provider="anthropic",
            api_key="explicit-key"
        )
        self.assertEqual(config.provider, "anthropic")
        self.assertEqual(config.api_key, "explicit-key")
    
    def test_all_provider_defaults(self):
        """Test default models for each provider"""
        providers = {
            "ollama": "llama3.2:3b",
            "openai": "gpt-4o-mini",
            "anthropic": "claude-3-5-sonnet-20241022",
            "azure": "gpt-4",
        }
        
        for provider, expected_model in providers.items():
            os.environ["LLM_PROVIDER"] = provider
            
            # Set API keys for non-ollama providers
            if provider == "openai":
                os.environ["OPENAI_API_KEY"] = "test"
            elif provider == "anthropic":
                os.environ["ANTHROPIC_API_KEY"] = "test"
            elif provider == "azure":
                os.environ["AZURE_API_KEY"] = "test"
                os.environ["AZURE_ENDPOINT"] = "https://test.com"
            
            config = LLMConfig()
            self.assertEqual(config.model, expected_model)


if __name__ == "__main__":
    unittest.main()
