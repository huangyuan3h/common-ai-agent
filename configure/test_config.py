import unittest
import os
import yaml
from configure.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        # Create a temporary config file for testing
        self.config_path = os.path.join(os.path.dirname(__file__), 'default_config.yaml')
        self.config = Config()

    def test_default_config_loading(self):
        # Test default configuration values
        self.assertEqual(self.config.get_config('llm.client_type'), 'ollama')
        self.assertEqual(self.config.get_config('llm.ollama.model_name'), 'llama2')
        self.assertEqual(self.config.get_config('llm.gemini.model_name'), 'gemini-pro')
        self.assertEqual(self.config.get_config('llm.gemini.api_key'), '')

    def test_set_and_get_config(self):
        # Test setting and getting configuration values
        test_api_key = 'test_api_key_123'
        self.config.set_config('llm.gemini.api_key', test_api_key)
        self.assertEqual(self.config.get_config('llm.gemini.api_key'), test_api_key)

    def test_save_and_load_config(self):
        # Test saving and loading configuration
        test_api_key = 'test_api_key_456'
        self.config.set_config('llm.gemini.api_key', test_api_key)
        self.config.save_config()

        # Create a new instance to load the saved config
        new_config = Config()
        self.assertEqual(new_config.get_config('llm.gemini.api_key'), test_api_key)

    def test_nested_config_access(self):
        # Test accessing nested configuration
        self.config.set_config('llm.test.nested.value', 'test_value')
        self.assertEqual(self.config.get_config('llm.test.nested.value'), 'test_value')

    def test_invalid_config_access(self):
        # Test accessing non-existent configuration
        self.assertIsNone(self.config.get_config('non.existent.key'))

if __name__ == '__main__':
    unittest.main()