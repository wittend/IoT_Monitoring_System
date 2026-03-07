"""Tests for shared data models."""

from datetime import datetime

from iot_shared.models import Alert, AlertRule, AlertSeverity, SensorReading, SensorType


def test_sensor_reading_defaults():
    reading = SensorReading(
        sensor_id="sensor-001",
        sensor_type=SensorType.TEMPERATURE,
        value=22.5,
        unit="°C",
    )
    assert reading.sensor_id == "sensor-001"
    assert reading.sensor_type == SensorType.TEMPERATURE
    assert reading.value == 22.5
    assert reading.unit == "°C"
    assert reading.id is not None
    assert isinstance(reading.timestamp, datetime)
    assert reading.location is None
    assert reading.metadata is None


def test_sensor_reading_with_location():
    reading = SensorReading(
        sensor_id="sensor-002",
        sensor_type=SensorType.HUMIDITY,
        value=65.0,
        unit="%",
        location="Room A",
        metadata={"floor": 1},
    )
    assert reading.location == "Room A"
    assert reading.metadata == {"floor": 1}


def test_sensor_reading_unique_ids():
    r1 = SensorReading(sensor_id="s1", sensor_type=SensorType.CO2, value=400.0, unit="ppm")
    r2 = SensorReading(sensor_id="s1", sensor_type=SensorType.CO2, value=401.0, unit="ppm")
    assert r1.id != r2.id


def test_alert_defaults():
    alert = Alert(
        sensor_id="sensor-001",
        sensor_type=SensorType.TEMPERATURE,
        reading_id="reading-001",
        rule="max_value",
        value=45.0,
        threshold=40.0,
        severity=AlertSeverity.CRITICAL,
    )
    assert alert.acknowledged is False
    assert alert.id is not None
    assert isinstance(alert.timestamp, datetime)


def test_alert_rule_min_max():
    rule = AlertRule(
        sensor_type=SensorType.TEMPERATURE,
        max_value=40.0,
        severity=AlertSeverity.CRITICAL,
    )
    assert rule.sensor_type == SensorType.TEMPERATURE
    assert rule.max_value == 40.0
    assert rule.min_value is None


def test_all_sensor_types():
    types = [t.value for t in SensorType]
    assert "temperature" in types
    assert "humidity" in types
    assert "pressure" in types
    assert "co2" in types
    assert "motion" in types
    assert "light" in types


def test_all_alert_severities():
    severities = [s.value for s in AlertSeverity]
    assert "info" in severities
    assert "warning" in severities
    assert "critical" in severities
