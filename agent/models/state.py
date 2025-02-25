from typing import Annotated, List, Optional, Literal, Union, Dict
from typing_extensions import TypedDict
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph.message import add_messages

class SubTask(TypedDict):
    id: str                      # 任务唯一标识
    type: Literal["web", "cli", "code", "reflect"]
    description: str             # 任务描述
    parameters: Dict             # 任务参数
    result: Optional[str]        # 任务结果
    status: Literal["pending", "running", "completed", "failed"]

class AgentState(TypedDict):
    """完整的Agent状态模型"""
    messages: Annotated[List[Union[HumanMessage, AIMessage, SystemMessage]], add_messages]
    tasks: List[SubTask]          # 任务列表
    current_task_id: Optional[str]  # 当前执行的任务ID
    working_memory: Dict          # 临时工作内存
    execution_history: List[Dict]  # 执行历史记录