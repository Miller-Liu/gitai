from unittest.mock import patch

from src.config import DEFAULTS, load


def test_load_returns_defaults_when_no_config(tmp_path):
    fake_path = tmp_path / ".gitai" / "config.toml"
    with patch("src.config.CONFIG_PATH", fake_path):
        config = load()
    assert config["provider"] == DEFAULTS["provider"]
    assert config["model"] == DEFAULTS["model"]