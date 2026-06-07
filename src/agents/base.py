from langchain.agents import create_agent

from src.config import load


class BaseAgent:
    system_prompt: str = ""
    tools: list = []

    def __init__(self, system_prompt: str = "", tools: list = []):
        cfg = load()
        provider = cfg.get("provider", "groq")
        model = cfg.get("model", "llama-3.1-8b-instant")

        _prompt = system_prompt if system_prompt is not None else self.system_prompt
        _tools = tools if tools is not None else self.tools

        self._agent = create_agent(
            f"{provider}:{model}",
            tools=_tools,
            system_prompt=_prompt
        )

    def run(self, task: str) -> str:
        result = self._agent.invoke({
            "messages": [{"role": "user", "content": task}]
        })
        return result["messages"][-1].content
    