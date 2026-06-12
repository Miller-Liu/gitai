import time

import pytest
from dotenv import load_dotenv

from src.agents.specialist import SpecialistAgent

load_dotenv()

DIVISIONS = [
    {"domain": "agents", "files": ["src/agents/base.py", "src/agents/orchestrator.py"], "rationale": "core agent classes"},
    {"domain": "graphs", "files": ["src/graphs/state.py", "src/graphs/graph.py"], "rationale": "graph wiring and state"}
]

@pytest.fixture(autouse=True)
def clear_registry():
    SpecialistAgent.clear_registry()
    yield
    SpecialistAgent.clear_registry()

@pytest.fixture
def specialists():
    s1 = SpecialistAgent(DIVISIONS, "agents", DIVISIONS[0]["files"], DIVISIONS[0]["rationale"])
    s2 = SpecialistAgent(DIVISIONS, "graphs", DIVISIONS[1]["files"], DIVISIONS[1]["rationale"])
    return s1, s2

def test_registry(specialists):
    s1, s2 = specialists
    assert SpecialistAgent.get("agents") is s1
    assert SpecialistAgent.get("graphs") is s2
    assert SpecialistAgent.get("nonexistent") is None

def test_understand_round1(specialists):
    s1, s2 = specialists
    time.sleep(2)
    s1.understand()
    assert s1.finding != ""
    assert s1.rounds == 1

def test_questions_routed(specialists):
    s1, s2 = specialists
    time.sleep(2)
    s1.understand()
    time.sleep(2)
    s2.understand()
    # questions in s2's pending should be addressed TO graphs (from agents)
    for q in s2.pending_questions:
        assert q["to"] == "graphs"
    # questions in s1's pending should be addressed TO agents (from graphs)
    for q in s1.pending_questions:
        assert q["to"] == "agents"

def test_answer_cycle(specialists):
    s1, s2 = specialists
    time.sleep(2)
    s1.understand()
    time.sleep(2)
    s2.understand()

    # only test answer cycle if questions were actually asked
    if s2.pending_questions:
        time.sleep(2)
        result = s2.answer()
        assert result is True
        # answer should have been deposited in the asker's answered_questions
        asker_domain = s2.answered_questions[-1]["to"] if s2.answered_questions else None
        if asker_domain:
            asker = SpecialistAgent.get(asker_domain)
            assert len(asker.answered_questions) > 0 # type: ignore

    if s1.pending_questions:
        time.sleep(2)
        result = s1.answer()
        assert result is True

def test_final_round(specialists):
    s1, s2 = specialists
    time.sleep(2)
    s1.understand()
    time.sleep(2)
    s2.understand()

    if s1.pending_questions:
        time.sleep(2)
        s1.answer()
    if s2.pending_questions:
        time.sleep(2)
        s2.answer()

    time.sleep(2)
    s1.understand(final=True)

    assert s1.satisfied is True
    assert s1.finding != ""
    assert s1.rounds == 2