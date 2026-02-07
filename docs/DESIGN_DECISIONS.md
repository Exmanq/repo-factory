# Design Decisions

- Default to Python 3.11 and Node 20 because they are widely available.
- Use Jinja templates to keep generated repos deterministic and easy to extend.
- Include CI + lint/test hooks by default for confidence.
- Keep dependencies small (click, pyyaml, jinja2) for fast installs.
