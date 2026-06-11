from src.agents.base import BaseAgent
from src.prompts import CRITIC_PROMPT
from src.tools.filesystem import FILESYSTEM_TOOLS


class CriticAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=CRITIC_PROMPT,
            tools=FILESYSTEM_TOOLS
        )

    def evaluate(self, proposal: dict) -> dict:
        result = self.run(
            f"Evaluate these proposed module divisions and return JSON verdict:\n{proposal}"
        )
        parsed = self._parse_json(result)
        return {"approved": True, "issues": [], **parsed}