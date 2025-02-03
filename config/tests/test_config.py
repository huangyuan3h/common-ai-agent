import os
import unittest
from config.config import Config

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config()

    def test_get_set_config(self):
        self.config.set_config('test.key', 'test_value')
        self.assertEqual(self.config.get_config('test.key'), 'test_value')

    def test_nested_config(self):
        self.config.set_config('nested.key1.key2', 'nested_value')
        self.assertEqual(self.config.get_config('nested.key1.key2'), 'nested_value')

    def test_nonexistent_config(self):
        self.assertIsNone(self.config.get_config('nonexistent.key'))

if __name__ == '__main__':
    unittest.main()