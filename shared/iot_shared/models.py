"""Pydantic data models shared across all services."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class SensorType(str, Enum):
    """Supported sensor measurement types."""

    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    CO2 = "co2"
    MOTION = "motion"
    LIGHT = "light"


class AlertSeverity(str, Enum):
    """Severity levels for triggered alerts."""

    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class SensorReading(BaseModel):
    """A single measurement from an IoT sensor."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sensor_id: str
    sensor_type: SensorType
    value: float
    unit: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    location: str | None = None
    metadata: dict[str, Any] | None = None


class AlertRule(BaseModel):
    """A rule that triggers an alert when a threshold is crossed."""

    sensor_type: SensorType
    min_value: float | None = None
    max_value: float | None = None
    severity: AlertSeverity = AlertSeverity.WARNING


class Alert(BaseModel):
    """An alert triggered by a sensor reading exceeding a threshold."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    sensor_id: str
    sensor_type: SensorType
    reading_id: str
    rule: str
    value: float
    threshold: float
    severity: AlertSeverity
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    acknowledged: bool = False
