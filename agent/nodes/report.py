from typing import Dict, Any, Tuple, Callable, List
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from agent.models.state import AgentState
from llm.llm_factory import create_llm_client
from config import Config

REPORT_PROMPT = """你是一位专业的报告总结AI助手。请根据以下任务执行情况，生成一份全面的总结报告：

用户请求: {user_request}

任务执行情况:
{task_summary}

执行历史:
{execution_history}

请提供一份全面、专业的总结报告，包括：
1. 执行了哪些任务及其结果
2. 遇到的主要问题和解决方案
3. 从执行结果中获得的关键信息
4. 对用户原始请求的直接回答

请确保报告条理清晰、语言专业。
"""

def create_report_node(config: Config) -> Tuple[str, Callable]:
    """创建结果报告节点"""
    llm_client = create_llm_client(config)
    
    def _report_node(state: AgentState) -> Dict[str, Any]:
        # 检查是否所有任务都已完成
        all_completed = True
        for task in state["tasks"]:
            if task["status"] not in ["completed", "failed"]:
                all_completed = False
                break
                
        # 获取最后一条用户消息
        user_messages = [msg for msg in state["messages"] if isinstance(msg, HumanMessage)]
        user_request = user_messages[-1].content if user_messages else "未找到用户请求"
        
        # 简单任务的特殊处理：如果只有一个任务，直接返回结果
        if len(state["tasks"]) == 1 and state["tasks"][0]["status"] in ["completed", "failed"]:
            task = state["tasks"][0]
            if task["type"] == "cli" and "date" in task["parameters"].get("command", ""):
                return {
                    "messages": [AIMessage(content=f"当前日期和时间是:\n\n{task['result']}")],
                    "current_task_id": None  # 标记所有任务已完成
                }
        
        # 如果没有待执行的任务，生成报告
        if all_completed or (state["current_task_id"] is None and state["tasks"]):
            # 生成任务摘要
            task_summary = ""
            for i, task in enumerate(state["tasks"]):
                status_emoji = "✅" if task["status"] == "completed" else "❌"
                result_preview = task.get("result", "无结果")
                if result_preview and len(result_preview) > 100:
                    result_preview = result_preview[:100] + "..."
                    
                task_summary += f"{i+1}. {status_emoji} {task['description']} ({task['type']})\n"
                task_summary += f"   结果: {result_preview}\n\n"
            
            # 生成执行历史摘要
            execution_history = ""
            for i, entry in enumerate(state["execution_history"]):
                execution_history += f"{i+1}. {entry['action']}: {entry['result_summary']}\n"
            
            # 生成报告
            prompt = REPORT_PROMPT.format(
                user_request=user_request,
                task_summary=task_summary,
                execution_history=execution_history
            )
            
            report = llm_client.generate_text(prompt, {})
            
            return {
                "messages": [AIMessage(content=report)],
                "current_task_id": None  # 标记所有任务已完成
            }
        
        # 如果还有任务待执行，不生成报告
        return state
    
    return "report", _report_node
