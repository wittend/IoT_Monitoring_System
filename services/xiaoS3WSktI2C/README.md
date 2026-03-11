# XIAO ESP32S3 Edge Data Collector

Firmware for Seeed Studio XIAO ESP32S3 acting as an IoT edge data collector for magnetic and temperature sensors, with LoRa relay capabilities.

## Features

- **Sensors**: 
  - PNI RM3100 (Magnetometer) via I2C.
  - Microchip MCP9808 (Temperature) via I2C.
  - Seeed Studio L76K (GNSS) via UART for timing and PPS.
- **Connectivity**: 
  - Semtech SX1262 (LoRa) for long-range data transmission.
  - WiFi Access Point for web-based configuration.
- **Data Format**: 1Hz sampling, output as JSONL strings.
- **Power Management**: Optimized for battery operation with solar charging support.

## Getting Started

### Prerequisites

- [PlatformIO Core](https://docs.platformio.org/en/latest/core/index.html)
- Seeed Studio XIAO ESP32S3 module

### Build and Upload

1. Clone the repository.
2. Build the project:
   ```bash
   pio run
   ```
3. Upload to your device:
   ```bash
   pio run --target upload
   ```
4. Monitor serial output:
   ```bash
   pio device monitor
   ```

## Configuration

To enter configuration mode:
1. Hold the **BOOT button (GPIO 0)** while powering up or resetting.
2. Connect to the WiFi AP named `XIAO_S3_CONFIG`.
3. Navigate to `http://192.168.4.1` in your browser to access the configuration form.

## Documentation

Full documentation is built using Sphinx and the Furo theme.
To build it locally:
```bash
./venv/bin/sphinx-build -b html docs/source docs/build/html
```

## Testing

The project uses the Unity framework for both native and embedded testing.

- **Native Tests**: `pio test -e native`
- **Embedded Tests**: `pio test -e seeed_xiao_esp32s3`

## License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](LICENSE) file for details.
