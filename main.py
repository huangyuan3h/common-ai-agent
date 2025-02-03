from llm.llm_factory import create_llm_client
from configure.config import Config

def main():
    # Load configuration
    config = Config()

    # LLM client configuration from Config
    llm_config = {
        "client_type": config.get_config("llm.client_type"),
        "model_name": config.get_config(f"llm.{config.get_config('llm.client_type')}.model_name")
    }

    # Add API key for Gemini if needed
    if llm_config["client_type"] == "gemini":
        llm_config["api_key"] = config.get_config("llm.gemini.api_key")

    # Create LLM client using the factory
    llm_client = create_llm_client(llm_config)

    # Test LLM client: generate text
    prompt = "请介绍一下 Langchain"
    print(f"Prompt: {prompt}")
    response = llm_client.generate_text(prompt, {})
    print(f"LLM Response:\n{response}")

    # You can add more tests or interactions here if needed

if __name__ == "__main__":
    main()
