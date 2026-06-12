from src.agents.manager import ManagerAgent
from src.graphs.state import ExecutionState

_manager = ManagerAgent()

def manager_node(state: ExecutionState) -> ExecutionState:
    """Dummy manager — always approves."""
    return {
        **state,
        "phase": "manager",
        "manager_verdict": {"approved": True},
        "feedback_type": "none",
    }