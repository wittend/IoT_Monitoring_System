Firmware Design
===============

The firmware is developed using the ESP-IDF framework (v5.x) and PlatformIO.

Main Tasks
----------

- **Sensor Task**: Samples RM3100 (magnetometer) and MCP9808 (temperature) at 1Hz.
- **GNSS Task**: Handles time synchronization and PPS triggering.
- **LoRa Task**: Transmits data packets via the SX1262 module.

Data Format
-----------

Data is formatted as JSONL strings:

.. code-block:: json

   {"ts":"26 Oct 2025 14:20:00", "rt": 25.000, "x":12345.678, "y":-234.500, "z":987.001}

Configuration Mode
------------------

The device can be put into configuration mode via BLE or WiFi to set parameters such as node ID, location, and LoRa settings.
