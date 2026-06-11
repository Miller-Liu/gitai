from langgraph.constants import Send
from langgraph.graph import END, StateGraph

from src.graphs.nodes.critic import critic_node
from src.graphs.nodes.manager import manager_node
from src.graphs.nodes.orchestrator import orchestrator_node
from src.graphs.nodes.specialist import specialist_node
from src.graphs.nodes.synthesis import synthesis_node
from src.graphs.routers.execution import after_manager, after_specialists
from src.graphs.routers.planning import after_critic
from src.graphs.state import ExecutionState, PlanningState
from src.tools.filesystem import get_file_tree

MAX_ITERATIONS = 3

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

# ── execution graph ───────────────────────────────────────────────

def increment_round(state: ExecutionState) -> ExecutionState:
    return {**state, "round": state.get("round", 1) + 1}

def dispatch_specialists(state: ExecutionState):
    """Fan out — spawn one specialist node per division."""
    return [
        Send("specialist", {**state, "domain": d["domain"]})
        for d in state.get("divisions", [])
    ]

def build_execution_graph():
    graph = StateGraph(ExecutionState)

    graph.add_node("specialist", dispatch_specialists) # type: ignore
    graph.add_node("increment_round", increment_round)
    graph.add_node("manager", manager_node)
    graph.add_node("synthesis", synthesis_node)

    graph.set_entry_point("specialist")
    graph.add_conditional_edges(
        "specialist",
        after_specialists,
        {
            "manager": "manager",
            "next_round": "increment_round",
        }
    )
    graph.add_edge("increment_round", "specialist")
    graph.add_conditional_edges(
        "manager",
        after_manager,
        {
            "synthesis": "synthesis",
            "specialists": "specialist",
            "replan": END
        }
    )
    graph.add_edge("synthesis", END)

    return graph.compile()

# ── master runner ─────────────────────────────────────────────────

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

    # phase 2 — execution
    total_files = sum(len(d.get("files", [])) for d in divisions)
    max_rounds = max(3, total_files // 10)

    execution_graph = build_execution_graph()
    execution_result = execution_graph.invoke({
        "divisions": divisions,
        "findings": {},
        "questions": [],
        "answers": [],
        "submitted": [],
        "round": 1,
        "max_rounds": max_rounds,
        "manager_verdict": {},
        "feedback_type": "none",
        "execution_approved": False,
        "final_output": "",
        "domain": ""
    })

    return execution_result.get("final_output", "No output generated.")
