from typing import Dict, Any
from llm.llm_client import LLMClient
from llm.ollama_client import OllamaClient
from llm.gemini_client import GeminiClient

def create_llm_client(config: Dict[str, Any]) -> LLMClient:
    """
    Factory method to create LLM clients based on the given configuration.

    Args:
        config (Dict[str, Any]): Configuration parameters for LLM client creation.
            Must contain 'client_type' key to specify the type of LLM client.

    Returns:
        LLMClient: An instance of the LLMClient based on the configuration.

    Raises:
        ValueError: If 'client_type' is not provided or an invalid client type is specified.
    """
    client_type = config.get("client_type")

    if not client_type:
        raise ValueError("Configuration must contain 'client_type' to specify the LLM client.")

    if client_type == "ollama":
        model_name = config.get("model_name", "llama2")
        return OllamaClient(model_name=model_name)
    elif client_type == "gemini":
        api_key = config.get("api_key")
        model_name = config.get("model_name", "gemini-pro")
        if not api_key:
            raise ValueError("API key is required for Gemini client.")
        return GeminiClient(api_key=api_key, model_name=model_name)
    else:
        raise ValueError(f"Invalid client type: {client_type}. Supported types are 'ollama', 'gemini'.")
