import pytest

from src.providers.ollama import OLLAMA_DEF, OllamaProvider


def test_ollama_def_has_correct_name():
    assert OLLAMA_DEF.name == "ollama"

def test_ollama_no_api_key_required():
    assert not OLLAMA_DEF.requires_api_key

def test_ollama_validate_passes_without_api_key():
    provider = OllamaProvider(definition=OLLAMA_DEF, model="llama3.2")
    errors = provider.validate()
    assert errors == []

def test_base_provider_chat_raises():
    from src.providers.base import Provider
    provider = Provider(definition=OLLAMA_DEF, model="llama3.2")
    with pytest.raises(NotImplementedError):
        provider.chat("system", "user")