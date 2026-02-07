from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

import yaml
from jinja2 import Environment, FileSystemLoader, Template

ALLOWED_TYPES = {"library", "cli", "api", "saas-lite", "research"}
ALLOWED_LANGS = {"python", "node"}
ALLOWED_FEATURES = {"docker", "ci", "lint", "tests", "docs"}


@dataclass
class RepoConfig:
    name: str
    type: str
    language: str
    features: List[str]


_TEMPLATE_ROOT = Path(__file__).parent / "templates"


def load_config(path: Path) -> RepoConfig:
    data = yaml.safe_load(path.read_text())
    return RepoConfig(
        name=str(data.get("name", "")).strip(),
        type=str(data.get("type", "")).strip(),
        language=str(data.get("language", "")).strip(),
        features=list(data.get("features", []) or []),
    )


def validate_config(cfg: RepoConfig) -> List[str]:
    errors: List[str] = []
    if not cfg.name:
        errors.append("name is required")
    if cfg.type not in ALLOWED_TYPES:
        errors.append(f"type must be one of {sorted(ALLOWED_TYPES)}")
    if cfg.language not in ALLOWED_LANGS:
        errors.append(f"language must be one of {sorted(ALLOWED_LANGS)}")
    unknown_features = [f for f in cfg.features if f not in ALLOWED_FEATURES]
    if unknown_features:
        errors.append(f"unknown features: {', '.join(unknown_features)}")
    return errors


def _env(template_dir: Path) -> Environment:
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    env.trim_blocks = True
    env.lstrip_blocks = True
    return env


def _render(template: Template, context: Dict[str, Any]) -> str:
    return template.render(**context)


def build_repo(cfg: RepoConfig, out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    ctx = {
        "name": cfg.name,
        "type": cfg.type,
        "language": cfg.language,
        "features": cfg.features,
    }

    env = _env(_TEMPLATE_ROOT)

    def write_template(rel: str, dest_rel: str | None = None) -> None:
        tmpl = env.get_template(rel)
        content = _render(tmpl, ctx)
        target = out_dir / (dest_rel or rel)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)

    base_prefix = "base/"
    base_files = {
        "LICENSE.j2": "LICENSE",
        "gitignore.j2": ".gitignore",
        "README.j2": "README.md",
        "CHANGELOG.j2": "CHANGELOG.md",
        "ROADMAP.j2": "ROADMAP.md",
        "CODE_OF_CONDUCT.j2": "CODE_OF_CONDUCT.md",
        "SECURITY.j2": "SECURITY.md",
        "CONTRIBUTING.j2": "CONTRIBUTING.md",
        "editorconfig.j2": ".editorconfig",
    }
    for src, dest in base_files.items():
        write_template(base_prefix + src, dest)

    # language specific
    write_template(f"{cfg.language}/makefile.j2", "Makefile")
    write_template(f"{cfg.language}/main.j2", "src/main.py" if cfg.language == "python" else "src/index.js")
    write_template(f"{cfg.language}/manifest.j2", "pyproject.toml" if cfg.language == "python" else "package.json")

    # docs
    write_template("base/docs/ARCHITECTURE.j2", "docs/ARCHITECTURE.md")
    write_template("base/docs/DESIGN_DECISIONS.j2", "docs/DESIGN_DECISIONS.md")
    write_template("base/docs/CONFIG.j2", "docs/CONFIG.md")

    # workflow
    write_template("base/github/ci.j2", ".github/workflows/ci.yml")
    write_template("base/github/bug.j2", ".github/ISSUE_TEMPLATE/bug.yml")
    write_template("base/github/feature.j2", ".github/ISSUE_TEMPLATE/feature.yml")
    write_template("base/github/pr.j2", ".github/PULL_REQUEST_TEMPLATE.md")

    # src package init (python only)
    if cfg.language == "python":
        pkg_dir = out_dir / "src" / cfg.name.replace("-", "_")
        pkg_dir.mkdir(parents=True, exist_ok=True)
        (pkg_dir / "__init__.py").write_text("""__version__ = '0.1.0'\n""")
        (out_dir / "src" / "__init__.py").write_text("")
    else:
        (out_dir / "src").mkdir(parents=True, exist_ok=True)

    # tests scaffolding
    write_template("base/tests/test_sample.j2", "tests/test_generated.py")

    # feature extras
    if "docker" in cfg.features:
        write_template(f"{cfg.language}/dockerfile.j2", "Dockerfile")
    if "lint" in cfg.features:
        if cfg.language == "python":
            write_template("python/ruff.j2", "ruff.toml")
            write_template("python/pre-commit.j2", ".pre-commit-config.yaml")
        else:
            write_template("node/eslint.j2", ".eslintrc.cjs")
            write_template("node/prettier.j2", ".prettierrc")
    if "docs" in cfg.features:
        write_template("base/docs/README_docs.j2", "docs/README.md")
    if "tests" in cfg.features and cfg.language == "node":
        write_template("node/jest.j2", "jest.config.cjs")

    return {
        "out": str(out_dir),
        "generated": True,
        "files": sorted(str(p.relative_to(out_dir)) for p in out_dir.rglob("*") if p.is_file()),
    }
