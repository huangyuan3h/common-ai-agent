from llm.llm_factory import create_llm_client
from config import Config

def main():
    # Load configuration
    config = Config()

    # Create LLM client using the factory with Config object
    llm_client = create_llm_client(config)

    # Test LLM client: generate text
    prompt = "利用Langchain 去实现AI agent的思路"
    print(f"Prompt: {prompt}")
    response = llm_client.generate_text(prompt, {})
    print(f"LLM Response:\n{response}")

    # You can add more tests or interactions here if needed

if __name__ == "__main__":
    main()
