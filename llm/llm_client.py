from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMClient(ABC):
    """
    Abstract base class for LLM clients.
    """

    @abstractmethod
    def generate_text(self, prompt: str, config: Dict[str, Any]) -> str:
        """
        Generates text based on the given prompt and configuration.

        Args:
            prompt (str): The input prompt for text generation.
            config (Dict[str, Any]): Configuration parameters for text generation.

        Returns:
            str: The generated text.
        """
        pass

    @abstractmethod
    def chat(self, messages: list, config: Dict[str, Any]) -> str:
        """
        Initiates a chat session with the LLM.

        Args:
            messages (list): A list of messages in the chat session.
            config (Dict[str, Any]): Configuration parameters for the chat session.

        Returns:
            str: The response from the LLM.
        """
        pass
