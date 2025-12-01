from __future__ import annotations

from .sd import SDEntry, DiskInfo, SDInterface
from .modbus import ModbusInterface
from .ef import EFInterface
from .user_ram import UserRAMInterface
from .connection import LabJackDevice

# Backwards-compatible alias
LabJackSD = LabJackDevice

__all__ = [
    "LabJackDevice",
    "LabJackSD",
    "SDEntry",
    "DiskInfo",
    "SDInterface",
    "ModbusInterface",
    "EFInterface",
    "UserRAMInterface",
]
