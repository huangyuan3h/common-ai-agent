import pytest
from config import Config

@pytest.fixture
def config():
    return Config()

def test_get_set_config(config):
    config.set_config('test.key', 'test_value')
    assert config.get_config('test.key') == 'test_value'

def test_nested_config(config):
    config.set_config('nested.key1.key2', 'nested_value')
    assert config.get_config('nested.key1.key2') == 'nested_value'

def test_nonexistent_config(config):
    assert config.get_config('nonexistent.key') is None