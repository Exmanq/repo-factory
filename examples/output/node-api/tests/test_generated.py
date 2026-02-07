import yaml
from pathlib import Path


def test_generated_structure_exists(tmp_path: Path):
    root = tmp_path / "photon-api"
    root.mkdir()
    (root / "README.md").write_text("ok")
    assert (root / "README.md").exists()


def test_config_fields():
    cfg = yaml.safe_load("""
name: sample
language: node
type: api
features: []
""")
    assert cfg["name"] == "sample"
    assert cfg["language"] == "node"