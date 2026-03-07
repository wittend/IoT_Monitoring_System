"""Tests for sensor simulators."""

import pytest
from iot_shared.models import SensorType
from sensor_agent.sensors import CO2Sensor, HumiditySensor, PressureSensor, TemperatureSensor


def test_temperature_sensor_returns_reading():
    sensor = TemperatureSensor(sensor_id="test-temp-01", location="Lab")
    reading = sensor.read()
    assert reading.sensor_id == "test-temp-01"
    assert reading.sensor_type == SensorType.TEMPERATURE
    assert reading.unit == "°C"
    assert reading.location == "Lab"
    assert isinstance(reading.value, float)


def test_humidity_sensor_value_in_range():
    sensor = HumiditySensor(sensor_id="test-hum-01")
    for _ in range(50):
        reading = sensor.read()
        assert 0.0 <= reading.value <= 100.0, f"Humidity out of range: {reading.value}"


def test_pressure_sensor_returns_reading():
    sensor = PressureSensor(sensor_id="test-pres-01")
    reading = sensor.read()
    assert reading.sensor_type == SensorType.PRESSURE
    assert reading.unit == "hPa"
    assert isinstance(reading.value, float)


def test_co2_sensor_value_above_floor():
    sensor = CO2Sensor(sensor_id="test-co2-01")
    for _ in range(20):
        reading = sensor.read()
        assert reading.value >= 350.0, f"CO2 below floor: {reading.value}"


def test_sensor_reading_has_id():
    sensor = TemperatureSensor(sensor_id="test-id-01")
    reading = sensor.read()
    assert reading.id is not None
    assert len(reading.id) > 0


def test_sensor_readings_have_unique_ids():
    sensor = TemperatureSensor(sensor_id="test-unique-01")
    r1 = sensor.read()
    r2 = sensor.read()
    assert r1.id != r2.id


def test_sensor_without_location():
    sensor = HumiditySensor(sensor_id="no-loc-01")
    reading = sensor.read()
    assert reading.location is None


@pytest.mark.asyncio
async def test_send_reading_success(respx_mock):
    import httpx
    from sensor_agent.agent import send_reading
    from iot_shared.models import SensorReading, SensorType

    reading = SensorReading(
        sensor_id="s1",
        sensor_type=SensorType.TEMPERATURE,
        value=22.0,
        unit="°C",
    )
    respx_mock.post("http://collector:8000/readings").mock(
        return_value=httpx.Response(201, json=reading.model_dump(mode="json"))
    )
    async with httpx.AsyncClient() as client:
        result = await send_reading(client, "http://collector:8000", reading)
    assert result is True


@pytest.mark.asyncio
async def test_send_reading_network_error(respx_mock):
    import httpx
    from sensor_agent.agent import send_reading
    from iot_shared.models import SensorReading, SensorType

    reading = SensorReading(
        sensor_id="s1",
        sensor_type=SensorType.TEMPERATURE,
        value=22.0,
        unit="°C",
    )
    respx_mock.post("http://collector:8000/readings").mock(
        side_effect=httpx.ConnectError("refused")
    )
    async with httpx.AsyncClient() as client:
        result = await send_reading(client, "http://collector:8000", reading)
    assert result is False
