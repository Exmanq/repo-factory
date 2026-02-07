# Architecture

```mermaid
graph TD
  User -->|runs| CLI[repofactory CLI]
  CLI -->|parses| CFG[config.yaml]
  CLI -->|validates| VALIDATOR
  CLI -->|renders| TPL[templates]
  TPL --> OUT[generated repo]
```

- Validation checks required fields and allowed values.
- Templates are Jinja-based per language/type; base assets cover LICENSE, README, CI.
- Features toggle extra assets (Dockerfile, lint configs, docs).
