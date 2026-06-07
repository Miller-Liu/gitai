import tomllib
from pathlib import Path
from typing import Any

import tomli_w

CONFIG_PATH = Path.home() / ".gitai" / "config.toml"

DEFAULTS = {
    "provider": "ollama",
    "model": "llama3.2",
    "api_key": "",
}

def load() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return DEFAULTS.copy()
    with open(CONFIG_PATH, "rb") as f:
        return {**DEFAULTS, **tomllib.load(f)}

def save(updates: dict[str, Any]):
    CONFIG_PATH.parent.mkdir(exist_ok=True)
    config = load()
    config.update(updates)
    with open(CONFIG_PATH, "wb") as f:
        tomli_w.dump(config, f)