# t7sd_api/ef.py

from __future__ import annotations

from .modbus import ModbusInterface


class EFInterface:
    """
    EF helper for Steinhart-Hart thermistors, etc.
    """

    def __init__(self, modbus: ModbusInterface):
        self.modbus = modbus

    def configure_thermistor_SH(self, ain: str, A: float, B: float, C: float, D: float):
        prefix = f"{ain}_EF_"

        # Enable SH EF (EF index 50)
        self.modbus.write(prefix + "INDEX", 50)

        # Fixed EF settings (same as your Lua/script)
        self.modbus.write(prefix + "CONFIG_A", 1)      # excitation settings
        self.modbus.write(prefix + "CONFIG_B", 4)      # differential mode
        self.modbus.write(prefix + "CONFIG_D", 5)      # negative channel/divider
        self.modbus.write(prefix + "CONFIG_E", 10000)  # pull-up ohms
        self.modbus.write(prefix + "CONFIG_F", 10000)  # pull-down ohms

        # SH coefficients
        self.modbus.write(prefix + "CONFIG_G", A)
        self.modbus.write(prefix + "CONFIG_H", B)
        self.modbus.write(prefix + "CONFIG_I", C)
        self.modbus.write(prefix + "CONFIG_J", D)

    def read_ef_value(self, ain: str) -> float:
        name = f"{ain}_EF_READ_A"
        return self.modbus.read(name)
