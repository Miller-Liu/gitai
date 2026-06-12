import pytest
from dotenv import load_dotenv

from src.agents.specialist import SpecialistAgent
from src.graphs.nodes.specialist import next_phase_node, pick_domain_node, setup_node
from src.graphs.routers.execution import after_phase, after_specialist

load_dotenv()

DIVISIONS = [
    {"domain": "agents", "files": ["src/agents/base.py"], "rationale": "core agent classes"},
    {"domain": "graphs", "files": ["src/graphs/state.py"], "rationale": "graph state"}
]

BASE_STATE = {
    "divisions": DIVISIONS,
    "phase": "understand",
    "current_domain": "",
    "done_this_phase": [],
    "round": 1,
    "findings": {},
    "manager_verdict": {},
    "feedback_type": "none",
    "final_output": ""
}

@pytest.fixture(autouse=True)
def clear_registry():
    SpecialistAgent.clear_registry()
    yield
    SpecialistAgent.clear_registry()


# ── setup_node ────────────────────────────────────────────────────

def test_setup_creates_specialists():
    setup_node(BASE_STATE) # type: ignore
    assert SpecialistAgent.get("agents") is not None
    assert SpecialistAgent.get("graphs") is not None

def test_setup_initializes_state():
    result = setup_node(BASE_STATE) # type: ignore
    assert result["phase"] == "understand"
    assert result["round"] == 1
    assert result["done_this_phase"] == []
    assert result["findings"] == {}


# ── pick_domain_node ──────────────────────────────────────────────

def test_pick_first_domain():
    state = {**BASE_STATE}
    result = pick_domain_node(state) # type: ignore
    assert result["current_domain"] == "agents"

def test_pick_second_domain():
    state = {**BASE_STATE, "done_this_phase": ["agents"]}
    result = pick_domain_node(state) # type: ignore
    assert result["current_domain"] == "graphs"

def test_pick_no_change_when_all_done():
    state = {**BASE_STATE, "current_domain": "graphs", "done_this_phase": ["agents", "graphs"]}
    result = pick_domain_node(state) # type: ignore
    assert result["current_domain"] == "graphs"


# ── next_phase_node ───────────────────────────────────────────────

def test_understand_to_answer():
    state = {**BASE_STATE, "phase": "understand"}
    result = next_phase_node(state) # type: ignore
    assert result["phase"] == "answer"
    assert result["round"] == 1
    assert result["done_this_phase"] == []

def test_answer_to_understand():
    state = {**BASE_STATE, "phase": "answer", "round": 1}
    result = next_phase_node(state) # type: ignore
    assert result["phase"] == "understand"
    assert result["round"] == 2

def test_answer_to_finalize_at_max_rounds():
    state = {**BASE_STATE, "phase": "answer", "round": 3}
    result = next_phase_node(state) # type: ignore
    assert result["phase"] == "finalize"

def test_finalize_to_manager():
    state = {**BASE_STATE, "phase": "finalize"}
    result = next_phase_node(state) # type: ignore
    assert result["phase"] == "manager"

def test_round_resets_done_this_phase():
    state = {**BASE_STATE, "phase": "answer", "round": 1, "done_this_phase": ["agents", "graphs"]}
    result = next_phase_node(state) # type: ignore
    assert result["done_this_phase"] == []

def test_after_specialist_more_domains():
    state = {**BASE_STATE, "done_this_phase": ["agents"]}
    assert after_specialist(state) == "pick_domain" # type: ignore

def test_after_specialist_all_done():
    state = {**BASE_STATE, "done_this_phase": ["agents", "graphs"]}
    assert after_specialist(state) == "next_phase" # type: ignore

def test_after_phase_understand():
    state = {**BASE_STATE, "phase": "understand"}
    assert after_phase(state) == "pick_domain" # type: ignore

def test_after_phase_finalize():
    state = {**BASE_STATE, "phase": "finalize"}
    assert after_phase(state) == "manager" # type: ignore

def test_after_phase_manager_approved():
    state = {**BASE_STATE, "phase": "manager", "feedback_type": "none"}
    assert after_phase(state) == "synthesis" # type: ignore

def test_after_phase_manager_replan():
    state = {**BASE_STATE, "phase": "manager", "feedback_type": "replan"}
    assert after_phase(state) == "replan" # type: ignore
