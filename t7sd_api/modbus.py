# t7sd_api/modbus.py

from __future__ import annotations
from labjack import ljm


class ModbusInterface:
    """
    Simple Modbus read/write interface bound to a device handle.
    """

    def __init__(self, handle: int):
        self.handle = handle

    def read(self, name: str) -> float:
        return ljm.eReadName(self.handle, name)

    def write(self, name: str, value: float):
        ljm.eWriteName(self.handle, name, value)
