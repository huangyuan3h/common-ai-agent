from agent.graph_builder import build_chatbot_graph
from config import Config
from langchain_core.messages import HumanMessage

def main():
    # 初始化配置
    config = Config()
    
    # 构建流程图
    graph = build_chatbot_graph(config)
    
    # 测试流程
    test_state = {
        "messages": [HumanMessage(content="你好")]
    }
    print(graph.invoke(test_state))

if __name__ == "__main__":
    main()
