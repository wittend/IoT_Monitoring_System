### Project Guidelines for XIAO ESP32S3 Edge Data Collector

This project uses **PlatformIO** with the **ESP-IDF** framework to develop firmware for the Seeed Studio XIAO ESP32S3 module.

#### 1. Build and Configuration Instructions

- **Prerequisites**: [PlatformIO Core](https://docs.platformio.org/en/latest/core/index.html) must be installed.
- **Build**: Run the following command from the project root:
  ```bash
  pio run
  ```
- **Documentation**: To build the HTML documentation:
  ```bash
  ./venv/bin/sphinx-build -b html docs/source docs/build/html
  ```
- **Upload**: Connect the XIAO ESP32S3 and run:
  ```bash
  pio run --target upload
  ```
- **Serial Monitor**: To view logs over USB:
  ```bash
  pio device monitor
  ```
- **SDK Configuration**: ESP-IDF settings are managed via `sdkconfig.seeed_xiao_esp32s3`. For interactive configuration, use:
  ```bash
  pio run -t menuconfig
  ```

#### 2. Testing Information

This project supports both host-side (native) and on-device (embedded) testing using the [Unity](http://www.throwtheswitch.org/unity) framework.

- **Native Tests**: Unit tests that do not depend on ESP32 hardware. These run on your development machine.
  ```bash
  pio test -e native
  ```
- **Embedded Tests**: Tests that run on the actual XIAO ESP32S3 hardware.
  ```bash
  pio test -e seeed_xiao_esp32s3
  ```
- **Adding New Tests**:
  1. Create a new file in the `test/` directory (e.g., `test/test_logic.c`).
  2. For native tests, ensure they use standard C and do not include ESP-IDF specific headers (or use mocks).
  3. Example structure:
     ```c
     #include <unity.h>
     
     void test_example(void) {
         TEST_ASSERT_EQUAL(1, 1);
     }
     
     int main(int argc, char **argv) {
         UNITY_BEGIN();
         RUN_TEST(test_example);
         return UNITY_END();
     }
     ```

#### 3. Additional Development Information

- **Framework**: ESP-IDF (v5.x).
- **Code Style**: Follow the [ESP-IDF Style Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/contribute/style-guide.html).
- **Hardware Specifications**:
  - **Module**: Seeed Studio XIAO ESP32S3.
  - **Sensors**: 
    - RM3100 (Magnetometer) via I2C.
    - MCP9808 (Temperature) via I2C.
    - L76K (GNSS) via UART.
    - SX1262 (LoRa) via SPI.
- **Data Format**: Sensors are sampled at 1Hz and data is output as JSONL:
  `{"ts":"DD Mon YYYY HH:MM:SS", "rt": 25.000, "x":12345.678, "y":-234.500, "z":987.001}`
- **Key Files**:
  - `src/main.c`: Application entry point (`app_main`) and main task logic.
  - `lib/`: Contains driver implementations for RM3100, MCP9808, SX1262, and GNSS.
  - `platformio.ini`: Project configuration and environments.
  - `docs/`: Sphinx documentation sources and build outputs.
- **Configuration Mode**: To enter configuration mode, hold the BOOT button (GPIO 0) during power-up or reset. The device will start a WiFi AP named `XIAO_S3_CONFIG`. Connect and navigate to `http://192.168.4.1` to access the configuration form.
- **Power Management**: Designed for battery operation (LiPO/LiFePO) with solar charging support.
