from langgraph.graph import StateGraph, START, END
from agent.models.state import AgentState
from agent.nodes.planner import create_planner_node
from agent.nodes.web import create_web_node
from agent.nodes.cli import create_cli_node
from agent.nodes.validator import create_validator_node
from agent.nodes.report import create_report_node
from config import Config

def build_agent_graph(config: Config) -> StateGraph:
    """构建智能Agent流程图"""
    builder = StateGraph(AgentState)
    
    # 创建所有节点
    planner_node = create_planner_node(config)
    web_node = create_web_node(config)
    cli_node = create_cli_node(config)
    validator_node = create_validator_node(config)
    report_node = create_report_node(config)
    
    # 添加所有节点到图中
    builder.add_node(*planner_node)
    builder.add_node(*web_node)
    builder.add_node(*cli_node)
    builder.add_node(*validator_node)
    builder.add_node(*report_node)
    
    # 节点路由逻辑：根据当前任务类型选择执行器
    def route_by_task_type(state: AgentState) -> str:
        # 如果没有当前任务，返回报告生成器
        if not state["current_task_id"]:
            return "report"
            
        # 获取当前任务
        current_task = next((t for t in state["tasks"] if t["id"] == state["current_task_id"]), None)
        if not current_task:
            return "report"
            
        # 根据任务类型路由
        task_type = current_task["type"]
        if task_type == "web":
            return "web_access"
        elif task_type == "cli":
            return "cli_command"
        elif task_type == "reflect":
            return "report"  # 反思任务直接交给报告生成器
        else:
            return "report"  # 未知任务类型，返回报告生成器
    
    # 设置图的起点为规划器
    builder.set_entry_point("planner")
    
    # 从规划器到执行器的路由
    builder.add_conditional_edges(
        "planner",
        route_by_task_type,
        {
            "web_access": "web_access",
            "cli_command": "cli_command",
            "report": "report"
        }
    )
    
    # 从执行器到验证器
    builder.add_edge("web_access", "validator")
    builder.add_edge("cli_command", "validator")
    
    # 从验证器到路由器或报告生成器
    builder.add_conditional_edges(
        "validator",
        route_by_task_type,
        {
            "web_access": "web_access",
            "cli_command": "cli_command",
            "report": "report"
        }
    )
    
    # 报告生成器为终点
    builder.add_edge("report", END)
    
    return builder.compile()

# 兼容旧代码，为了向后兼容
build_chatbot_graph = build_agent_graph

