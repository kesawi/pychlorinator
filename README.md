# Astral Pool Viron eQuilibrium Chlorinator

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pychlorinator?style=for-the-badge&logo=python&logoColor=green)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/py3-pyhue?label=pychlorinator&logo=python&logoColor=green&style=for-the-badge)](https://pypi.org/project/pychlorinator/)
[![PyPi - Downloads](https://img.shields.io/pypi/dm/pychlorinator?label=Downloads&style=for-the-badge)](https://pypi.org/project/pychlorinator)


[![Buy Me A Coffee](https://img.buymeacoffee.com/button-api/?text=Buy%20me%20a%20coffee&emoji=&slug=pbutterworQ&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff)](https://www.buymeacoffee.com/pbutterworQ)


This library offers a BLE API for the Viron and Halo series of AstralPool chlorinators and can be used to remote control pool pump and the chlorinator operation.

It is the foundation for the HomeAssistant [Astral Pool Viron eQuilibrium Chlorinator](https://github.com/pbutterworth/astralpool_chlorinator) plugin.

## New in this PR

- `ChlorinatorSetupWrite` class — packs setup bytes for writing pH setpoint, chlorine output level and default manual speed
- `async_write_setup()` method on `ChlorinatorAPI` — writes pH setpoint, chlorine output and default manual speed to `UUID_CHLORINATOR_SETUP`
- `async_write_action()` extended with `period_minutes` parameter for `DisableAcidDosingForPeriod` action
- Unit tests for `ChlorinatorSetupWrite` round-trip verification
- Improved debug logging in `async_gatherdata()` — full coordinator data logged at debug level