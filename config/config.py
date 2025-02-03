import json
import os
import yaml 

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.config_data = {}
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_dir = os.path.dirname(__file__)
        project_root = os.path.dirname(os.path.dirname(__file__))
        
        config_path = os.path.join(project_root, 'config.yaml')
        template_path = os.path.join(project_root, 'config.yaml.template')

        if os.path.exists(config_path):
            with open(config_path, 'r') as file:
                self.config_data = yaml.safe_load(file)
        elif os.path.exists(template_path):
            with open(template_path, 'r') as file:
                self.config_data = yaml.safe_load(file)
        else:
            self._load_default_config()

        # Create config.yaml if it doesn't exist
        if not os.path.exists(config_path):
            self.save_config()

    def save_config(self):
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.yaml')
        with open(config_path, 'w') as file:
            yaml.safe_dump(self.config_data, file, default_flow_style=False)

    def _load_default_config(self):
        self.config_data = {
            'llm': {
                'client_type': 'ollama',
                'ollama': {
                    'model_name': 'llama2'
                },
                'gemini': {
                    'model_name': 'gemini-pro',
                    'api_key': ''
                }
            }
        }

    def set_config(self, key_path, value):
        keys = key_path.split('.')
        current = self.config_data
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        current[keys[-1]] = value

    def get_config(self, key_path):
        keys = key_path.split('.')
        current = self.config_data
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return None
            current = current[key]
        return current

    def print_config(self):
        print(yaml.dump(self.config_data, default_flow_style=False))

# Example usage (for demonstration, can be removed later)
if __name__ == '__main__':
    config = Config()
    config.set_config("llm_client_type", "ollama")
    config.set_config("ollama_model_name", "llama2")
    config.print_config()