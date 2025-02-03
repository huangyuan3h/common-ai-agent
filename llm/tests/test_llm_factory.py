import unittest
from llm.llm_factory import create_llm_client
from llm.ollama_client import OllamaClient
from llm.gemini_client import GeminiClient

class TestLLMFactory(unittest.TestCase):

    def test_create_ollama_client(self):
        config = {"client_type": "ollama", "model_name": "llama2"}
        client = create_llm_client(config)
        self.assertIsInstance(client, OllamaClient)
        self.assertEqual(client.model_name, "llama2")

    def test_create_gemini_client(self):
        config = {"client_type": "gemini", "api_key": "test_key", "model_name": "gemini-pro"}
        client = create_llm_client(config)
        self.assertIsInstance(client, GeminiClient)
        self.assertEqual(client.model_name, "gemini-pro")
        self.assertEqual(client.api_key, "test_key")

    def test_create_gemini_client_missing_api_key(self):
        config = {"client_type": "gemini", "model_name": "gemini-pro"}
        with self.assertRaisesRegex(ValueError, "API key is required for Gemini client."):
            create_llm_client(config)

    def test_create_invalid_client_type(self):
        config = {"client_type": "invalid"}
        with self.assertRaisesRegex(ValueError, "Invalid client type: invalid. Supported types are 'ollama', 'gemini'."):
            create_llm_client(config)

    def test_create_client_missing_client_type(self):
        config = {"model_name": "llama2"}
        with self.assertRaisesRegex(ValueError, "Configuration must contain 'client_type' to specify the LLM client."):
            create_llm_client(config)

if __name__ == '__main__':
    unittest.main()
