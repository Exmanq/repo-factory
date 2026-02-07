from pathlib import Path

import yaml


def test_example_config_valid_fields():
    cfg_path = Path("config.example.yaml")
    data = yaml.safe_load(cfg_path.read_text())
    assert data["name"]
    assert data["type"] in {"library", "cli", "api", "saas-lite", "research"}
    assert data["language"] in {"python", "node"}


def test_templates_exist():
    for path in [
        Path("src/repofactory/templates/python/manifest.j2"),
        Path("src/repofactory/templates/node/manifest.j2"),
    ]:
        assert path.exists()
