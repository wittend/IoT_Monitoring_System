# IoT Monitoring System

A monorepo for a distributed sensor data collection system built in Python.

## Overview

The IoT Monitoring System collects real-time measurements from distributed IoT
sensors, ingests them into a central collector service, evaluates configurable
alert rules, and exposes a REST API for downstream consumers.

```
┌─────────────────────────────────────────────────────────┐
│  IoT Devices / Sensor Simulators                        │
│  (services/sensor_agent)                                │
│                                                         │
│  TemperatureSensor  HumiditySensor  PressureSensor …   │
└───────────────────────┬─────────────────────────────────┘
                        │  HTTP POST /readings
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Collector Service  (services/collector)                │
│                                                         │
│  POST /readings  – ingest & validate                    │
│  GET  /readings  – query stored readings                │
│  GET  /alerts    – query triggered alerts               │
│  PATCH /alerts/{id}/acknowledge                         │
└─────────────────────────────────────────────────────────┘
```

## Repository Structure

```
IoT_Monitoring_System/
├── SPEC.md                    # Full system specification
├── docker-compose.yml         # Orchestrate all services
├── Makefile                   # Common development tasks
├── shared/                    # Shared Python package (models, enums)
│   ├── pyproject.toml
│   ├── iot_shared/
│   │   ├── __init__.py
│   │   └── models.py          # SensorReading, Alert, AlertRule, enums
│   └── tests/
│       └── test_models.py
└── services/
    ├── sensor_agent/          # IoT agent — reads sensors, ships data
    │   ├── pyproject.toml
    │   ├── sensor_agent/
    │   │   ├── agent.py
    │   │   └── sensors.py
    │   ├── tests/
    │   │   └── test_sensors.py
    │   └── Dockerfile
    └── collector/             # Collector — ingest, store, alert, API
        ├── pyproject.toml
        ├── collector/
        │   ├── app.py
        │   └── store.py
        ├── tests/
        │   └── test_collector.py
        └── Dockerfile
```

## Quick Start

### Prerequisites

- Python 3.11+
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/)

### Run with Docker Compose

```bash
docker compose up
```

The collector API will be available at <http://localhost:8000>.
Interactive API docs: <http://localhost:8000/docs>

### Local Development

Install all packages in editable mode (uses a virtual environment):

```bash
make install
```

Run the full test suite:

```bash
make test
```

Run individual service tests:

```bash
make test-shared
make test-sensor-agent
make test-collector
```

Start just the collector locally:

```bash
make run-collector
```

Start the sensor agent (pointing at a running collector):

```bash
COLLECTOR_URL=http://localhost:8000 make run-agent
```

## Configuration

All configuration is done through environment variables.

### Sensor Agent

| Variable          | Default                  | Description                        |
|-------------------|--------------------------|------------------------------------|
| `COLLECTOR_URL`   | `http://localhost:8000`  | URL of the collector service       |
| `SENSOR_INTERVAL` | `5`                      | Seconds between readings           |
| `SENSOR_LOCATION` | `default`                | Location tag applied to sensor IDs |
| `LOG_LEVEL`       | `INFO`                   | Logging level                      |

### Collector

| Variable      | Default     | Description                                             |
|---------------|-------------|---------------------------------------------------------|
| `HOST`        | `0.0.0.0`   | Interface to bind                                        |
| `PORT`        | `8000`      | Port to listen on                                        |
| `LOG_LEVEL`   | `INFO`      | Logging level                                            |
| `CORS_ORIGINS`| *(empty)*   | Comma-separated allowed CORS origins                     |

## API Reference

### `POST /readings`
Submit a sensor reading.

**Request body** (`SensorReading`):
```json
{
  "sensor_id": "office-temp-01",
  "sensor_type": "temperature",
  "value": 22.5,
  "unit": "°C",
  "location": "Office A"
}
```

### `GET /readings`
List stored readings. Query params: `sensor_id`, `sensor_type`, `since` (ISO-8601), `limit`.

### `GET /alerts`
List triggered alerts. Query params: `acknowledged` (bool), `severity`, `limit`.

### `PATCH /alerts/{id}/acknowledge`
Mark an alert as acknowledged.

### `GET /health`
Health check — returns `{"status": "ok"}`.

## Sensor Types

| Value         | Description                    | Typical unit |
|---------------|--------------------------------|--------------|
| `temperature` | Ambient temperature            | °C           |
| `humidity`    | Relative humidity              | %            |
| `pressure`    | Atmospheric pressure           | hPa          |
| `co2`         | CO₂ concentration              | ppm          |
| `motion`      | Motion detected (0/1)          | —            |
| `light`       | Illuminance                    | lux          |

## Alert Severities

| Value      | Meaning                                       |
|------------|-----------------------------------------------|
| `info`     | Informational — no action required            |
| `warning`  | Attention needed — approaching a threshold    |
| `critical` | Immediate action required                     |

## License

GNU General Public License v3 — see [LICENSE](LICENSE).
