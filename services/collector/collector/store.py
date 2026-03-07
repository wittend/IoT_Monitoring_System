"""Thread-safe in-memory store for sensor readings and alerts."""

from __future__ import annotations

import threading
from datetime import datetime

from iot_shared.models import Alert, AlertRule, AlertSeverity, SensorReading, SensorType


DEFAULT_RULES: list[AlertRule] = [
    AlertRule(sensor_type=SensorType.TEMPERATURE, max_value=35.0, severity=AlertSeverity.WARNING),
    AlertRule(sensor_type=SensorType.TEMPERATURE, max_value=40.0, severity=AlertSeverity.CRITICAL),
    AlertRule(sensor_type=SensorType.HUMIDITY, max_value=80.0, severity=AlertSeverity.WARNING),
    AlertRule(sensor_type=SensorType.CO2, max_value=1000.0, severity=AlertSeverity.WARNING),
    AlertRule(sensor_type=SensorType.CO2, max_value=2000.0, severity=AlertSeverity.CRITICAL),
]


class ReadingStore:
    """Thread-safe in-memory store for readings and alerts."""

    def __init__(self, rules: list[AlertRule] | None = None) -> None:
        self._lock = threading.Lock()
        self._readings: dict[str, SensorReading] = {}
        self._alerts: dict[str, Alert] = {}
        self._rules: list[AlertRule] = rules if rules is not None else list(DEFAULT_RULES)

    # ------------------------------------------------------------------
    # Readings
    # ------------------------------------------------------------------

    def add_reading(self, reading: SensorReading) -> list[Alert]:
        """Store a reading and evaluate alert rules. Returns any new alerts."""
        new_alerts: list[Alert] = []
        with self._lock:
            self._readings[reading.id] = reading
            new_alerts = self._evaluate(reading)
            for alert in new_alerts:
                self._alerts[alert.id] = alert
        return new_alerts

    def get_readings(
        self,
        sensor_id: str | None = None,
        sensor_type: SensorType | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[SensorReading]:
        """Return stored readings with optional filters, newest first."""
        with self._lock:
            results = list(self._readings.values())
        if sensor_id:
            results = [r for r in results if r.sensor_id == sensor_id]
        if sensor_type:
            results = [r for r in results if r.sensor_type == sensor_type]
        if since:
            results = [r for r in results if r.timestamp >= since]
        results.sort(key=lambda r: r.timestamp, reverse=True)
        return results[:limit]

    # ------------------------------------------------------------------
    # Alerts
    # ------------------------------------------------------------------

    def get_alerts(
        self,
        acknowledged: bool | None = None,
        severity: AlertSeverity | None = None,
        limit: int = 100,
    ) -> list[Alert]:
        """Return stored alerts with optional filters, newest first."""
        with self._lock:
            results = list(self._alerts.values())
        if acknowledged is not None:
            results = [a for a in results if a.acknowledged == acknowledged]
        if severity:
            results = [a for a in results if a.severity == severity]
        results.sort(key=lambda a: a.timestamp, reverse=True)
        return results[:limit]

    def acknowledge_alert(self, alert_id: str) -> Alert | None:
        """Mark an alert as acknowledged. Returns the updated alert or None."""
        with self._lock:
            alert = self._alerts.get(alert_id)
            if alert:
                updated = alert.model_copy(update={"acknowledged": True})
                self._alerts[alert_id] = updated
                return updated
        return None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _evaluate(self, reading: SensorReading) -> list[Alert]:
        """Evaluate all rules against *reading* and return triggered alerts."""
        triggered: list[Alert] = []
        for rule in self._rules:
            if rule.sensor_type != reading.sensor_type:
                continue
            if rule.max_value is not None and reading.value > rule.max_value:
                triggered.append(
                    Alert(
                        sensor_id=reading.sensor_id,
                        sensor_type=reading.sensor_type,
                        reading_id=reading.id,
                        rule="max_value",
                        value=reading.value,
                        threshold=rule.max_value,
                        severity=rule.severity,
                    )
                )
            if rule.min_value is not None and reading.value < rule.min_value:
                triggered.append(
                    Alert(
                        sensor_id=reading.sensor_id,
                        sensor_type=reading.sensor_type,
                        reading_id=reading.id,
                        rule="min_value",
                        value=reading.value,
                        threshold=rule.min_value,
                        severity=rule.severity,
                    )
                )
        return triggered
