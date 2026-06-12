from typing import TypedDict


class PlanningState(TypedDict):
    file_tree: str
    proposal: dict
    verdict: dict
    iterations: int
    approved: bool

class ExecutionState(TypedDict):
    divisions: list[dict]
    phase: str              # "understand" | "answer" | "finalize" | "check"
    current_domain: str
    done_this_phase: list[str]
    round: int
    findings: dict[str, str]   # only populated in finalize