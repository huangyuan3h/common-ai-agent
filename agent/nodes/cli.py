from typing import Dict, Any, Tuple, Callable, List
import subprocess
import shlex
from pathlib import Path
from langchain_core.messages import AIMessage
from agent.models.state import AgentState

def create_cli_node(config: Dict) -> Tuple[str, Callable]:
    """创建命令行执行节点"""
    
    # 安全命令白名单
    default_safe_commands = [
        "ls", "pwd", "echo", "cat", "find",
        "python --version", "python3 --version",
        "date", "whoami", "hostname"
    ]
    SAFE_COMMANDS = config.get_config("agent.cli.safe_commands") or default_safe_commands
    
    def is_command_safe(command: str) -> bool:
        """检查命令是否安全"""
        cmd = shlex.split(command)[0] if command else ""
        
        # 检查完整命令是否在白名单中
        if command in SAFE_COMMANDS:
            return True
            
        # 检查命令前缀是否在白名单中
        for safe_cmd in SAFE_COMMANDS:
            if command.startswith(safe_cmd):
                return True
                
        # 检查基础命令是否在白名单中
        return cmd in [shlex.split(c)[0] for c in SAFE_COMMANDS]
    
    def run_safe_command(command: str, timeout=30) -> Dict[str, Any]:
        """安全地执行命令"""
        try:
            if not is_command_safe(command):
                return {
                    "success": False,
                    "error": f"安全限制: 命令 '{command}' 不在允许列表中"
                }
                
            # 使用shlex分割命令以处理引号和空格
            cmd_parts = shlex.split(command)
            
            result = subprocess.run(
                cmd_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout,
                cwd=Path.home(),  # 在用户目录执行
                text=True,        # 返回字符串而非字节
                shell=False       # 禁用shell执行提高安全性
            )
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def _cli_node(state: AgentState) -> Dict[str, Any]:
        """命令行执行节点"""
        # 获取当前任务
        current_task_id = state["current_task_id"]
        if not current_task_id:
            return {
                "messages": [AIMessage(content="没有待执行的命令行任务")]
            }
            
        # 查找当前任务
        current_task = next((t for t in state["tasks"] if t["id"] == current_task_id), None)
        if not current_task or current_task["type"] != "cli":
            # 不是CLI任务，跳过
            return state
            
        # 更新任务状态
        tasks = list(state["tasks"])  # 创建副本
        for i, task in enumerate(tasks):
            if task["id"] == current_task_id:
                tasks[i] = {**task, "status": "running"}
        
        # 获取命令
        command = current_task["parameters"].get("command", "")
        if not command:
            result = "错误: 未提供命令参数"
            status = "failed"
        else:
            # 执行命令
            result_data = run_safe_command(command)
            
            if result_data["success"]:
                result = f"命令 '{command}' 执行成功:\n\n{result_data['output']}"
                status = "completed"
            else:
                result = f"命令 '{command}' 执行失败: {result_data['error']}"
                status = "failed"
        
        # 更新任务结果
        for i, task in enumerate(tasks):
            if task["id"] == current_task_id:
                tasks[i] = {**task, "result": result, "status": status}
        
        # 查找下一个任务
        next_task_id = None
        for task in tasks:
            if task["status"] == "pending":
                next_task_id = task["id"]
                break
        
        # 更新执行历史
        history = list(state["execution_history"])
        history.append({
            "task_id": current_task_id,
            "action": "cli_execution",
            "result_summary": f"{'成功' if status == 'completed' else '失败'}: {current_task['description']}"
        })
        
        return {
            "messages": [AIMessage(content=f"命令行执行结果: {result}")],
            "tasks": tasks,
            "current_task_id": next_task_id,
            "execution_history": history
        }
    
    return "cli_command", _cli_node