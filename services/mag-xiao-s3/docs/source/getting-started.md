---
# SPDX-License-Identifier: GPL-3.0-or-later
---

# Getting Started

This guide helps you build, flash, and verify the firmware on a Seeed Studio XIAO ESP32S3.

## Prerequisites
- PlatformIO CLI (`pio`) or VS Code with the PlatformIO extension
- A Seeed Studio XIAO ESP32S3 board
- Optional sensors and modules:
  - PNI RM3100-CB (I2C)
  - Microchip MCP9808/MCP9804 (I2C)
  - Seeed L76K GNSS (UART + PPS)
  - Seeed Wio SX1262 (LoRa)

## Clone and Build
```bash
# From your workspace
pio run -e seeed_xiao_esp32s3
```

## Upload
Most systems auto-detect the port. If not detected, double-tap the reset button to enter bootloader mode and retry.
```bash
pio run -e seeed_xiao_esp32s3 -t upload
```

## Serial Monitor
Default baud is 115200 unless you changed it in the sketch.
```bash
pio device monitor -b 115200
```

## Host-Native Unit Tests
Run fast tests on your host machine (no hardware required):
```bash
pio test -e native
```

## Configuration Mode
On first boot, or when you press the configuration button (GPIO42), the device presents a Wi‑Fi access point for configuration. Use the web page to set:
- Node identification and owner
- Location (latitude, longitude, elevation)
- Orientation (90° rotations per axis)
- LoRa radio parameters
