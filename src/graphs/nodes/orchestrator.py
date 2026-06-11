from src.agents.orchestrator import OrchestratorAgent
from src.graphs.state import PlanningState

_orchestrator = OrchestratorAgent()

def orchestrator_node(state: PlanningState) -> PlanningState:
    if state["iterations"] == 0:
        proposal = _orchestrator.propose_divisions(state["file_tree"])
    else:
        proposal = _orchestrator.revise_divisions(
            proposal=state["proposal"],
            issues=state["verdict"].get("issues", [])
        )

    return {
        **state,
        "proposal": proposal,
        "iterations": state["iterations"] + 1
    }