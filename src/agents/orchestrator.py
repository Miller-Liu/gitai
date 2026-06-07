from langchain.tools import tool

from src.agents.base import BaseAgent
from src.tools.filesystem import FILESYSTEM_TOOLS
from src.tools.prompts import ORCHESTRATOR_PROMPT

_findings: dict[str, str] = {}

def _make_spawn_tool():
    @tool
    def spawn_specialist(domain: str, description: str) -> str:
        """Spawn a specialist agent to analyze a specific module or domain.
        
        Args:
            domain: Short name for the domain e.g. 'auth', 'api', 'frontend'
            description: What files or concerns this specialist should focus on
        """
        from src.agents.specialist import SpecialistAgent
        specialist = SpecialistAgent(domain=domain)
        result = specialist.run(
            f"Analyze the '{domain}' module. Focus on: {description}"
        )
        _findings[domain] = result
        return f"Specialist '{domain}' completed."
    return spawn_specialist

@tool
def get_findings() -> str:
    """Get all findings collected from specialists so far."""
    if not _findings:
        return "No specialists have reported yet."
    return "\n\n---\n\n".join(
        f"## {domain}\n{finding}" 
        for domain, finding in _findings.items()
    )

class OrchestratorAgent(BaseAgent):
    system_prompt = ORCHESTRATOR_PROMPT

    def __init__(self):
        spawn_tool = _make_spawn_tool()
        super().__init__(
            system_prompt=self.system_prompt,
            tools=FILESYSTEM_TOOLS + [spawn_tool, get_findings]
        )