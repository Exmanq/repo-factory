import json
from pathlib import Path

from click.testing import CliRunner

from repofactory.cli import main


def test_cli_build(tmp_path: Path):
    cfg = tmp_path / "cfg.yaml"
    cfg.write_text("""
name: sample
language: python
type: cli
features: [lint, tests]
""")
    out_dir = tmp_path / "generated"
    runner = CliRunner()
    result = runner.invoke(main, ["build", str(cfg), "--out", str(out_dir)])
    assert result.exit_code == 0
    payload = json.loads(result.output)
    assert payload["generated"] is True
    assert (out_dir / "README.md").exists()
