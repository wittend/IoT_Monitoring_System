# mag-xiao-s3 (Seeed XIAO ESP32S3 Magnetometer Node)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3+-blue.svg)](LICENSE)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-ESP32-success)](platformio.ini)
[![Docs](https://img.shields.io/badge/docs-Read%20the%20Docs-brightgreen)](https://mag-xiao-s3.readthedocs.io/)

A small, battery/solar-powered firmware for the Seeed Studio XIAO ESP32S3 board.
- Samples a PNI RM3100 3‑axis magnetometer and an MCP9808/MCP9804 temperature sensor at 1 Hz
- Uses GNSS (L76K) PPS for timing and optional RTC discipline
- Transmits readings via LoRa (SX1262 / Wio-SX1262)
- Offers a simple Wi‑Fi configuration portal to set node identity, location, and radio params

## Hardware
- Seeed Studio XIAO ESP32S3
- PNI RM3100-CB magnetometer (I2C)
- Microchip MCP9808/9804 temperature sensor (I2C)
- Seeed L76K GNSS module (UART + PPS)
- Seeed Wio SX1262 (LoRa)
- Small solar panel + battery (LiPo/LiFePO/SLA)

## Build and Upload (PlatformIO)
- Prereqs: PlatformIO CLI (`pio`) or VS Code + PlatformIO
- Build:
  ```bash
  pio run -e seeed_xiao_esp32s3
  ```
- Upload:
  ```bash
  pio run -e seeed_xiao_esp32s3 -t upload
  ```
  If the port isn’t detected, double-tap reset to enter bootloader, then retry.
- Serial monitor (typical 115200):
  ```bash
  pio device monitor -b 115200
  ```

## Host-Native Tests
This repo includes a host-native test environment so you can run fast unit tests without hardware.
- Run all tests:
  ```bash
  pio test -e native
  ```

## Quickstart
1. Wire RM3100 and MCP9808 to I2C (SDA=GPIO5, SCL=GPIO6 on XIAO ESP32S3).
2. Connect L76K to UART1 (RX=GPIO44, TX=GPIO43) and PPS to GPIO2.
3. Attach the Wio SX1262 SPI lines as defined in `src/mag_xiao_s3.cpp` (NSS=3, DIO1=4, NRST=1, BUSY=7; default SPI pins).
4. Build and flash the firmware (see above).
5. On first boot or when configuration mode is triggered (button on GPIO42), connect to the device AP to enter configuration.

## Data Format
Readings are sent as JSON:
```json
{"ts":"26 Oct 2025 14:20:00","rt":25.000,"x":12345.678,"y":-234.500,"z":987.001}
```
- `ts`: UTC timestamp
- `rt`: remote temperature (°C)
- `x,y,z`: magnetic field components (nT)

## Documentation
- API (Doxygen) and User Docs (Sphinx/Furo) are provided and ready for Read the Docs.
- Build API docs (Doxygen):
  ```bash
  doxygen Doxyfile
  # HTML output: docs/doxygen/html/index.html
  ```
- Build Sphinx docs locally:
  ```bash
  mkdir -p docs/doxygen
  doxygen Doxyfile
  python -m pip install -r docs/requirements.txt
  sphinx-build -b html docs/source docs/_build/html
  ```
- Read the Docs: enable the repo in your RTD account. RTD will use `.readthedocs.yaml` to build both Doxygen and Sphinx.

## Contributing
Issues and PRs are welcome. Please keep `src/` Arduino-specific glue thin and place reusable logic under `include/` or `lib/` so it’s unit-testable on host.

## License
This project is licensed under the GNU General Public License v3.0 or later.

- SPDX-License-Identifier: GPL-3.0-or-later  
- See the `LICENSE` file for full text.

## Badges
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3+-blue.svg)](LICENSE)
[![PlatformIO](https://img.shields.io/badge/PlatformIO-ESP32-success)](platformio.ini)
[![Docs](https://img.shields.io/badge/docs-Read%20the%20Docs-brightgreen)](https://readthedocs.org/)  <!-- Replace with your project RTD URL when available -->
