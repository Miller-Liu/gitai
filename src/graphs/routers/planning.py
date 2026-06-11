from src.graphs.state import PlanningState

MAX_ITERATIONS = 3

def after_critic(state: PlanningState) -> str:
    if state["approved"] or state["iterations"] >= MAX_ITERATIONS:
        return "done"
    return "revise"