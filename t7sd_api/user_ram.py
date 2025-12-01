# t7sd_api/user_ram.py

from __future__ import annotations
from labjack import ljm


class UserRAMInterface:
    """
    USER_RAM access helpers for all supported types.
    """

    def __init__(self, handle: int):
        self.handle = handle

    def read_f32(self, index: int) -> float:
        return ljm.eReadName(self.handle, f"USER_RAM{index}_F32")

    def write_f32(self, index: int, value: float):
        ljm.eWriteName(self.handle, f"USER_RAM{index}_F32", value)

    def read_i32(self, index: int) -> int:
        return int(ljm.eReadName(self.handle, f"USER_RAM{index}_I32"))

    def write_i32(self, index: int, value: int):
        ljm.eWriteName(self.handle, f"USER_RAM{index}_I32", value)

    def read_u32(self, index: int) -> int:
        return int(ljm.eReadName(self.handle, f"USER_RAM{index}_U32"))

    def write_u32(self, index: int, value: int):
        ljm.eWriteName(self.handle, f"USER_RAM{index}_U32", value)

    def read_u16(self, index: int) -> int:
        return int(ljm.eReadName(self.handle, f"USER_RAM{index}_U16"))

    def write_u16(self, index: int, value: int):
        ljm.eWriteName(self.handle, f"USER_RAM{index}_U16", value)
