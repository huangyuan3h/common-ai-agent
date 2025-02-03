from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from llm.llm_client import LLMClient

class GeminiClient(LLMClient):
    """
    LLM client for Google Gemini models.
    """

    def __init__(self, model_name: str = "gemini-pro", api_key: str = None):
        """
        Initializes GeminiClient with the specified model name and API key.

        Args:
            model_name (str): The name of the Gemini model to use. Defaults to "gemini-pro".
            api_key (str): The API key for Google Gemini.
        """
        self.model_name = model_name
        self.api_key = api_key
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=self.api_key)

    def generate_text(self, prompt: str, config: Dict[str, Any]) -> str:
        """
        Generates text using Gemini model.

        Args:
            prompt (str): The input prompt for text generation.
            config (Dict[str, Any]): Configuration parameters for text generation.

        Returns:
            str: The generated text from Gemini.
        """
        return self.llm.predict(prompt)

    def chat(self, messages: list, config: Dict[str, Any]) -> str:
        """
        Initiates a chat session with Gemini.

        Args:
            messages (list): A list of messages in the chat session.
            config (Dict[str, Any]): Configuration parameters for the chat session.

        Returns:
            str: The response from Gemini.
        """
        formatted_messages = [{"role": msg["role"], "content": msg["content"]} for msg in messages]
        return self.llm.predict_messages(formatted_messages).content
