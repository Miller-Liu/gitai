from src.agents.synthesis import SynthesisAgent
from src.graphs.state import ExecutionState

_synthesis = SynthesisAgent()

def synthesis_node(state: ExecutionState) -> ExecutionState:
    result = _synthesis.synthesize(state.get("findings", {}))
    return {
        **state,
        "final_output": result
    }