from __future__ import annotations
from typing import Tuple

from labjack import ljm

from .sd import SDInterface
from .modbus import ModbusInterface
from .ef import EFInterface
from .user_ram import UserRAMInterface


class LabJackDevice:
    """
    High-level T7/T7 Pro device wrapper with sub-interfaces.
    """

    def __init__(self, handle: int, info_tuple: Tuple[int, int, int, int, int, int]):
        self.handle = handle
        self.info_tuple = info_tuple

        # Subsystems
        self.sd = SDInterface(handle)
        self.modbus = ModbusInterface(handle)
        self.ef = EFInterface(self.modbus)
        self.user_ram = UserRAMInterface(handle)

    # ---- lifecycle ---- #

    @classmethod
    def connect(
        cls,
        identifier: str = "ANY",
        device_type: str = "T7",
        connection: str = "ANY",
        quiet: bool = True,
    ) -> "LabJackDevice":
        handle = ljm.openS(device_type, connection, identifier)
        info = ljm.getHandleInfo(handle)

        if info[0] in (ljm.constants.dtT4, ljm.constants.dtT8):
            ljm.close(handle)
            raise RuntimeError(f"T{info[0]} does not support an SD card.")

        if not quiet:
            ip_str = ljm.numberToIP(info[3])
            print(
                f"Opened LabJack: devType={info[0]}, connType={info[1]}, "
                f"serial={info[2]}, ip={ip_str}, port={info[4]}, maxBytesPerMB={info[5]}"
            )

        dev = cls(handle, info)
        dev.identifier = identifier
        return dev

    def close(self):
        if self.handle is not None:
            ljm.close(self.handle)
            self.handle = None

    # ---- compatibility helpers (so existing code doesn't break) ---- #

    # SD
    def get_cwd(self) -> str:
        return self.sd.get_cwd()

    def chdir(self, path: str):
        return self.sd.chdir(path)

    def list_dir(self, path: str = None):
        return self.sd.list_dir(path)

    def read_file_bytes(self, sd_path: str) -> bytes:
        return self.sd.read_file_bytes(sd_path)

    def read_file_text(self, sd_path: str, encoding="utf-8", errors="replace") -> str:
        return self.sd.read_file_text(sd_path, encoding, errors)

    def delete_file(self, sd_path: str):
        return self.sd.delete_file(sd_path)

    def get_disk_info(self):
        return self.sd.get_disk_info()

    # Modbus
    def read_reg(self, name: str) -> float:
        return self.modbus.read(name)

    def write_reg(self, name: str, value: float):
        return self.modbus.write(name, value)

    # EF
    def configure_thermistor_SH(self, ain: str, A: float, B: float, C: float, D: float):
        return self.ef.configure_thermistor_SH(ain, A, B, C, D)

    def read_ef_value(self, ain: str) -> float:
        return self.ef.read_ef_value(ain)

    # USER_RAM
    def read_user_ram_f32(self, index: int) -> float:
        return self.user_ram.read_f32(index)

    def write_user_ram_f32(self, index: int, value: float):
        return self.user_ram.write_f32(index, value)

    def read_user_ram_i32(self, index: int) -> int:
        return self.user_ram.read_i32(index)

    def write_user_ram_i32(self, index: int, value: int):
        return self.user_ram.write_i32(index, value)

    def read_user_ram_u32(self, index: int) -> int:
        return self.user_ram.read_u32(index)

    def write_user_ram_u32(self, index: int, value: int):
        return self.user_ram.write_u32(index, value)

    def read_user_ram_u16(self, index: int) -> int:
        return self.user_ram.read_u16(index)

    def write_user_ram_u16(self, index: int, value: int):
        return self.user_ram.write_u16(index, value)
