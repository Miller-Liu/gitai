from src.agents.base import BaseAgent
from src.tools.filesystem import FILESYSTEM_TOOLS
from src.tools.prompts import SPECIALIST_PROMPT


class SpecialistAgent(BaseAgent):
    tools = FILESYSTEM_TOOLS

    def __init__(self, domain: str):
        self.domain = domain
        super().__init__(
            system_prompt=SPECIALIST_PROMPT,
            tools=FILESYSTEM_TOOLS
        )