import json

from src.agents.base import BaseAgent
from src.prompts import ORCHESTRATOR_PROMPT
from src.tools.filesystem import FILESYSTEM_TOOLS


class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=ORCHESTRATOR_PROMPT,
            tools=FILESYSTEM_TOOLS
        )

    def propose_divisions(self, file_tree: str) -> dict:
        result = self.run(
            f"Analyze this file tree and propose module divisions.\n\n"
            f"File tree:\n{file_tree}"
        )
        parsed = self._parse_json(result)
        return {"divisions": [], **parsed}

    def revise_divisions(self, proposal: dict, issues: list[str]) -> dict:
        result = self.run(
            f"Revise these module divisions based on specialist feedback.\n\n"
            f"Current divisions:\n{json.dumps(proposal, indent=2)}\n\n"
            f"Feedback:\n" + "\n".join(f"- {issue}" for issue in issues)
        )
        parsed = self._parse_json(result)
        return {"divisions": [], **parsed}