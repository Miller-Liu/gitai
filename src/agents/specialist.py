import json

from src.agents.base import BaseAgent
from src.prompts import SPECIALIST_PROMPT, SPECIALIST_REPEAT, SPECIALIST_START
from src.tools.filesystem import FILESYSTEM_TOOLS


class SpecialistAgent(BaseAgent):
    def __init__(self, domain: str, files: list[str], all_divisions: list[dict]):
        self.domain = domain
        self.files = files
        self.all_divisions = all_divisions
        super().__init__(
            system_prompt=SPECIALIST_PROMPT.format(
                domain=domain,
                all_domains="\n".join(
                    f"- {d['domain']}: {d['rationale']}"
                    for d in all_divisions
                    if d['domain'] != domain
                )
            ),
            tools=FILESYSTEM_TOOLS
        )

    def start(self) -> dict:
        result = self.run(
            SPECIALIST_START.format(
                domain=self.domain,
                files=self.files
            )
        )
        parsed = self._parse_json(result)
        return {"finding": "", "questions": [], **parsed}

    def repeat(
        self,
        previous_finding: str,
        incoming_questions: list[dict],
        received_answers: list[dict],
        peer_findings: str
    ) -> dict:
        result = self.run(
            SPECIALIST_REPEAT.format(
                domain=self.domain,
                previous_finding=previous_finding,
                incoming_questions=json.dumps(incoming_questions, indent=2) if incoming_questions else "None",
                received_answers=json.dumps(received_answers, indent=2) if received_answers else "None",
                peer_findings=peer_findings
            )
        )
        parsed = self._parse_json(result)
        return {"finding": "", "questions": [], "answers": [], "satisfied": False, **parsed}  # add defaults
