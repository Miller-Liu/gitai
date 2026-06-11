from src.graphs.state import ExecutionState


def after_specialists(state: ExecutionState) -> str:
    all_domains = [d["domain"] for d in state.get("divisions", [])]
    submitted = state.get("submitted", [])
    current_round = state.get("round", 1)
    max_rounds = state.get("max_rounds", 3)

    if all(d in submitted for d in all_domains):
        return "manager"
    if current_round >= max_rounds:
        return "manager"
    return "next_round"

def after_manager(state: ExecutionState) -> str:
    match state.get("feedback_type", "none"):
        case "replan":
            return "replan"
        case "revise_domains":
            return "specialists"
        case _:
            return "synthesis"