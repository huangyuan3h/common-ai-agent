from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
    """对话状态模型"""
    messages: Annotated[
        list[HumanMessage | AIMessage],  # 使用 LangChain 消息类型
        add_messages
    ]