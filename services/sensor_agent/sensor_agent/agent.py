"""IoT sensor agent — collects readings and ships them to the collector service."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from collections.abc import Sequence

import httpx

from iot_shared.models import SensorReading
from sensor_agent.sensors import CO2Sensor, HumiditySensor, PressureSensor, TemperatureSensor

logger = logging.getLogger(__name__)


def build_default_sensors() -> list:
    """Return a default set of sensors for the configured location."""
    location = os.getenv("SENSOR_LOCATION", "default")
    return [
        TemperatureSensor(sensor_id=f"{location}-temp-01", location=location),
        HumiditySensor(sensor_id=f"{location}-hum-01", location=location),
        PressureSensor(sensor_id=f"{location}-pres-01", location=location),
        CO2Sensor(sensor_id=f"{location}-co2-01", location=location),
    ]


async def send_reading(
    client: httpx.AsyncClient,
    collector_url: str,
    reading: SensorReading,
) -> bool:
    """POST a single reading to the collector. Returns True on success."""
    try:
        response = await client.post(
            f"{collector_url}/readings",
            json=reading.model_dump(mode="json"),
            timeout=5.0,
        )
        response.raise_for_status()
        return True
    except httpx.HTTPError as exc:
        logger.warning("Failed to send reading %s: %s", reading.id, exc)
        return False


async def run(sensors: Sequence, collector_url: str, interval: float) -> None:
    """Main agent loop — samples all sensors and ships data every *interval* seconds."""
    logger.info(
        "Starting agent: %d sensor(s), collector=%s, interval=%.1fs",
        len(sensors),
        collector_url,
        interval,
    )
    async with httpx.AsyncClient() as client:
        while True:
            for sensor in sensors:
                reading = sensor.read()
                success = await send_reading(client, collector_url, reading)
                if success:
                    logger.debug(
                        "Sent %s reading from %s: %.2f %s",
                        reading.sensor_type,
                        reading.sensor_id,
                        reading.value,
                        reading.unit,
                    )
            await asyncio.sleep(interval)


def main() -> None:
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s — %(message)s",
    )
    collector_url = os.getenv("COLLECTOR_URL", "http://localhost:8000")
    interval = float(os.getenv("SENSOR_INTERVAL", "5"))
    sensors = build_default_sensors()
    try:
        asyncio.run(run(sensors, collector_url, interval))
    except KeyboardInterrupt:
        logger.info("Agent stopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
