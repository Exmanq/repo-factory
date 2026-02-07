PYTHON := python3
VENV := .venv
PIP := $(VENV)/bin/pip
PYTEST := $(VENV)/bin/pytest
RUFF := $(VENV)/bin/ruff
BLACK := $(VENV)/bin/black

.PHONY: setup lint test demo run format

setup:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -e .[dev]

lint:
	$(RUFF) check src tests
	$(BLACK) --check src tests

format:
	$(BLACK) src tests
	$(RUFF) check --fix src tests

test:
	$(PYTEST)

run demo:
	$(VENV)/bin/repofactory build config.example.yaml --out examples/output/demo
	@echo "Demo generated at examples/output/demo"
