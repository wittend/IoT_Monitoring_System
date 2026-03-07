# IoT Monitoring System — System Specification

## 1. Purpose

The IoT Monitoring System is a distributed platform for collecting, storing,
and alerting on measurements produced by Internet-of-Things (IoT) sensor
devices. The system is designed to be:

* **Scalable** — multiple sensor agents can run independently across sites.
* **Extensible** — new sensor types and alert rules can be added without
  modifying the collector.
* **Observable** — every component logs structured messages; the collector
  exposes a REST API for querying readings and alerts.

---

## 2. Scope

This specification covers:

1. Shared data models (the canonical schema for sensor readings and alerts).
2. The **Sensor Agent** service.
3. The **Collector** service.
4. Inter-service communication protocol.
5. Deployment using Docker Compose.

---

## 3. Shared Data Models

All services use the `iot_shared` Python package (`shared/`) to ensure a
single source of truth for data schemas.

### 3.1 `SensorType` (enum)

| Value         | Description                |
|---------------|----------------------------|
| `temperature` | Ambient temperature        |
| `humidity`    | Relative humidity          |
| `pressure`    | Atmospheric pressure       |
| `co2`         | CO₂ concentration          |
| `motion`      | Motion detection (0 or 1)  |
| `light`       | Illuminance                |

### 3.2 `AlertSeverity` (enum)

| Value      | Description                                  |
|------------|----------------------------------------------|
| `info`     | Informational — no action required           |
| `warning`  | Attention needed — approaching a threshold   |
| `critical` | Immediate action required                    |

### 3.3 `SensorReading`

| Field         | Type               | Required | Description                          |
|---------------|--------------------|----------|--------------------------------------|
| `id`          | string (UUID)      | auto     | Unique identifier                    |
| `sensor_id`   | string             | yes      | Unique identifier of the sensor      |
| `sensor_type` | `SensorType`       | yes      | Type of measurement                  |
| `value`       | float              | yes      | Measured value                       |
| `unit`        | string             | yes      | Unit of measure (e.g. `°C`, `%`)     |
| `timestamp`   | datetime (UTC)     | auto     | Time of measurement (UTC)            |
| `location`    | string             | no       | Human-readable location label        |
| `metadata`    | object             | no       | Arbitrary key-value pairs            |

### 3.4 `AlertRule`

| Field         | Type               | Required | Description                          |
|---------------|--------------------|----------|--------------------------------------|
| `sensor_type` | `SensorType`       | yes      | Which sensor type this rule applies to |
| `min_value`   | float              | no       | Trigger alert when value < min_value |
| `max_value`   | float              | no       | Trigger alert when value > max_value |
| `severity`    | `AlertSeverity`    | yes      | Severity of generated alert          |

### 3.5 `Alert`

| Field         | Type               | Required | Description                          |
|---------------|--------------------|----------|--------------------------------------|
| `id`          | string (UUID)      | auto     | Unique identifier                    |
| `sensor_id`   | string             | auto     | From the triggering reading          |
| `sensor_type` | `SensorType`       | auto     | From the triggering reading          |
| `reading_id`  | string             | auto     | ID of the triggering reading         |
| `rule`        | string             | auto     | `"min_value"` or `"max_value"`       |
| `value`       | float              | auto     | The value that violated the rule     |
| `threshold`   | float              | auto     | The threshold that was violated      |
| `severity`    | `AlertSeverity`    | auto     | From the triggering alert rule       |
| `timestamp`   | datetime (UTC)     | auto     | Time the alert was created           |
| `acknowledged`| boolean            | auto     | Whether a human has acknowledged it  |

---

## 4. Sensor Agent

### 4.1 Responsibilities

* Periodically sample each registered sensor.
* Package each reading as a `SensorReading` JSON payload.
* POST the payload to the collector's `/readings` endpoint.
* Retry or log on transient network failures without crashing.

### 4.2 Built-in Sensor Simulators

| Class              | `sensor_type`  | Unit | Simulation notes                    |
|--------------------|----------------|------|-------------------------------------|
| `TemperatureSensor`| `temperature`  | °C   | Base 20 °C with sinusoidal drift    |
| `HumiditySensor`   | `humidity`     | %    | Base 50 % with Gaussian noise       |
| `PressureSensor`   | `pressure`     | hPa  | Base 1013.25 hPa with small noise   |
| `CO2Sensor`        | `co2`          | ppm  | Base 400 ppm with business-hours bump|

### 4.3 Configuration (environment variables)

| Variable          | Default                 | Description                          |
|-------------------|-------------------------|--------------------------------------|
| `COLLECTOR_URL`   | `http://localhost:8000` | Base URL of the collector service    |
| `SENSOR_INTERVAL` | `5`                     | Seconds between each sampling cycle  |
| `SENSOR_LOCATION` | `default`               | Location prefix for sensor IDs       |
| `LOG_LEVEL`       | `INFO`                  | Python logging level                 |

### 4.4 Failure Handling

* Network errors are caught per-reading; the agent continues to the next
  sensor without crashing.
* A warning is logged for each failed transmission.
* The agent exits cleanly on `SIGINT` / `KeyboardInterrupt`.

---

## 5. Collector Service

### 5.1 Responsibilities

* Accept `SensorReading` objects from one or more sensor agents.
* Persist readings in an in-memory store (indexed by ID).
* Evaluate all registered `AlertRule`s against each incoming reading.
* Persist triggered `Alert` objects.
* Expose a REST API for querying readings and alerts.

### 5.2 REST API

All endpoints accept and return JSON. Timestamps are ISO-8601 strings in UTC.

#### `POST /readings`

Ingest a new sensor reading.

* **Request**: `SensorReading` object (JSON)
* **Response 201**: Echo of the stored reading
* **Response 422**: Validation error

#### `GET /readings`

List stored readings (newest first).

| Query param   | Type       | Description                                  |
|---------------|------------|----------------------------------------------|
| `sensor_id`   | string     | Filter to a specific sensor                  |
| `sensor_type` | string     | Filter to a specific sensor type             |
| `since`       | datetime   | Return only readings on or after this time   |
| `limit`       | integer    | Max results to return (default 100, max 1000)|

#### `GET /alerts`

List triggered alerts (newest first).

| Query param    | Type    | Description                                  |
|----------------|---------|----------------------------------------------|
| `acknowledged` | boolean | Filter by acknowledgement status             |
| `severity`     | string  | Filter by severity                           |
| `limit`        | integer | Max results to return (default 100, max 1000)|

#### `PATCH /alerts/{id}/acknowledge`

Mark an alert as acknowledged.

* **Response 200**: Updated alert object
* **Response 404**: Alert not found

#### `GET /health`

Liveness check.

* **Response 200**: `{"status": "ok"}`

### 5.3 Default Alert Rules

| Sensor Type   | Condition           | Severity   |
|---------------|---------------------|------------|
| `temperature` | value > 35 °C       | `warning`  |
| `temperature` | value > 40 °C       | `critical` |
| `humidity`    | value > 80 %        | `warning`  |
| `co2`         | value > 1000 ppm    | `warning`  |
| `co2`         | value > 2000 ppm    | `critical` |

### 5.4 Configuration (environment variables)

| Variable      | Default   | Description                                             |
|---------------|-----------|---------------------------------------------------------|
| `HOST`        | `0.0.0.0` | Interface to bind                                       |
| `PORT`        | `8000`    | Port to listen on                                       |
| `LOG_LEVEL`   | `INFO`    | Python logging level                                    |
| `CORS_ORIGINS`| *(empty)* | Comma-separated allowed CORS origins (e.g. `https://dashboard.example.com`) |

---

## 6. Inter-Service Communication

The sensor agent communicates with the collector using plain **HTTP/1.1**.

* **Protocol**: HTTP with JSON bodies
* **Endpoint**: `POST {COLLECTOR_URL}/readings`
* **Content-Type**: `application/json`
* **Timeout**: 5 seconds per request
* **Retry policy**: No automatic retry in the current version; failed requests
  are logged as warnings and the agent continues.

---

## 7. Deployment

### 7.1 Docker Compose (development/demo)

`docker compose up` starts:

| Service        | Image built from              | Exposed port |
|----------------|-------------------------------|--------------|
| `collector`    | `services/collector/`         | 8000         |
| `sensor-agent` | `services/sensor_agent/`      | none         |

The sensor agent is configured to send to `http://collector:8000`.

### 7.2 Scaling

To simulate multiple sites, override `SENSOR_LOCATION` per agent replica:

```yaml
sensor-agent-lab:
  build: services/sensor_agent
  environment:
    COLLECTOR_URL: http://collector:8000
    SENSOR_LOCATION: lab

sensor-agent-office:
  build: services/sensor_agent
  environment:
    COLLECTOR_URL: http://collector:8000
    SENSOR_LOCATION: office
```

---

## 8. Non-Functional Requirements

| Requirement     | Target                                              |
|-----------------|-----------------------------------------------------|
| Language        | Python 3.11+                                        |
| Build tool      | Hatchling (PEP 517)                                 |
| Test framework  | pytest                                              |
| API framework   | FastAPI + Uvicorn                                   |
| Data validation | Pydantic v2                                         |
| HTTP client     | HTTPX (async)                                       |
| Storage         | In-memory (thread-safe) — persistent storage is a  |
|                 | planned future enhancement                          |

---

## 9. Future Enhancements

* Persistent storage backend (PostgreSQL / InfluxDB / SQLite).
* Message-queue transport layer (MQTT or AMQP) between agent and collector.
* Authentication and TLS between agent and collector.
* Time-series aggregation endpoints (`/readings/aggregate`).
* WebSocket push for real-time dashboard consumers.
* Helm chart / Kubernetes manifests for production deployment.
