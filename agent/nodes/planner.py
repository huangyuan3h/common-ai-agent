from typing import Dict, List, Any, Tuple, Callable
from uuid import uuid4
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from agent.models.state import AgentState, SubTask
from llm.llm_factory import create_llm_client
from config import Config

PLANNER_PROMPT = """你是一位专业的任务规划AI助手。请将用户的需求分解为一系列可执行的子任务。

用户需求: {user_request}

可用的任务类型:
- web: 网页访问和信息获取
- cli: 执行命令行操作
- code: 生成或执行代码
- reflect: 思考和总结已有信息

请以JSON格式返回任务列表，每个任务包含:
- type: 任务类型
- description: 任务描述
- parameters: 相关参数(URL、命令等)

示例响应:
```json
[
  {
    "type": "web",
    "description": "查询天气信息",
    "parameters": {"url": "https://weather.example.com/beijing"}
  },
  {
    "type": "cli",
    "description": "创建存储目录",
    "parameters": {"command": "mkdir -p ~/weather_data"}
  }
]
```

请分析用户需求并返回合适的任务计划:
"""

def create_planner_node(config: Config) -> Tuple[str, Callable]:
    """创建任务规划节点"""
    llm_client = create_llm_client(config)
    
    def _planner_node(state: AgentState) -> Dict[str, Any]:
        # 获取最后一条用户消息
        user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
        if not user_messages:
            return {
                "messages": [AIMessage(content="请先输入您的请求")]
            }
        
        user_request = user_messages[-1].content
        
        # 针对特殊请求自动创建任务
        if "日期" in user_request.lower() or "时间" in user_request.lower():
            # 直接创建获取日期/时间的任务
            tasks = [
                SubTask(
                    id=str(uuid4())[:8],
                    type="cli",
                    description="获取当前日期和时间",
                    parameters={"command": "date"},
                    result=None,
                    status="pending"
                )
            ]
            plan_summary = "我将为您获取当前日期和时间。"
            return {
                "messages": [AIMessage(content=plan_summary)],
                "tasks": tasks,
                "current_task_id": tasks[0]["id"],
                "working_memory": {},
                "execution_history": []
            }
        
        # 生成任务计划
        prompt = PLANNER_PROMPT.format(user_request=user_request)
        response = llm_client.generate_text(prompt, {})
        
        # 尝试解析JSON
        try:
            import json
            import re
            
            # 提取JSON部分
            json_match = re.search(r'```json\s*([\s\S]*?)\s*```', response)
            if json_match:
                tasks_json = json_match.group(1)
            else:
                # 尝试找到方括号包围的JSON数组
                json_array_match = re.search(r'\[\s*{.*}\s*\]', response, re.DOTALL)
                if json_array_match:
                    tasks_json = json_array_match.group(0)
                else:
                    # 如果没有找到明确的JSON，直接创建一个默认任务
                    fallback_task = SubTask(
                        id=str(uuid4())[:8],
                        type="reflect",
                        description=f"分析用户请求: {user_request}",
                        parameters={},
                        result=None,
                        status="pending"
                    )
                    return {
                        "messages": [AIMessage(content=f"我将分析您的请求: {user_request}")],
                        "tasks": [fallback_task],
                        "current_task_id": fallback_task["id"],
                        "working_memory": {},
                        "execution_history": []
                    }
                
            # 清理JSON字符串中可能的格式问题
            tasks_json = tasks_json.strip()
            tasks_json = re.sub(r',\s*}', '}', tasks_json)  # 移除对象末尾多余的逗号
            tasks_json = re.sub(r',\s*]', ']', tasks_json)  # 移除数组末尾多余的逗号
                
            tasks_data = json.loads(tasks_json)
            
            # 添加任务ID和状态
            tasks = []
            for task_data in tasks_data:
                task = SubTask(
                    id=str(uuid4())[:8],
                    type=task_data["type"],
                    description=task_data["description"],
                    parameters=task_data.get("parameters", {}),
                    result=None,
                    status="pending"
                )
                tasks.append(task)
            
            # 创建计划总结消息
            plan_summary = f"我已将您的请求分解为{len(tasks)}个子任务:\n\n"
            for i, task in enumerate(tasks):
                plan_summary += f"{i+1}. {task['description']} ({task['type']})\n"
            
            return {
                "messages": [AIMessage(content=plan_summary)],
                "tasks": tasks,
                "current_task_id": tasks[0]["id"] if tasks else None,
                "working_memory": {},
                "execution_history": []
            }
            
        except Exception as e:
            # 创建一个后备任务
            fallback_task = SubTask(
                id=str(uuid4())[:8],
                type="cli",
                description="获取基本信息",
                parameters={"command": "date && pwd && whoami"},
                result=None,
                status="pending"
            )
            
            return {
                "messages": [AIMessage(content=f"我将执行一个基本的信息获取任务。")],
                "tasks": [fallback_task],
                "current_task_id": fallback_task["id"],
                "working_memory": {},
                "execution_history": []
            }
    
    return "planner", _planner_node
