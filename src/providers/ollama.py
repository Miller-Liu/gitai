import ollama

from src.providers.base import Provider, ProviderDef

OLLAMA_DEF = ProviderDef(
    name="ollama",
    display_name="Ollama (local)",
    default_model="llama3.2",
    requires_api_key=False,
    is_local=True,
)

class OllamaProvider(Provider):
    def chat(self, system: str, user: str) -> str:
        response = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ]
        )
        return response["message"]["content"]