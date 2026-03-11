# Project Firmware Requirements for xiaoS3WSI2C Edge Data Collector (xiao-s3)

## 1. Overview
- Problem statement:
    * Create firmware for a Seeed Studio XIAO ESP32S3 Sense module to act as an IoT edge data collector for a small number of sensors. 
    * Its function will be to interrogate these sensors and relay the data to an aggregating network for relay to a central host.
    * It must use a low bandwidth radio frequency protocol such as LoRa for this transfer.
    * It must provide power management to maintain sufficient charge in battery storage (using LiPO, LiFePO, NaPO, SLA, etc.) from a small solar panel.
    * It must optionally support a small local GNSS receiver to maintain local time and provide PPS triggering of transmissions. 
   
## 2. Hardware
- Board: Seeed Studio XIAO ESP32S3 
- Example Sensors/ICs: 
    * PNI RM3100cb (magnetometer).
    * Microchip MCP9804/MCP9808 temperature sensor.
    * Seeed Studio L76K GPS/GNSS module for XIAO.
    * Seeed Studio Wio-SX1262 for XIAO (uses Semtech SX1262 module).
    * Soil moisture sensor (TBD).
  
- Power: (battery/USB), voltage(s)
    * Uing LiPO, LiFePO, NaPO, SLA, etc. battery.
    * 3.3 v operation.
    * Solar panel and conditioning as required.
    
- Wiring: diagram/photo + table (pin → signal)
  
- Buses: I2C/UART; target clock rates; pull-ups
    * I2C bus default timing.
    * UART (if required for GNSS) 115200 bps.
     
- Notes: level shifting, analog refs, shielding
    * not at present.

## Project Requirements
- This project must include an appropriate testing harness that allows addition of functional tests as new sensors and features are added.
- This project must create and maintain a set of documentation that is to be periodically updated to Read The Docs using the Sphinx documentation tool and the Furo style theme.

## 3. Functional Requirements
- REQ-001 [MUST]: sample sensors once per second and send data samples from RM3100, MCP9804/8 within that interval.
- REQ-002 [MUST]:  Use GNSS PPS signal to trigger sample transmission and acquisition cadence.
- REQ-003 [MUST]:  Data shall be sent as JSONL strings at a fixed cadence.
- REQ-004 [SHOULD]: Check GNSS at startup and 1/hour to set local real time clock to maintain timing accuracy.

## 4. Non-Functional Requirements
- Performance: sample rate 1 Hz
- Accuracy: ±(TBD) (units), stability (TBD)
- Power: avg (TBD) mA, sleep (tbd) mA
- Memory: max RAM (TBD) KB, flash (TBD) KB
- Startup time: < (TBD) ms to ready
- Reliability: watchdog, brown-out behavior
- Advertised RM3100-cb performance:
	* Sensitivity	13nT
	* Noise	15nT
	* Linearity over +/- 200 uT	0.50%
	* Field Measurement Range	+/- 1100 uT
	* Current @ 8Hz, 3 Axes	260 uA
	* Operating Temperature	-40°C to +85°C

## 5. Interfaces & Protocols
Baseline schema
{ "ts": "DD Mon YYYY HH:MM:SS", "rt": <float> "x": <float>, "y": <float>, ... }
- ts (string): UTC timestamp formatted like 25 Oct 2025 14:02:33 (RFC‑2822‑like time portion without timezone offset).
- rt (number): temperature (degrees C) of remote node.
- x, y, ... (number): Field components in appropriate units, with three (3) decimal places printed.

Example:

{ "ts":"26 Oct 2025 14:20:00", "rt": 25.000, "x":12345.678, "y":-234.500, "z":987.001 }

### 5.1 USB/Serial
- Baud: 115200 (or other)
  - Message format (JSONL over Websocket):
    - Example request:
      ```json
      {"cmd":"get_sample"}
      ```
    - Example response:
      ```json
{"ts":"DD Mon YYYY HH:MM:SS", "rt": NN.NNN, "x": NNN.NNN, "y": NNN.NNN, "z": NNN.NNN }
```
  
- Timeouts, retries, error codes

### 5.2 Other interfaces (BLE or Wi‑Fi)

- A Bluetooth Low Energy (BLE) [optionally WiFi] interface must be provided at initial startup to allow configuration of operational parameters, node identification, location (latitude, longitude, elevation) and owner, perhaps more.
- A button connected to a GPIO pin (TBD) allows the user to reset the device to configuration mode and causes it to present the HTML page that allows entry of configuration information.
- A mechanism to present output of sensor data and other messages over a benchtop interface such as USB serial for simple debugging and related purposes.  This mode must be configurable in the BLE/WiFi interface or using a command line argument at startup.

## 6. Data Processing & Algorithms
- (TBD)

## 7. User Interaction
- HTML Form configuration interface:
    * node identification 
    * location (latitude, longitude, elevation) 
    * owner
    * orientation
    * LoRa signal parameters
    
- after initial boot or button reset the system presents the configuration HTML page to allow input of operating parameters.

## 8. Calibration & Test Procedures
- Procedure steps (with timings) (TBD)
- Acceptance thresholds (TBD)

## 9. Validation & Acceptance Criteria
- ACC-001 validates REQ-001: method, tool, threshold (TBD)
- ACC-002 validates REQ-___: … (TBD)

## 10. Operating Conditions
- Temperature range: 40 Degrees C to 45 degrees C (depending on battery subsystem) 
- Magnetic environment < 1 mT

## 11. Risks & Constraints
- Library dependencies (with versions)
- PlatformIO: version, espressif32 platform version (current)
- Arduino‑ESP32 core version (current)
- USB CDC on boot needed? (`ARDUINO_USB_MODE=1`, `ARDUINO_USB_CDC_ON_BOOT=1`) Yes

## 12. Deliverables
- Firmware binary (.pio/build/seeed_xiao_esp32s3/firmware.bin)
- Source code structure
  * seperete code modules for each sensor used.
  * seperete code modules for major operational code component.
- Test results : on-device
- User guide / quickstart

## Local sources for device pinouts and schematics:
- docs/xiao-s3-schematic.pdf
- ![SX1262 LoRa module](../planning/Seeed%20Wio-SX1262.png)
- ![XIAO ESP32S3 Pinout](../planning/Seeed%20XIAO-ESPS3plus_pinout.png)

## 13. References
- data concerning reading RM3100 registers is contained in src/rm3100.h
- example arduino code for reading the RM3100 device: docs/RM3100_Arduino_I2C.ino.txt
- data concerning reading MCP9804/8 registers is contained in src/MCP9808.h
- MCP9808 Temperature Sensor datasheet: https://ww1.microchip.com/downloads/en/DeviceDoc/MCP9808-0.5C-Maximum-Accuracy-Digital-Temperature-Sensor-Data-Sheet-DS20005095B.pdf
- ESP32S3 XIAO Pinouts: https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/
- ESP32S3 WiFi information: https://wiki.seeedstudio.com/xiao_esp32s3_wifi_usage/
- ESP32S3 Bluetooth LE information: https://wiki.seeedstudio.com/xiao_esp32s3_bluetooth/
- LoRa Wio-sx1262 module: https://wiki.seeedstudio.com/wio_sx1262/
- Seeed L76k GNSS board for XAIO: https://wiki.seeedstudio.com/get_start_l76k_gnss/#hardware-overview

