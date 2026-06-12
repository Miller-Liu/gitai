from langgraph.graph import END, StateGraph

from src.graphs.nodes.critic import critic_node
from src.graphs.nodes.manager import manager_node
from src.graphs.nodes.orchestrator import orchestrator_node
from src.graphs.nodes.specialist import (
    next_phase_node,
    pick_domain_node,
    setup_node,
    specialist_node,
)
from src.graphs.nodes.synthesis import synthesis_node
from src.graphs.routers.execution import after_phase, after_specialist
from src.graphs.routers.planning import after_critic
from src.graphs.state import ExecutionState, PlanningState
from src.tools.filesystem import get_file_tree

# ── planning graph ────────────────────────────────────────────────

def build_planning_graph():
    graph = StateGraph(PlanningState)

    graph.add_node("orchestrator", orchestrator_node)
    graph.add_node("critic", critic_node)

    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", "critic")
    graph.add_conditional_edges(
        "critic",
        after_critic,
        {"revise": "orchestrator", "done": END}
    )

    return graph.compile()

def build_execution_graph():
    graph = StateGraph(ExecutionState)

    graph.add_node("setup", setup_node)
    graph.add_node("pick_domain", pick_domain_node)
    graph.add_node("specialist", specialist_node)
    graph.add_node("next_phase", next_phase_node)
    graph.add_node("manager", manager_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("setup")
    graph.add_edge("setup", "pick_domain")
    graph.add_conditional_edges(
        "pick_domain",
        lambda state: "specialist",
        {"specialist": "specialist"}
    )
    graph.add_conditional_edges(
        "specialist",
        after_specialist,
        {
            "pick_domain": "pick_domain",
            "next_phase": "next_phase"
        }
    )
    graph.add_conditional_edges(
        "next_phase",
        after_phase,
        {
            "pick_domain": "pick_domain",
            "manager": "manager",
        }
    )
    graph.add_conditional_edges(
        "manager",
        after_phase,
        {
            "synthesis": "synthesis",
            "replan": END,
            "pick_domain": "pick_domain",
        }
    )
    graph.add_edge("synthesis", END)

    return graph.compile()

def run_explain() -> str:
    # phase 1 — planning
    planning_graph = build_planning_graph()
    planning_result = planning_graph.invoke({
        "file_tree": get_file_tree(),
        "proposal": {},
        "verdict": {},
        "iterations": 0,
        "approved": False
    })

    divisions = planning_result["proposal"].get("divisions", [])
    if not divisions:
        return "Could not determine codebase structure."
    
    print(divisions) # for debugging

    # phase 2 — execution
    execution_graph = build_execution_graph()
    execution_result = execution_graph.invoke({
        "divisions": divisions,
        "phase": "",
        "current_domain": "",
        "done_this_phase": [],
        "round": 0,
        "findings": {},
        "manager_verdict": {},
        "feedback_type": "none",
        "final_output": ""
    })

    return execution_result.get("final_output", "No output generated.")
