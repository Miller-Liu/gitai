from typing import TypedDict


class PlanningState(TypedDict):
    file_tree: str
    proposal: dict
    verdict: dict
    iterations: int
    approved: bool

class ExecutionState(TypedDict):
    divisions: list[dict]
    findings: dict[str, str]       # domain → current finding
    questions: list[dict]          # [{"from": "auth", "to": "db", "question": "..."}]
    answers: list[dict]            # [{"from": "db", "to": "auth", "answer": "..."}]
    submitted: list[str]           # domains that are satisfied and done
    round: int                     # current round number
    max_rounds: int                # dynamic cap based on codebase size
    manager_verdict: dict
    feedback_type: str             # "none" | "replan" | "revise_domains"
    execution_approved: bool
    final_output: str
    domain: str                    # current domain being processed (for specialist node)
