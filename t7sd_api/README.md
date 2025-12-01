# t7sd_api – Python API for LabJack T7 / T7 Pro

`t7sd_api` is a modular library providing high-level access to:

- SD card I/O
- Modbus registers
- EF thermistor configuration
- USER_RAM memory
- Device lifecycle management

---

## 🔌 Connect to a Device

```python
from t7sd_api import LabJackSD
dev = LabJackSD.connect("192.168.1.4")
dev.close()
```

---

## 📂 SD API Example

```python
entries = dev.sd.list_dir("/")
data = dev.sd.read_file_bytes("RMBL_ALL.csv")
dev.sd.delete_file("old.csv")
```

---

## ⚙️ Modbus Example

```python
ain0 = dev.modbus.read("AIN0")
dev.modbus.write("DAC0", 2.5)
```

---

## 🌡️ EF Example

```python
dev.ef.configure_thermistor_SH(
    "AIN54",
    A=0.00335401643,
    B=0.000238083666,
    C=-0.00000856583758,
    D=0.0000248779044
)
temp = dev.ef.read_ef_value("AIN54")
```

---

## 💾 USER_RAM Example

```python
dev.user_ram.write_f32(0, 3.14)
print(dev.user_ram.read_f32(0))
```
