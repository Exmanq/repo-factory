# Config

Schema (yaml):

```yaml
name: string
type: [library, cli, api, saas-lite, research]
language: [python, node]
features: [docker, ci, lint, tests, docs]
```

Run:

```bash
repofactory build config.example.yaml --out ./generated
```
