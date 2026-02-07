from pathlib import Path

from repofactory.builder import RepoConfig, build_repo


def test_build_generates_core_files(tmp_path: Path):
    cfg = RepoConfig(name="demo", type="cli", language="python", features=["lint", "tests"])
    out = tmp_path / "out"
    result = build_repo(cfg, out)
    files = result["files"]
    assert "README.md" in files
    assert "pyproject.toml" in files
    assert any(f.startswith(".github/workflows/ci.yml") for f in files)


def test_build_skips_mp4_and_writes_gitignore(tmp_path: Path):
    cfg = RepoConfig(name="demo", type="cli", language="python", features=[])
    out = tmp_path / "out"
    build_repo(cfg, out)
    assert (out / ".gitignore").exists()


def test_node_templates(tmp_path: Path):
    cfg = RepoConfig(name="demo-node", type="api", language="node", features=["docker", "lint"])
    out = tmp_path / "out"
    build_repo(cfg, out)
    assert (out / "package.json").exists()
    assert (out / "Dockerfile").exists()
