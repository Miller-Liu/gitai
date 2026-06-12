from src.agents.specialist import SpecialistAgent
from src.graphs.state import ExecutionState

MAX_ROUNDS = 3

def setup_node(state: ExecutionState) -> ExecutionState:
    """Create all specialists from divisions."""
    SpecialistAgent.clear_registry()

    for d in state["divisions"]:
        SpecialistAgent(
            all_divisions=state["divisions"],
            domain=d["domain"],
            files=d["files"],
            rationale=d.get("rationale", "")
        )

    return {
        **state,
        "phase": "understand",
        "current_domain": "",
        "done_this_phase": [],
        "round": 1,
        "findings": {},
    }

def pick_domain_node(state: ExecutionState) -> ExecutionState:
    all_domains = [d["domain"] for d in state["divisions"]]
    done = state.get("done_this_phase", [])

    for domain in all_domains:
        if domain not in done:
            return {**state, "current_domain": domain}

    return state

def next_phase_node(state: ExecutionState) -> ExecutionState:
    current_phase = state["phase"]
    current_round = state["round"]
    all_domains = [d["domain"] for d in state["divisions"]]

    match current_phase:
        case "understand":
            # after understand, always go to answer
            new_phase = "answer"
            new_round = current_round

        case "answer":
            # check if any specialist still has pending questions
            any_pending = any(
                len(SpecialistAgent.get(d).pending_questions) > 0 # type: ignore
                for d in all_domains
                if SpecialistAgent.get(d)
            )
            if any_pending:
                # another answer cycle
                new_phase = "answer"
                new_round = current_round
            elif current_round >= MAX_ROUNDS:
                # hit max rounds, finalize
                new_phase = "finalize"
                new_round = current_round
            else:
                # back to understand
                new_phase = "understand"
                new_round = current_round + 1

        case "finalize":
            # after finalize, snapshot findings and go to manager
            new_phase = "manager"
            new_round = current_round

        case _:
            new_phase = current_phase
            new_round = current_round

    return {
        **state,
        "phase": new_phase,
        "round": new_round,
        "done_this_phase": [],
    }

def specialist_node(state: ExecutionState) -> ExecutionState:
    domain = state["current_domain"]
    specialist = SpecialistAgent.get(domain)

    if not specialist:
        return state

    match state["phase"]:
        case "understand":
            specialist.understand()
        case "answer":
            specialist.answer()
        case "finalize":
            specialist.understand(final=True)

    done_this_phase = state.get("done_this_phase", []) + [domain]

    return {
        **state,
        "done_this_phase": done_this_phase,
    }