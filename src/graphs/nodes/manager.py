from src.agents.manager import ManagerAgent
from src.graphs.state import ExecutionState

_manager = ManagerAgent()

def manager_node(state: ExecutionState) -> ExecutionState:
    verdict = _manager.validate(
        findings=state.get("findings", {}),
        questions=state.get("questions", []),
        answers=state.get("answers", []),
        divisions=state.get("divisions", [])
    )

    return {
        **state,
        "manager_verdict": verdict,
        "feedback_type": verdict.get("feedback_type", "none"),
        "execution_approved": verdict.get("execution_approved", False),
    }