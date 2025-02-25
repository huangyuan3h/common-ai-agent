from typing import Dict, Any, Tuple, Callable
import httpx
import re
from bs4 import BeautifulSoup
from langchain_core.messages import AIMessage
from agent.models.state import AgentState, SubTask

def create_web_node(config: Dict) -> Tuple[str, Callable]:
    """创建网页访问节点"""
    
    async def fetch_url(url: str) -> Dict[str, Any]:
        """安全地获取URL内容"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 AI Research Agent"}
                )
                response.raise_for_status()
                
                # 解析HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 提取正文内容
                main_content = ""
                
                # 尝试找到主要内容区域
                main_tags = soup.find_all(['article', 'main', 'div'], class_=re.compile(r'content|main|article'))
                if main_tags:
                    main_content = main_tags[0].get_text(strip=True)
                else:
                    # 备选方案：获取所有段落
                    paragraphs = soup.find_all('p')
                    main_content = "\n".join([p.get_text(strip=True) for p in paragraphs])
                
                # 限制内容长度
                main_content = main_content[:5000] + "..." if len(main_content) > 5000 else main_content
                
                return {
                    "success": True,
                    "content": main_content,
                    "title": soup.title.string if soup.title else "无标题",
                    "url": response.url
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def _web_node(state: AgentState) -> Dict[str, Any]:
        """网页访问节点"""
        # 获取当前任务
        current_task_id = state["current_task_id"]
        if not current_task_id:
            return {
                "messages": [AIMessage(content="没有待执行的任务")]
            }
            
        # 查找当前任务
        current_task = next((t for t in state["tasks"] if t["id"] == current_task_id), None)
        if not current_task or current_task["type"] != "web":
            # 不是web任务，跳过
            return state
            
        # 更新任务状态
        tasks = list(state["tasks"])  # 创建副本
        for i, task in enumerate(tasks):
            if task["id"] == current_task_id:
                tasks[i] = {**task, "status": "running"}
        
        # 获取URL
        url = current_task["parameters"].get("url", "")
        if not url:
            result = "错误: 未提供URL参数"
            status = "failed"
        else:
            # 同步调用异步函数(简化处理)
            import asyncio
            result_data = asyncio.run(fetch_url(url))
            
            if result_data["success"]:
                result = f"成功从 {url} 获取内容:\n\n标题: {result_data['title']}\n\n{result_data['content']}"
                status = "completed"
            else:
                result = f"访问 {url} 失败: {result_data['error']}"
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
            "action": "web_access",
            "result_summary": f"{'成功' if status == 'completed' else '失败'}: {current_task['description']}"
        })
        
        return {
            "messages": [AIMessage(content=f"网页访问结果: {result}")],
            "tasks": tasks,
            "current_task_id": next_task_id,
            "execution_history": history
        }
    
    return "web_access", _web_node