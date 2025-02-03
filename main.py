from llm.llm_factory import create_llm_client

def main():
    # Ollama client configuration
    ollama_config = {
        "client_type": "ollama",
        "model_name": "deepseek-r1:14b"  # You can change the model name here if needed
    }

    # Create Ollama client using the factory
    ollama_client = create_llm_client(ollama_config)

    # Test Ollama client: generate text
    prompt = "请介绍一下 Langchain"
    print(f"Prompt: {prompt}")
    response = ollama_client.generate_text(prompt, {})
    print(f"Ollama Response:\n{response}")

    # You can add more tests or interactions here if needed

if __name__ == "__main__":
    main()
