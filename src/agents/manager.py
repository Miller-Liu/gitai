import json

from src.agents.base import BaseAgent
from src.prompts import MANAGER_PROMPT
from src.tools.filesystem import FILESYSTEM_TOOLS


class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=MANAGER_PROMPT,
            tools=FILESYSTEM_TOOLS
        )

    def validate(
        self,
        findings: dict[str, str],
        questions: list[dict],
        answers: list[dict],
        divisions: list[dict]
    ) -> dict:
        context = (
            f"Specialist findings:\n{json.dumps(findings, indent=2)}\n\n"
            f"Questions asked between specialists:\n{json.dumps(questions, indent=2)}\n\n"
            f"Answers given:\n{json.dumps(answers, indent=2)}\n\n"
            f"Original divisions:\n{json.dumps(divisions, indent=2)}"
        )
        result = self.run(
            f"Validate these specialist findings against the actual codebase.\n\n{context}"
        )
        parsed = self._parse_json(result)
        return {
            "execution_approved": False,
            "feedback_type": "none",
            "issues": [],
            "domain_revisions": {},
            **parsed
        }