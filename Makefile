.PHONY: install test test-shared test-sensor-agent test-collector run-collector run-agent lint

PYTHON ?= python3

# ---------------------------------------------------------------------------
# Install
# ---------------------------------------------------------------------------

install:
	$(PYTHON) -m pip install -e "shared[dev]"
	$(PYTHON) -m pip install -e "services/sensor_agent[dev]"
	$(PYTHON) -m pip install -e "services/collector[dev]"

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

test: test-shared test-sensor-agent test-collector

test-shared:
	$(PYTHON) -m pytest shared/ -v

test-sensor-agent:
	$(PYTHON) -m pytest services/sensor_agent/ -v

test-collector:
	$(PYTHON) -m pytest services/collector/ -v

# ---------------------------------------------------------------------------
# Run services locally
# ---------------------------------------------------------------------------

run-collector:
	$(PYTHON) -m uvicorn collector.app:app --reload --host 0.0.0.0 --port 8000

run-agent:
	COLLECTOR_URL=$${COLLECTOR_URL:-http://localhost:8000} $(PYTHON) -m sensor_agent.agent

# ---------------------------------------------------------------------------
# Docker
# ---------------------------------------------------------------------------

up:
	docker compose up --build

down:
	docker compose down
