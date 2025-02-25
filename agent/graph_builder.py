from langgraph.graph import StateGraph, START, END
from agent.models.state import ChatState
from agent.nodes.chatbot_node import create_chatbot_node
from config import Config

def build_chatbot_graph(config: Config) -> StateGraph:
    """构建对话流程图"""
    builder = StateGraph(ChatState)
    
    # 创建并添加节点
    node_name, node_func = create_chatbot_node(config)
    builder.add_node(node_name, node_func)
    
    # 设置简单线性流程
    builder.set_entry_point(node_name)
    builder.set_finish_point(node_name)
    
    return builder.compile()
