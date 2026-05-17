# Astral Pool Viron eQuilibrium Chlorinator — pychlorinator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

This is a fork of [@pbutterworth](https://github.com/pbutterworth)'s [pychlorinator](https://github.com/pbutterworth/pychlorinator) library.

A Python BLE (Bluetooth Low Energy) library for controlling **Astral Pool Viron eQuilibrium** and **Halo** series pool chlorinators.

It is the foundation for the Home Assistant [Astral Pool Viron eQuilibrium Chlorinator](https://github.com/kesawi/astralpool_chlorinator) integration forked from [@pbutterworth](https://github.com/pbutterworth)'s [astralpool_chlorinator](https://github.com/pbutterworth/astralpool_chlorinator).

## Changes from upstream

All current changes have been merged into the upstream repository.

## Enabling debug logging

To log full coordinator data in Home Assistant, add to `configuration.yaml`:

```yaml
logger:
  logs:
    pychlorinator.chlorinator: debug
```

## Compatibility

- Tested on Viron EQ25
- Other Viron models should work but are untested
- Halo series: `halochlorinator.py` is unchanged from upstream

## Credits

- [@pbutterworth](https://github.com/pbutterworth) — original library and protocol reverse engineering

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

To install this fork directly:

```bash
pip install git+https://github.com/kesawi/pychlorinator@main
```

To install the upstream package from PyPI:

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

Contributions should be made to the upstream repository ([pbutterworth/pychlorinator](https://github.com/pbutterworth/pychlorinator))

## Related

- Original [@pbutterworth](https://github.com/pbutterworth)'s [astralpool_chlorinator](https://github.com/pbutterworth/astralpool_chlorinator) — Home Assistant custom integration that uses this library
- My forked [astralpool_chlorinator](https://github.com/kesawi/astralpool_chlorinator) — Home Assistant custom integration that uses this library

---

## License

MIT License — see [LICENSE](LICENSE) for details.