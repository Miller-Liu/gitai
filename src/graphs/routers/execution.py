from src.graphs.state import ExecutionState


def after_specialist(state: ExecutionState) -> str:
    all_domains = [d["domain"] for d in state["divisions"]]
    done = state.get("done_this_phase", [])

    if len(done) < len(all_domains):
        return "pick_domain"
    
    return "next_phase"

def after_phase(state: ExecutionState) -> str:
    match state["phase"]:
        case "understand" | "answer" | "finalize":
            return "pick_domain"
        case "manager":
            return "manager"
        case _:
            return "pick_domain"