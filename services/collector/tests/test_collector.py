"""Integration tests for the collector REST API."""

import pytest
from fastapi.testclient import TestClient

from collector.app import create_app
from collector.store import ReadingStore
from iot_shared.models import AlertRule, AlertSeverity, SensorType


@pytest.fixture
def client():
    store = ReadingStore(
        rules=[
            AlertRule(
                sensor_type=SensorType.TEMPERATURE,
                max_value=30.0,
                severity=AlertSeverity.WARNING,
            ),
            AlertRule(
                sensor_type=SensorType.TEMPERATURE,
                max_value=40.0,
                severity=AlertSeverity.CRITICAL,
            ),
        ]
    )
    return TestClient(create_app(store))


def _reading(**kwargs) -> dict:
    defaults = dict(
        sensor_id="sensor-001",
        sensor_type="temperature",
        value=22.0,
        unit="°C",
    )
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


class TestHealth:
    def test_health_ok(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# Readings
# ---------------------------------------------------------------------------


class TestReadings:
    def test_ingest_reading_returns_201(self, client):
        resp = client.post("/readings", json=_reading())
        assert resp.status_code == 201
        body = resp.json()
        assert body["sensor_id"] == "sensor-001"
        assert body["sensor_type"] == "temperature"
        assert body["value"] == 22.0

    def test_list_readings_empty_on_fresh_store(self, client):
        resp = client.get("/readings")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_readings_after_ingest(self, client):
        client.post("/readings", json=_reading(value=23.0))
        resp = client.get("/readings")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_filter_by_sensor_id(self, client):
        client.post("/readings", json=_reading(sensor_id="s-001", value=20.0))
        client.post("/readings", json=_reading(sensor_id="s-002", value=21.0))
        resp = client.get("/readings?sensor_id=s-001")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["sensor_id"] == "s-001"

    def test_filter_by_sensor_type(self, client):
        client.post("/readings", json=_reading(sensor_type="temperature", value=20.0))
        client.post("/readings", json=_reading(sensor_type="humidity", value=55.0, unit="%"))
        resp = client.get("/readings?sensor_type=humidity")
        data = resp.json()
        assert len(data) == 1
        assert data[0]["sensor_type"] == "humidity"

    def test_limit_parameter(self, client):
        for i in range(5):
            client.post("/readings", json=_reading(value=float(i)))
        resp = client.get("/readings?limit=3")
        assert len(resp.json()) == 3

    def test_invalid_sensor_type_returns_422(self, client):
        resp = client.post("/readings", json=_reading(sensor_type="nonexistent"))
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------


class TestAlerts:
    def test_no_alert_within_threshold(self, client):
        client.post("/readings", json=_reading(value=25.0))
        resp = client.get("/alerts")
        assert resp.json() == []

    def test_alert_triggered_above_max(self, client):
        client.post("/readings", json=_reading(value=35.0))
        alerts = client.get("/alerts").json()
        assert len(alerts) >= 1
        assert alerts[0]["sensor_id"] == "sensor-001"
        assert alerts[0]["severity"] == "warning"

    def test_acknowledge_alert(self, client):
        client.post("/readings", json=_reading(value=35.0))
        alerts = client.get("/alerts").json()
        alert_id = alerts[0]["id"]
        resp = client.patch(f"/alerts/{alert_id}/acknowledge")
        assert resp.status_code == 200
        assert resp.json()["acknowledged"] is True

    def test_acknowledge_nonexistent_alert_returns_404(self, client):
        resp = client.patch("/alerts/nonexistent/acknowledge")
        assert resp.status_code == 404

    def test_filter_unacknowledged_alerts(self, client):
        client.post("/readings", json=_reading(value=35.0))
        alerts = client.get("/alerts").json()
        alert_id = alerts[0]["id"]
        client.patch(f"/alerts/{alert_id}/acknowledge")

        unacked = client.get("/alerts?acknowledged=false").json()
        acked = client.get("/alerts?acknowledged=true").json()
        assert any(a["id"] == alert_id for a in acked)
        assert not any(a["id"] == alert_id for a in unacked)

    def test_filter_by_severity(self, client):
        client.post("/readings", json=_reading(value=45.0))
        critical = client.get("/alerts?severity=critical").json()
        assert len(critical) >= 1
        assert all(a["severity"] == "critical" for a in critical)
