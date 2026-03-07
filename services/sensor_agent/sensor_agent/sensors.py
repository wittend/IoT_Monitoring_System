"""Sensor simulators for the IoT monitoring system."""

from __future__ import annotations

import math
import random
import time
from dataclasses import dataclass, field

from iot_shared.models import SensorReading, SensorType


@dataclass
class TemperatureSensor:
    """Simulates a temperature sensor with realistic sinusoidal drift."""

    sensor_id: str
    location: str | None = None
    _base_value: float = field(default=20.0, init=False, repr=False)
    _noise_std: float = field(default=0.5, init=False, repr=False)

    sensor_type: SensorType = field(default=SensorType.TEMPERATURE, init=False)
    unit: str = field(default="°C", init=False)

    def read(self) -> SensorReading:
        drift = math.sin(time.time() / 3600) * 3
        noise = random.gauss(0, self._noise_std)
        value = round(self._base_value + drift + noise, 2)
        return SensorReading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            unit=self.unit,
            location=self.location,
        )


@dataclass
class HumiditySensor:
    """Simulates a relative humidity sensor (0–100 %)."""

    sensor_id: str
    location: str | None = None
    _base_value: float = field(default=50.0, init=False, repr=False)

    sensor_type: SensorType = field(default=SensorType.HUMIDITY, init=False)
    unit: str = field(default="%", init=False)

    def read(self) -> SensorReading:
        noise = random.gauss(0, 2.0)
        value = round(max(0.0, min(100.0, self._base_value + noise)), 2)
        return SensorReading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            unit=self.unit,
            location=self.location,
        )


@dataclass
class PressureSensor:
    """Simulates an atmospheric pressure sensor."""

    sensor_id: str
    location: str | None = None
    _base_value: float = field(default=1013.25, init=False, repr=False)

    sensor_type: SensorType = field(default=SensorType.PRESSURE, init=False)
    unit: str = field(default="hPa", init=False)

    def read(self) -> SensorReading:
        noise = random.gauss(0, 0.5)
        value = round(self._base_value + noise, 2)
        return SensorReading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            unit=self.unit,
            location=self.location,
        )


@dataclass
class CO2Sensor:
    """Simulates a CO₂ concentration sensor with a business-hours bump."""

    sensor_id: str
    location: str | None = None
    _base_value: float = field(default=400.0, init=False, repr=False)

    sensor_type: SensorType = field(default=SensorType.CO2, init=False)
    unit: str = field(default="ppm", init=False)

    def read(self) -> SensorReading:
        hour = time.gmtime().tm_hour
        hourly_offset = (
            200 * max(0.0, math.sin(math.pi * (hour - 8) / 10)) if 8 <= hour <= 18 else 0.0
        )
        noise = random.gauss(0, 10.0)
        value = round(max(350.0, self._base_value + hourly_offset + noise), 2)
        return SensorReading(
            sensor_id=self.sensor_id,
            sensor_type=self.sensor_type,
            value=value,
            unit=self.unit,
            location=self.location,
        )
