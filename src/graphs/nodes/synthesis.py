from src.agents.synthesis import SynthesisAgent
from src.graphs.state import ExecutionState

_synthesis = SynthesisAgent()

def synthesis_node(state: ExecutionState) -> ExecutionState:
    """Dummy synthesis — just combines findings."""
    combined = "\n\n".join(
        f"## {domain}\n{finding}"
        for domain, finding in state.get("findings", {}).items()
    )
    return {
        **state,
        "final_output": combined or "No findings generated."
    }