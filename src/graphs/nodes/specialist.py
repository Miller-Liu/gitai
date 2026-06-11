from src.agents.specialist import SpecialistAgent
from src.graphs.state import ExecutionState

_specialists: dict[str, SpecialistAgent] = {}

def get_specialist(domain: str, files: list[str], all_divisions: list[dict]) -> SpecialistAgent:
    if domain not in _specialists:
        _specialists[domain] = SpecialistAgent(
            domain=domain,
            files=files,
            all_divisions=all_divisions
        )
    return _specialists[domain]

def specialist_node(state: ExecutionState, domain: str) -> ExecutionState:
    division = next(
        (d for d in state["divisions"] if d["domain"] == domain),
        None
    )
    if not division:
        return state

    specialist = get_specialist(domain, division.get("files", []), state["divisions"])
    current_round = state.get("round", 1)

    if current_round == 1:
        result = specialist.start()
    else:
        my_questions = [q for q in state.get("questions", []) if q["to"] == domain]
        my_answers = [a for a in state.get("answers", []) if a["to"] == domain]
        peer_findings = "\n\n".join(
            f"[{d}]: {finding}"
            for d, finding in state.get("findings", {}).items()
            if d != domain
        ) or "No peer findings yet."

        result = specialist.repeat(
            previous_finding=state.get("findings", {}).get(domain, "None yet"),
            incoming_questions=my_questions,
            received_answers=my_answers,
            peer_findings=peer_findings
        )

    findings = {**state.get("findings", {}), domain: result.get("finding", "")}

    # keep only unanswered questions
    remaining_questions = [
        q for q in state.get("questions", [])
        if not (q["to"] == domain and any(
            a["to"] == q["from"] for a in result.get("answers", [])
        ))
    ]

    questions = remaining_questions + [
        {**q, "from": domain} for q in result.get("questions", [])
    ]

    answers = state.get("answers", []) + [
        {**a, "from": domain} for a in result.get("answers", [])
    ]
    submitted = state.get("submitted", [])
    if result.get("satisfied") and domain not in submitted:
        submitted = submitted + [domain]

    return {
        **state,
        "findings": findings,
        "questions": questions,
        "answers": answers,
        "submitted": submitted,
    }