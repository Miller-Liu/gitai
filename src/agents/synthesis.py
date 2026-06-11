from src.agents.base import BaseAgent
from src.prompts import SYNTHESIS_PROMPT


class SynthesisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            system_prompt=SYNTHESIS_PROMPT,
            tools=[]
        )

    def synthesize(self, findings: dict[str, str]) -> str:
        formatted = "\n\n---\n\n".join(
            f"## {domain}\n{finding}"
            for domain, finding in findings.items()
        )
        return self.run(
            f"Synthesize these specialist findings into a "
            f"comprehensive explanation:\n\n{formatted}"
        )