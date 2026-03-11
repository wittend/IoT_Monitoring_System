# Maintenance — mag-xiao-s3 (PlatformIO / Seeed XIAO ESP32S3)

This document describes how to keep PlatformIO Core, platforms, frameworks, and libraries up to date while maintaining a balanced approach between freshness and stability.

- Project board: Seeed XIAO ESP32S3
- Build system: PlatformIO (CLI and/or VS Code PlatformIO IDE)
- Language/Framework: Arduino on ESP32-S3

## Philosophy: Balanced Updates

We favor safe, routine updates that pull in bug fixes and minor improvements without risking large breaking changes.

- Platform policy: keep `platform = espressif32` unpinned to track the latest stable platform release.
- Library policy: use libraries stored in the `vendor/` directory, managed via `lib_extra_dirs = vendor`.
- Testing: run host-native unit tests and a firmware build after updates.

If a breaking change slips in, temporarily pin the platform to the last known good version until it’s resolved.

## Quick Checklist (run from project root)

```bash
# 1) Update PlatformIO Core (stable)
pio upgrade            # ensures Core is latest stable
pio --version          # verify Core version

# 2) Update platforms, toolchains, frameworks, libs
pio update             # updates packages for all environments
pio system prune -f    # optional: clean unused caches/packages

# 3) Verify and build
pio run -e seeed_xiao_esp32s3  # build firmware for the board
pio test -e native             # run host-native unit tests
```

## PlatformIO Core: Installation-specific notes

Use the command that matches how you installed PlatformIO:

- pipx (recommended):
  ```bash
  pipx upgrade platformio
  pio upgrade
  pio --version
  ```
- pip:
  ```bash
  python3 -m pip install -U platformio
  pio upgrade
  pio --version
  ```
- Homebrew (macOS):
  ```bash
  brew update && brew upgrade platformio
  pio upgrade
  pio --version
  ```
- VS Code IDE: update the “PlatformIO IDE” extension from Marketplace, then verify in the built-in terminal with `pio --version`.

## Ensuring the Correct PIO Core Version

If `pio --version` reports an old version or you see warnings about multiple PIO Cores, ensure that the version installed via `pipx` (in `~/.local/bin`) takes precedence over older system-provided versions (like those in `/usr/bin` from APT).

1. Add `~/.local/bin` to the front of your `PATH`:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   ```
2. Verify:
   ```bash
   which pio
   # Expected: /home/dave/.local/bin/pio (or similar local path)
   ```

Notes:
- `pipx upgrade platformio` is the preferred way to keep the Core up to date.
- `pio upgrade` installs the latest stable Core (avoid `--dev` unless explicitly testing pre-releases).
- `pio system info` prints useful environment diagnostics.

## Project Dependency Updates

- Update PlatformIO platforms, frameworks, and toolchains:
  ```bash
  pio update
  ```
- Libraries are maintained in the `vendor/` directory. To update a library, replace its files in the `vendor/` directory with the new version.
- Show details for the ESP32 platform:
  ```bash
  pio platform show espressif32
  ```
- Update only platforms:
  ```bash
  pio platform update
  ```

## Verify Resolved Versions

- Dump the resolved environment configuration:
  ```bash
  pio run -e seeed_xiao_esp32s3 -t envdump
  ```
- List installed packages and libraries:
  ```bash
  pio pkg list --installed
  pio lib list
  ```

## Current Configuration in platformio.ini

- `platform = espressif32` (no explicit version): track latest stable platform.
- Libraries are located in the `vendor/` folder and included via `lib_extra_dirs`:

```ini
[env:seeed_xiao_esp32s3]
platform = espressif32
board = seeed_xiao_esp32s3
framework = arduino
lib_extra_dirs = vendor
lib_deps =
    wire
    ArduinoJson
    RadioLib
    ESPAsyncWebServer
    AsyncTCP
    TinyGPSPlus
    esp32time
```

If you encounter instability, you can temporarily pin the platform, for example:

```ini
platform = espressif32@~6.6.0  ; use the last known good minor series
```

## Troubleshooting & Tips

- Upload/USB (XIAO ESP32S3): If upload port isn’t detected after updates, double-tap reset to enter bootloader and retry. Ensure your user is in the `dialout` group on Linux.
- CDC on boot: If you rely on native USB CDC early in boot, keep these flags in `platformio.ini` (already present):
  ```ini
  build_flags =
    -DARDUINO_USB_MODE=1
    -DARDUINO_USB_CDC_ON_BOOT=1
  ```
- Dependency resolution issues: clear caches and retry updates/builds:
  ```bash
  pio system prune -f
  pio update
  pio run -e seeed_xiao_esp32s3
  ```
- Breakages after updates: 
  1) Pin the platform (`platform = espressif32@<version>`), 
  2) Open an issue with release notes/links, 
  3) Plan migration and unpin once fixed.

## Reference Commands Cheatsheet

```bash
# Build for board
pio run -e seeed_xiao_esp32s3

# Upload to board
pio run -e seeed_xiao_esp32s3 -t upload

# Serial monitor (115200)
pio device monitor -b 115200

# Run host-native unit tests
pio test -e native
```
