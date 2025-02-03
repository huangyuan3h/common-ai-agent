# Common AI Agent

![architecture](./doc/image.png)

## Overview

Common AI Agent is an AI-powered assistant designed to process complex tasks by leveraging multiple components such as memory, context awareness, planning, and decomposition. It integrates various tools and interfaces to help with real-time actions, reflection, and refinement based on dynamic data. The agent can read files, perform searches, interface with code, and generate solutions through a structured problem-solving flow.

## environments

```
conda create --name common-ai-agent python=3.10

conda activate common-ai-agent
```

## Configuration

The project uses a YAML configuration file to manage settings. To get started:

1. Copy the template configuration file:

   ```bash
   cp config.yaml.template config.yaml
   ```

2. Edit `config.yaml` with your settings:
   ```yaml
   llm:
     client_type: ollama # Choose between 'ollama' or 'gemini'
     ollama:
       model_name: llama2
     gemini:
       model_name: gemini-pro
       api_key: "YOUR_API_KEY_HERE" # Required for Gemini
   ```

## overall developing plan

```
common_ai_agent/
│
├── core/                    # 核心功能
│   ├── memory/              # 处理长短期记忆（Long Term & Short Term Memory）
│   ├── context/             # 上下文管理，提供实时上下文数据
│   ├── tools/               # 工具集，处理外部任务如文件读取、搜索等
│   ├── agent/               # AI Agent 管理，负责与 LLM（语言模型）的交互
│   ├── planning/            # 任务规划与拆解
│   └── actions/             # 执行任务和行动
│
├── flow/                    # 控制聊天流程，负责调用各个模块
│   ├── chat_chain/          # 核心聊天链逻辑，管理输入输出
│   └── reflection/          # 反思与优化，处理任务执行后的反馈和调整
│
├── utils/                   # 工具类和通用代码
│   ├── logger.py            # 日志记录
│   └── helpers.py           # 通用辅助函数
│
├── config/                  # 配置文件
│   ├── config.yaml          # 环境和服务配置
│   └── settings.py          # 项目特定设置
│
├── tests/                   # 测试目录
│   ├── test_agent.py        # 测试 AI Agent 相关功能
│   ├── test_tools.py        # 测试工具集
│   └── test_memory.py       # 测试记忆模块
│
└── main.py                  # 启动脚本
```

    1.	core/
    •	memory/：处理短期和长期记忆的管理。你可以使用 ConversationBufferMemory 来处理短期记忆，长期记忆则可以采用数据库或文件存储。
    •	功能：提供存储、更新和读取记忆的接口。
    •	context/：提供当前的上下文数据，允许你为 AI 提供最新的会话背景信息。
    •	功能：管理对话的上下文信息，结合记忆进行实时更新。
    •	tools/：提供各种功能模块（如文件读取、搜索、代码接口等）。这些工具可以根据需要灵活组合。
    •	功能：集成外部资源或接口，以便用于执行任务。
    •	agent/：管理 AI Agent 的生命周期，处理与模型的交互。
    •	功能：配置与 LLM 交互的设置，处理任务的输入和输出。
    •	planning/：负责生成任务执行的计划，并拆解任务。
    •	功能：根据输入问题生成任务计划和子任务。
    •	actions/：执行计划中的具体任务。
    •	功能：执行任务，例如调用工具、执行代码等。
    2.	flow/
    •	chat_chain/：控制和管理聊天的核心流程。负责连接不同的模块，例如将用户输入传递给 Agent，获取响应，并进行适当的处理。
    •	功能：组合各个模块形成完整的 ChatChain，管理输入输出。
    •	reflection/：任务完成后的反思与优化，根据结果进行调整。可以结合模型的反馈来优化执行流程。
    •	功能：收集反馈，优化模型输出，改进系统性能。
    3.	utils/：
    •	logger.py：记录系统日志，便于调试和追踪。
    •	helpers.py：一些通用的辅助函数，如格式化、转换等。
    4.	config/：
    •	config.yaml：存储项目的全局配置，如 API 密钥、模型参数、环境配置等。
    •	settings.py：项目中其他细节设置的存储，比如是否开启调试模式、日志级别等。
    5.	tests/：
    •	test_agent.py：测试与 AI Agent 相关的功能，确保它能正确处理不同的输入和任务。
    •	test_tools.py：测试工具集的功能，确保如搜索、文件读取等工具的正确性。
    •	test_memory.py：测试记忆管理功能，确保记忆的读写操作正确。
    •	其他测试模块可以根据需要添加。
    6.	main.py：
    •	这是项目的启动脚本，可以加载配置并启动主服务。

## Components

1. **RAG (Retrieval-Augmented Generation)**:

   - Retrieves external knowledge or context to aid in decision-making or response generation.

2. **Memory**:
   - **Short Term Memory**: Stores temporary context for immediate tasks.
   - **Long Term Memory**: Retains more permanent data across sessions for deeper context understanding.
3. **AI Agent (LLM)**:

   - The core language model that processes tasks, interacts with tools, and generates actions.

4. **Tools**:

   - Tools like file readers and code interfaces are used to interact with data and external resources.

5. **Planning**:

   - Generates a plan to approach a task, including decomposition of subtasks into manageable actions.

6. **Actions**:

   - Executes tasks based on the agent's planning and inputs from the environment (e.g., read files, search the web, interact with code).

7. **Reflection and Refinement**:
   - After executing actions, the agent reflects on the outcome and refines its approach for improved efficiency and accuracy.

## Features

- **File Reading**: Read and process content from files to gather necessary data for task execution.
- **Search**: Perform web or local searches to gather additional context and resources.
- **Code Interface**: Interface with code repositories and systems for programming-related tasks.
- **Task Decomposition**: Break down larger tasks into smaller, manageable subtasks for efficient execution.
- **Contextual Awareness**: Utilize both short-term and long-term memory for enhanced decision-making.
- **Planning and Reflection**: Plan task execution and reflect on outcomes for optimization.
