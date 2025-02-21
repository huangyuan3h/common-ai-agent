import pytest
from llm.llm_factory import create_llm_client
from config import Config
from llm.gemini_client import GeminiClient
from llm.ollama_client import OllamaClient

@pytest.fixture
def config():
    return Config()

def test_create_ollama_client(config):
    config.set_config("llm.client_type", "ollama")
    config.set_config("llm.ollama.model_name", "llama2")
    
    client = create_llm_client(config)
    assert isinstance(client, OllamaClient)
    assert client.model_name == "llama2"

def test_create_gemini_client(config):
    config.set_config("llm.client_type", "gemini")
    config.set_config("llm.gemini.model_name", "gemini-pro")
    config.set_config("llm.gemini.api_key", "test_api_key")
    
    client = create_llm_client(config)
    assert isinstance(client, GeminiClient)
    assert client.model_name == "gemini-pro"
    assert client.api_key == "test_api_key"

def test_invalid_client_type(config):
    config.set_config("llm.client_type", "invalid_client")
    
    with pytest.raises(ValueError, match="Invalid client type: invalid_client"):
        create_llm_client(config)

def test_missing_api_key_for_gemini(config):
    config.set_config("llm.client_type", "gemini")
    config.set_config("llm.gemini.model_name", "gemini-pro")
    config.set_config("llm.gemini.api_key", None)
    
    with pytest.raises(ValueError, match="API key is required for Gemini client."):
        create_llm_client(config)
