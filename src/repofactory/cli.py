import json
import sys
from pathlib import Path

import click

from .builder import build_repo, load_config, validate_config


@click.group()
def main() -> None:
    """repo-factory CLI."""


@main.command("build")
@click.argument("config_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--out", "out_dir", required=True, type=click.Path(path_type=Path))
def cmd_build(config_path: Path, out_dir: Path) -> None:
    """Generate a repository from CONFIG_PATH into OUT."""
    cfg = load_config(config_path)
    errors = validate_config(cfg)
    if errors:
        click.echo("Config validation failed:\n" + "\n".join(f"- {e}" for e in errors), err=True)
        sys.exit(1)
    result = build_repo(cfg, out_dir)
    click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":  # pragma: no cover
    main()
