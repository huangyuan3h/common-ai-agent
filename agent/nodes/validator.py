from typing import Dict, Any, Tuple, Callable, List
from langchain_core.messages import AIMessage, SystemMessage
from agent.models.state import AgentState
from llm.llm_factory import create_llm_client
from config import Config

VALIDATION_PROMPT = """你是一位任务验证专家。请评估以下任务执行结果是否成功，并提供简短分析：

任务描述: {task_description}
任务类型: {task_type}
执行结果: 
{task_result}

请判断任务是否成功执行，如果失败请说明原因并提供改进建议。
"""

def create_validator_node(config: Config) -> Tuple[str, Callable]:
    """创建结果验证节点"""
    llm_client = create_llm_client(config)
    
    def _validator_node(state: AgentState) -> Dict[str, Any]:
        # 获取当前任务
        current_task_id = state["current_task_id"]
        if not current_task_id:
            return state
            
        # 查找当前任务
        current_task = next((t for t in state["tasks"] if t["id"] == current_task_id), None)
        if not current_task:
            return state
            
        # 特殊处理日期相关任务 - 简化流程，不需要验证
        if current_task["type"] == "cli" and current_task["status"] == "completed":
            if "date" in current_task["parameters"].get("command", ""):
                # 更新执行历史
                history = list(state.get("execution_history", []))
                history.append({
                    "task_id": current_task_id,
                    "action": "validation",
                    "result_summary": "日期命令成功执行，无需验证"
                })
                
                # 直接跳到报告阶段
                return {
                    "working_memory": state.get("working_memory", {}),
                    "execution_history": history,
                    "current_task_id": None  # 直接完成所有任务
                }
        
        # 如果任务已完成或失败，则进行验证
        if current_task["status"] in ["completed", "failed"]:
            try:
                # 准备验证
                prompt = VALIDATION_PROMPT.format(
                    task_description=current_task["description"],
                    task_type=current_task["type"],
                    task_result=current_task["result"] or "无结果"
                )
                
                # 获取验证结果
                validation_result = llm_client.generate_text(prompt, {})
                
                # 更新工作内存
                working_memory = dict(state.get("working_memory", {}))
                if "validations" not in working_memory:
                    working_memory["validations"] = {}
                working_memory["validations"][current_task_id] = validation_result
                
                # 更新执行历史
                history = list(state.get("execution_history", []))
                history.append({
                    "task_id": current_task_id,
                    "action": "validation",
                    "result_summary": validation_result[:100] + "..." if len(validation_result) > 100 else validation_result
                })
                
                # 查找下一个任务
                next_task_id = None
                for task in state["tasks"]:
                    if task["status"] == "pending":
                        next_task_id = task["id"]
                        break
                
                # 如果没有下一个任务，则验证结束，不更新current_task_id
                if next_task_id:
                    return {
                        "working_memory": working_memory,
                        "execution_history": history,
                        "current_task_id": next_task_id
                    }
                else:
                    return {
                        "working_memory": working_memory,
                        "execution_history": history,
                        "current_task_id": None  # 表示所有任务已完成
                    }
            except Exception as e:
                # 如果验证出错，添加错误信息并继续执行
                history = list(state.get("execution_history", []))
                history.append({
                    "task_id": current_task_id,
                    "action": "validation_error",
                    "result_summary": f"验证过程中出错: {str(e)}"
                })
                
                # 继续下一个任务
                next_task_id = None
                for task in state["tasks"]:
                    if task["status"] == "pending":
                        next_task_id = task["id"]
                        break
                        
                return {
                    "execution_history": history,
                    "current_task_id": next_task_id if next_task_id else None
                }
        
        # 如果任务未完成，则不进行验证
        return state
    
    return "validator", _validator_node
