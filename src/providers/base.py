from dataclasses import dataclass
from typing import Optional

@dataclass
class ProviderDef:
    name: str
    display_name: str
    default_model: str
    requires_api_key: bool
    is_local: bool = False

class Provider:
    def __init__(self, definition: ProviderDef, model: str, api_key: Optional[str] = None):
        self.definition = definition
        self.model = model
        self.api_key = api_key

    def chat(self, system: str, user: str) -> str:
        raise NotImplementedError

    def validate(self) -> list[str]:
        errors = []
        if self.definition.requires_api_key and not self.api_key:
            errors.append(f"{self.definition.display_name} requires an API key. Run `gitai setup`.")
        return errors