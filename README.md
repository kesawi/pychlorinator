# Astral Pool Viron eQuilibrium Chlorinator — pychlorinator

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pychlorinator?style=for-the-badge&logo=python&logoColor=green)](https://python.org)

This is a fork of [@pbutterworth](https://github.com/pbutterworth)'s [pychlorinator](https://github.com/pbutterworth/pychlorinator) library, extended with write support for the Viron eQuilibrium chlorinator setup characteristic.

## Changes from upstream

- `ChlorinatorSetupWrite` class — packs setup bytes for writing pH setpoint, chlorine output level and default manual speed back to the device
- `async_write_setup()` method on `ChlorinatorAPI` — writes pH setpoint, chlorine output and/or default manual speed to `UUID_CHLORINATOR_SETUP`
- `async_write_action()` extended with `period_minutes` parameter for `DisableAcidDosingForPeriod` action
- Improved debug logging in `async_gatherdata()` — full coordinator data logged at debug level when `pychlorinator.chlorinator` debug logging enabled
- Unit tests for `ChlorinatorSetupWrite` round-trip verification

## About

This library offers a BLE API for the Viron series of AstralPool chlorinators and can be used to remote control pool pump and the chlorinator operation.

It is the foundation for the HomeAssistant [Astral Pool Viron eQuilibrium Chlorinator](https://github.com/kesawi/astralpool_chlorinator) plugin.

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