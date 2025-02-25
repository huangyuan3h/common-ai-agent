from typing import Callable
from langchain_core.messages import AIMessage, HumanMessage
from agent.models.state import AgentState
from llm.llm_factory import create_llm_client
from config import Config

def create_chatbot_node(config: Config) -> tuple[str, Callable]:
    """创建对话节点（返回节点名称和函数）"""
    llm_client = create_llm_client(config)
    
    def _chatbot_node(state: AgentState):
        # 查找最后一条人类消息
        last_human_msg = next(
            (msg for msg in reversed(state["messages"]) 
             if isinstance(msg, HumanMessage)),
            None
        )
        prompt = last_human_msg.content if last_human_msg else ""
        
        # 生成回复
        response = llm_client.generate_text(prompt, {})
        return {"messages": [AIMessage(content=response)]}
    
    return "chatbot", _chatbot_node  # 简化为返回元组
