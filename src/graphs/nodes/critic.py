from src.agents.critic import CriticAgent
from src.graphs.state import PlanningState

_critic = CriticAgent()

def critic_node(state: PlanningState) -> PlanningState:
    verdict = _critic.evaluate(state["proposal"])
    return {
        **state,
        "verdict": verdict,
        "approved": verdict.get("approved", True)
    }