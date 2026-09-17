# Project Development Guidelines — mag-xiao-s3 (PlatformIO / Seeed XIAO ESP32S3)

This project targets the Seeed XIAO ESP32S3 board using the Arduino framework under PlatformIO.
The notes below capture project-specific build, testing, and development practices that have been verified in this repo.

## 1) Build and Configuration

- Tooling
  - PlatformIO CLI (`pio`) or VS Code + PlatformIO extension.
  - Board environment is defined in `platformio.ini` as `[env:seeed_xiao_esp32s3]`:
    ```ini
    [env:seeed_xiao_esp32s3]
    platform = espressif32
    board = seeed_xiao_esp32s3
    framework = arduino
    ```

- Common commands
  - Build firmware for the board:
    ```bash
    pio run -e seeed_xiao_esp32s3
    ```
  - Upload to the board (auto-detects port on most systems):
    ```bash
    pio run -e seeed_xiao_esp32s3 -t upload
    ```
  - Open serial monitor (adjust baud to your sketch; 115200 is typical):
    ```bash
    pio device monitor -b 115200
    ```

- USB/Upload tips for XIAO ESP32S3
  - If the upload port is not detected, double-tap the reset button to enter the bootloader, then retry upload.
  - On Linux, ensure your user is in the `dialout` group and udev rules permit access to `/dev/ttyACM*` or `/dev/ttyUSB*`.
  - If you rely on native USB CDC early in boot on ESP32-S3, you may add (optional) build flags:
    ```ini
    build_flags =
      -DARDUINO_USB_MODE=1
      -DARDUINO_USB_CDC_ON_BOOT=1
    ```
    Only add these if you actually need CDC active from reset; otherwise, keep `platformio.ini` minimal.

- Project layout
  - `src/` contains Arduino entry points (`setup()`, `loop()`).
  - `include/` for public headers shared across modules.
  - `lib/` for reusable libraries (if a module becomes substantial, promote it here).

## 2) Testing

This repo is configured to support PlatformIO Unit Testing with a host-native environment, so you can run fast tests without hardware.

- Environments for tests
  - A host-native test environment is defined in `platformio.ini`:
    ```ini
    [env:native]
    platform = native
    test_build_src = no
    ```
    - `platform = native` builds and runs tests on your host machine.
    - `test_build_src = no` avoids pulling Arduino `src/` into host tests (prevents Arduino/ESP32 headers from being required).

- Running tests (host)
  - Run all tests for the native env:
    ```bash
    pio test -e native
    ```
  - This will build the Unity framework automatically and execute tests under `test/`.

- Writing tests
  - Place tests under `test/<suite_name>/`. Each suite may contain one or more `*.cpp` files.
  - For host-native tests, avoid Arduino-specific headers; keep logic in plain C/C++ so it compiles without the Arduino core.
  - Suggested pattern: extract business logic into `.h/.cpp` under `include/` and `lib/` so it’s unit-testable on host, while `src/main.cpp` stays as the Arduino integration layer.

- Example (verified)
  - The following Unity test was used to validate the setup locally:
    ```cpp
    #include <unity.h>

    void setUp(void) {}
    void tearDown(void) {}

    static void test_addition(void) {
        TEST_ASSERT_EQUAL_INT(4, 2 + 2);
    }

    int main(int, char**) {
        UNITY_BEGIN();
        RUN_TEST(test_addition);
        return UNITY_END();
    }
    ```
  - Place it at `test/test_native/test_main.cpp`, then run:
    ```bash
    pio test -e native
    ```
  - Expected output includes a PASSED status for the test case.

- Hardware-in-the-loop tests (optional)
  - PlatformIO also supports running tests on-device (serial/USB). If you need that:
    - Keep Arduino-specific tests under `test/` and run with:
      ```bash
      pio test -e seeed_xiao_esp32s3
      ```
    - You may need to expose test entry points via Arduino `setup()` wrappers; see PlatformIO docs for on-device Unity tests.

## 3) Code Style and Development Notes

- Language level
  - C++ (Arduino framework on ESP32). Prefer standard C++ where possible; keep Arduino dependencies at the boundary.

- Structure & testability
  - Keep `src/main.cpp` thin (board setup, wiring, loop). Put unit-testable logic into separate `.cpp/.h` under `lib/` or `include/`.
  - For logic that must use Arduino APIs, consider small adapter interfaces so core logic remains testable on the host.

- Logging & diagnostics
  - For quick logs, use `Serial.printf` and ensure the monitor baud matches sketch configuration.
  - For more advanced logging on ESP32, you can include `esp_log.h` and use `ESP_LOGI/W/E` macros. Be mindful of binary size and log levels.

- Common pitfalls
  - Mixing Arduino-only headers in host-native tests will fail to compile. Use `test_build_src = no` and keep host tests Arduino-free.
  - Inconsistent baud rates between sketch and monitor lead to garbage output; standardize on 115200 unless you have strict timing reasons.
  - If uploads intermittently fail, try entering bootloader (double-tap reset) and/or specify the upload port in `platformio.ini` using `upload_port`.

## 4) Useful Commands Cheatsheet

- Build for board:
  ```bash
  pio run -e seeed_xiao_esp32s3
  ```
- Upload to board:
  ```bash
  pio run -e seeed_xiao_esp32s3 -t upload
  ```
- Serial monitor at 115200:
  ```bash
  pio device monitor -b 115200
  ```
- Run unit tests on host (native):
  ```bash
  pio test -e native
  ```

## 5) Maintenance

- `platformio.ini` keeps environments minimal. Extend with care; prefer per-environment flags.
- If you add substantial modules, move them into `lib/` with their own unit tests.
- Prefer small, composable units of logic to keep both firmware and tests fast and clear.
