# pychlorinator

[![PyPI - Version](https://img.shields.io/pypi/v/pychlorinator?style=for-the-badge&logo=python&logoColor=green)](https://pypi.org/project/pychlorinator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pychlorinator?style=for-the-badge&logo=python&logoColor=green)](https://python.org)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pychlorinator?label=Downloads&style=for-the-badge)](https://pypi.org/project/pychlorinator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

A Python BLE (Bluetooth Low Energy) library for controlling **Astral Pool Viron eQuilibrium** and **Halo** series pool chlorinators.

It is the foundation for the Home Assistant [Astral Pool Viron eQuilibrium Chlorinator](https://github.com/pbutterworth/astralpool_chlorinator) integration.

[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=pbutterworQ&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/pbutterworQ)

---

## Features

### Viron / eQuilibrium

- Read current device state: operating mode, pump speed, pH, chlorine, ORP
- Control pump: off, auto, manual, low / medium / high speed
- Switch between pool and spa modes
- Write pH setpoint, chlorine output level, and default manual speed
- Acid dosing: disable indefinitely or for a set period
- Read timers (4 schedules), statistics, and device capabilities

### Halo

- All of the above, plus:
- Temperature monitoring (board, water, heater, solar)
- Heater and solar panel control
- Multi-zone lighting control (on/off, auto, colour, sync)
- Equipment mode control: filter pump, GPO, valves, relays
- Maintenance task tracking

---

## Requirements

- Python 3.8+
- Bluetooth adapter accessible from the host machine
- [`bleak`](https://github.com/hbldh/bleak) — BLE client
- [`bleak-retry-connector`](https://github.com/Bluetooth-Devices/bleak-retry-connector) — reliable connection handling
- [`pycryptodome`](https://pycryptodome.readthedocs.io/) — AES-128 encryption (used by the device protocol)

---

## Installation

```bash
pip install pychlorinator
```

---

## Usage

### Viron / eQuilibrium Chlorinator

```python
import asyncio
from bleak import BleakScanner
from pychlorinator.chlorinator import ChlorinatorAPI

async def main():
    # Discover the device by name or address
    device = await BleakScanner.find_device_by_name("Viron")

    api = ChlorinatorAPI(ble_device=device, access_code="1234")

    # Read all state from the device
    data = await api.async_gatherdata()

    print(f"Mode:        {data['state'].mode}")
    print(f"Pump speed:  {data['state'].speed}")
    print(f"pH:          {data['state'].ph}")
    print(f"Chlorine:    {data['state'].chlorine}")
    print(f"ORP:         {data['state'].orp}")

asyncio.run(main())
```

#### Sending commands

```python
from pychlorinator.chlorinator_parsers import ChlorinatorActions

# Turn pump on in auto mode
await api.async_write_action(ChlorinatorActions.Auto)

# Switch to spa mode
await api.async_write_action(ChlorinatorActions.Spa)

# Disable acid dosing for 30 minutes
await api.async_write_action(
    ChlorinatorActions.DisableAcidDosingForPeriod,
    period_minutes=30,
)

# Update setpoints
await api.async_write_setup(ph_setpoint=7.4, chlorine_setpoint=60)
```

### Halo Chlorinator

```python
import asyncio
from bleak import BleakScanner
from pychlorinator.halochlorinator import HaloChlorinatorAPI

async def main():
    device = await BleakScanner.find_device_by_name("Halo")

    api = HaloChlorinatorAPI(ble_device=device, access_code="1234")
    data = await api.async_gatherdata()

    print(f"Water temp:  {data['temp'].water_temperature}")
    print(f"Solar temp:  {data['temp'].solar_roof_temperature}")

asyncio.run(main())
```

---

## API Reference

### `ChlorinatorAPI`

| Method | Description |
|---|---|
| `async_gatherdata()` | Reads all device state, setup, capabilities, timers, and statistics. Returns a dict of parsed characteristic objects. |
| `async_write_action(action, period_minutes=None)` | Sends a control command. `period_minutes` is used with `DisableAcidDosingForPeriod`. |
| `async_write_setup(ph_setpoint, chlorine_setpoint, default_speed)` | Writes pH setpoint, chlorine output level, and default manual speed. |

### `ChlorinatorActions`

| Action | Description |
|---|---|
| `Off` | Turn pump off |
| `Auto` | Auto mode |
| `Manual` | Manual mode at default speed |
| `Low` / `Medium` / `High` | Manual mode at specific speed |
| `Pool` / `Spa` | Switch between pool and spa |
| `DisableAcidDosingIndefinitely` | Pause acid dosing |
| `DisableAcidDosingForPeriod` | Pause acid dosing for `period_minutes` |
| `ResetStatistics` | Clear historical statistics |
| `TriggerCellReversal` | Manually trigger cell reversal |
| `DismissInfoMessage` | Dismiss active info/warning message |

### `HaloChlorinatorAPI`

`HaloChlorinatorAPI` exposes the same `async_gatherdata()` interface and also accepts action commands via the `ChlorinatorActions`, `HeaterAppActions`, `SolarAppActions`, and `LightAppActions` enums defined in `halo_parsers`.

---

## Data Objects

`async_gatherdata()` returns a dictionary whose values are parsed dataclass-style objects. Key entries:

| Key | Type | Contents |
|---|---|---|
| `state` | `ChlorinatorState` | Mode, speed, pH, chlorine, ORP, timer info, info messages |
| `setup` | `ChlorinatorSetup` | pH and chlorine setpoints, default speed |
| `capabilities` | `ChlorinatorCapabilities` | Min/max limits for pH and chlorine |
| `timers` | `ChlorinatorTimers` | Four pump timer schedules |
| `statistics` | `ChlorinatorStatistics` | pH/ORP min/max, cell reversals, running time, salt level |
| `settings` | `ChlorinatorSettings` | Acid dosing inhibit status and remaining time |
| `temp` *(Halo)* | `TempCharacteristic` | Board, water, heater, and solar temperatures |
| `equipment` *(Halo)* | `EquipmentModeCharacteristic` | Pump, GPO, valve, and relay modes |
| `lights` *(Halo)* | `LightStateCharacteristic` | Lighting zone state and colour |

---

## Contributing

Contributions are welcome. Please open an issue to discuss significant changes before submitting a pull request.

```bash
# Install dev dependencies
pip install poetry
poetry install

# Run pre-commit hooks
pre-commit install
pre-commit run --all-files

# Run tests
python -m pytest
```

---

## Related

- [astralpool_chlorinator](https://github.com/pbutterworth/astralpool_chlorinator) — Home Assistant custom integration that uses this library

---

## License

MIT License — see [LICENSE](LICENSE) for details.
