from agent.graph_builder import build_agent_graph
from config import Config
from langchain_core.messages import HumanMessage

def main():
    # 初始化配置
    config = Config()
    
    # 构建智能Agent流程图
    graph = build_agent_graph(config)
    
    # 交互式测试
    print("智能Agent已启动，请输入您的请求（输入'退出'结束）")
    while True:
        user_input = input("\n用户: ")
        if user_input.lower() in ["退出", "exit", "quit"]:
            break
            
        # 准备初始状态
        initial_state = {
            "messages": [HumanMessage(content=user_input)],
            "tasks": [],
            "current_task_id": None,
            "working_memory": {},
            "execution_history": []
        }
        
        # 执行流程图
        try:
            result = graph.invoke(initial_state)
            
            # 打印AI回复
            if "messages" in result and result["messages"]:
                ai_messages = [msg for msg in result["messages"] if hasattr(msg, "type") and msg.type == "ai"]
                if ai_messages:
                    for msg in ai_messages:
                        print(f"\nAI: {msg.content}")
                else:
                    print("\nAI: 没有生成回复。")
            else:
                print("\nAI: 处理完成，但没有生成回复。")
        except Exception as e:
            print(f"执行过程中发生错误: {e}")

if __name__ == "__main__":
    main()
