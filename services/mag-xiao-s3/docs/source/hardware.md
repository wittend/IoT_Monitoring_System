---
# SPDX-License-Identifier: GPL-3.0-or-later
---

# Hardware

The project targets the Seeed Studio XIAO ESP32S3 and integrates these peripherals:

- PNI RM3100-CB magnetometer (I2C)
- Microchip MCP9808/MCP9804 temperature sensor (I2C)
- Seeed L76K GNSS module (UART + PPS)
- Seeed Wio SX1262 (LoRa)
- Power: battery + small solar panel (with appropriate charge/PMIC circuitry)

## Pins (XIAO ESP32S3)
- I2C: `SDA=GPIO5`, `SCL=GPIO6`
- GNSS UART1: `RX=GPIO44`, `TX=GPIO43`
- GNSS PPS: `GPIO2`
- LoRa (SX1262 via Wio):
  - `NSS=GPIO3`
  - `DIO1=GPIO4`
  - `NRST=GPIO1`
  - `BUSY=GPIO7`
  - SPI: default pins (MOSI=GPIO9, MISO=GPIO8, SCK=GPIO10)
- Config button: `GPIO42` (enters configuration portal)

> Always verify the latest Seeed XIAO ESP32S3 pinout and the Wio SX1262 wiring in case of board revisions.

## Buses and Speeds
- I2C: standard 100 kHz (default), higher modes may be possible depending on wiring and sensor tolerance.
- UART (GNSS): 115200 bps.
- SPI: default settings for RadioLib + SX1262; adjust via firmware if needed.

## Power Notes
- 3.3 V logic throughout.
- Ensure your PMIC/charger supports your chosen chemistry (LiPo/LiFePO/SLA).
- Keep wiring short; consider shielding if the magnetic environment is noisy.
