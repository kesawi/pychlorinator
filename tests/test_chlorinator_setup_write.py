"""Tests for ChlorinatorSetupWrite"""

from pychlorinator.chlorinator_parsers import (
    ChlorinatorSetup,
    ChlorinatorSetupWrite,
    SpeedLevels,
)


def make_setup_bytes(speed: int, ph: int, chlorine: int, flags: int) -> bytes:
    """Helper to create raw setup bytes matching the @BBHB struct format"""
    import struct
    return struct.pack("@BBHB", speed, ph, chlorine, flags) + bytes(16)  # pad to 20 bytes


def test_roundtrip_ph_setpoint():
    """Test that writing and reading pH setpoint round-trips correctly"""
    # Simulate current device state: speed=Medium, pH=8.0, chlorine=650, flags=0
    raw = make_setup_bytes(speed=1, ph=80, chlorine=650, flags=0)
    current = ChlorinatorSetup(raw)

    assert current.ph_control_setpoint == 8.0
    assert current.chlorine_control_setpoint == 650
    assert current.default_manual_on_speed == SpeedLevels.Medium

    # Write new pH setpoint of 7.4
    write = ChlorinatorSetupWrite(
        default_manual_on_speed=current.default_manual_on_speed,
        ph_control_setpoint=7.4,
        chlorine_control_setpoint=current.chlorine_control_setpoint,
        flags=current.flags,
    )

    # Read back the packed bytes
    result = ChlorinatorSetup(bytes(write) + bytes(16))
    assert result.ph_control_setpoint == 7.4
    assert result.chlorine_control_setpoint == 650
    assert result.default_manual_on_speed == SpeedLevels.Medium


def test_roundtrip_chlorine_setpoint():
    """Test that writing and reading chlorine setpoint round-trips correctly"""
    raw = make_setup_bytes(speed=1, ph=72, chlorine=650, flags=0)
    current = ChlorinatorSetup(raw)

    write = ChlorinatorSetupWrite(
        default_manual_on_speed=current.default_manual_on_speed,
        ph_control_setpoint=current.ph_control_setpoint,
        chlorine_control_setpoint=5,
        flags=current.flags,
    )

    result = ChlorinatorSetup(bytes(write) + bytes(16))
    assert result.chlorine_control_setpoint == 5
    assert result.ph_control_setpoint == 7.2


def test_preserves_unchanged_values():
    """Test that only the target value changes, others are preserved"""
    raw = make_setup_bytes(speed=2, ph=75, chlorine=700, flags=3)
    current = ChlorinatorSetup(raw)

    write = ChlorinatorSetupWrite(
        default_manual_on_speed=current.default_manual_on_speed,
        ph_control_setpoint=7.2,
        chlorine_control_setpoint=current.chlorine_control_setpoint,
        flags=current.flags,
    )

    result = ChlorinatorSetup(bytes(write) + bytes(16))
    assert result.ph_control_setpoint == 7.2
    assert result.chlorine_control_setpoint == 700
    assert result.default_manual_on_speed == SpeedLevels.High
    assert result.flags == 3
