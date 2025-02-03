from typing import Dict, Any
from langchain_ollama import OllamaLLM
from llm.llm_client import LLMClient

class OllamaClient(LLMClient):
    """
    LLM client for Ollama models.
    """

    def __init__(self, model_name: str = "llama2"):
        """
        Initializes OllamaClient with the specified model name.

        Args:
            model_name (str): The name of the Ollama model to use. Defaults to "llama2".
        """
        self.model_name = model_name
        self.llm = OllamaLLM(model=self.model_name)

    def generate_text(self, prompt: str, config: Dict[str, Any]) -> str:
        """
        Generates text using Ollama model.

        Args:
            prompt (str): The input prompt for text generation.
            config (Dict[str, Any]): Configuration parameters for text generation (not used for Ollama).

        Returns:
            str: The generated text from Ollama.
        """
        return self.llm.invoke(prompt)

    def chat(self, messages: list, config: Dict[str, Any]) -> str:
        """
        Initiates a chat session with Ollama (not directly supported, using generate_text).

        Args:
            messages (list): A list of messages in the chat session (only the last message is used as prompt).
            config (Dict[str, Any]): Configuration parameters for the chat session (not used for Ollama).

        Returns:
            str: The response from Ollama.
        """
        prompt = messages[-1]['content'] if messages else ""
        return self.generate_text(prompt, config)
