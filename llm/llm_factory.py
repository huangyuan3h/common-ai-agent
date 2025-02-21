from typing import Dict, Any
from llm.llm_client import LLMClient
from llm.ollama_client import OllamaClient
from llm.gemini_client import GeminiClient

def create_llm_client(config) -> LLMClient:
    """
    Factory method to create LLM clients based on the given configuration.

    Args:
        config: An instance of the Config class containing the LLM configuration.

    Returns:
        LLMClient: An instance of the LLMClient based on the configuration.

    Raises:
        ValueError: If client_type is not provided or an invalid client type is specified.
    """
    client_type = config.get_config("llm.client_type")
    print(f"Client type: {client_type}")  # 调试输出

    if not client_type:
        raise ValueError("Configuration must contain 'llm.client_type' to specify the LLM client.")

    if client_type == "ollama":
        model_name = config.get_config("llm.ollama.model_name")
        return OllamaClient(model_name=model_name)
    elif client_type == "gemini":
        api_key = config.get_config("llm.gemini.api_key")
        print(f"API key: {api_key}")  # 调试输出
        model_name = config.get_config("llm.gemini.model_name")
        if not api_key:
            raise ValueError("API key is required for Gemini client.")
        return GeminiClient(api_key=api_key, model_name=model_name)
    else:
        raise ValueError(f"Invalid client type: {client_type}. Supported types are 'ollama', 'gemini'.")
