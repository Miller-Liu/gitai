import json

from src.agents.base import BaseAgent
from src.prompts import (
    SPECIALIST_ANSWER,
    SPECIALIST_FINAL,
    SPECIALIST_PROMPT,
    SPECIALIST_START,
)
from src.tools.filesystem import FILESYSTEM_TOOLS


class SpecialistAgent(BaseAgent):
    _registry: dict[str, "SpecialistAgent"] = {}

    def __init__(self,  all_divisions: list[dict], domain: str, files: list[str], rationale: str = ""):
        self.domain = domain
        self.files = files
        self.rationale = rationale
        self.finding: str = ""
        self.rounds: int = 0
        self.pending_questions: list[dict] = []
        self.answered_questions: list[dict] = []

        SpecialistAgent._registry[domain] = self

        super().__init__(
            system_prompt=SPECIALIST_PROMPT.format(
                domain=domain,
                all_domains="\n".join(
                    f"- {d['domain']}: {d['rationale']}"
                    for d in all_divisions
                    if d["domain"] != domain
                )
            ),
            tools=FILESYSTEM_TOOLS
        )

    @classmethod
    def get(cls, domain: str) -> "SpecialistAgent | None":
        return cls._registry.get(domain)

    @classmethod
    def clear_registry(cls):
        """Call this before each new explain run."""
        cls._registry.clear()

    def understand(self, final: bool = False) -> str:
        if not final:
            task = SPECIALIST_START.format(
                domain=self.domain,
                files=self.files
            )
        else:
            task = SPECIALIST_FINAL.format(
                domain=self.domain,
                current_finding=self.finding,
                answered_questions=json.dumps(
                    self.answered_questions, indent=2
                ) if self.answered_questions else "None"
            )

        result = self.run(task)
        parsed = self._parse_json(result)

        if parsed.get("finding"):
            self.finding = parsed["finding"]

        self.rounds += 1

        valid_domains = set(SpecialistAgent._registry.keys()) - {self.domain}
        raw_questions = parsed.get("questions", [])

        valid_questions = [
            {"to": q["to"], "question": q["question"], "from": self.domain}
            for q in raw_questions
            if isinstance(q, dict)
            and q.get("to") in valid_domains
            and q.get("question")
        ]

        for q in valid_questions:
            SpecialistAgent._registry[q["to"]].pending_questions.append(q)
        
        return self.finding
    
    def answer(self) -> bool:
        """Answer the next pending question. Returns True if answered, False if nothing pending."""
        if not self.pending_questions:
            return False

        question = self.pending_questions.pop(0)

        task = SPECIALIST_ANSWER.format(
            domain=self.domain,
            question=question.get("question", ""),
            asker=question.get("from", "unknown"),
            finding=self.finding
        )

        result = self.run(task)
        parsed = self._parse_json(result)

        answer = {
            "to": question.get("from"),
            "from": self.domain,
            "question": question.get("question"),
            "answer": parsed.get("answer", result)
        }

        asker = SpecialistAgent.get(question.get("from", ""))
        if asker:
            asker.answered_questions.append(answer)

        return True