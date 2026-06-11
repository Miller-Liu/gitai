import json
import re

from langchain.agents import create_agent

from src.config import load


class BaseAgent:
    def __init__(self, system_prompt: str = "", tools: list | None = None):
        cfg = load()
        provider = cfg.get("provider", "groq")
        model = cfg.get("model", "llama-3.1-8b-instant")

        self._agent = create_agent(
            f"{provider}:{model}",
            tools=tools or [],
            system_prompt=system_prompt
        )

    def run(self, task: str) -> str:
        result = self._agent.invoke({
            "messages": [{"role": "user", "content": task}]
        })
        return result["messages"][-1].content
    
    def _parse_json(self, text: str) -> dict:
        text = re.sub(r'```(?:json)?\n?', '', text).strip()
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return {}
    