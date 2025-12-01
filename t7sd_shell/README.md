# t7sd_shell – Interactive Shell & Batch Tool for LabJack T7 / T7 Pro

`t7sd_shell` provides an interactive, command-driven interface for navigating
the SD card, reading/writing Modbus registers, configuring EF (Extended
Features) such as Steinhart–Hart thermistors, and interacting with USER_RAM
memory on LabJack T7 devices.

It also includes a **batch mode** that can execute a list of commands on
multiple devices in parallel, with per-device logging and `$DEVICE` variable
substitution.

---

## 🔧 Installation & Setup

Project structure should look like:

```
project/
  t7sd_api/
  t7sd_shell/
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the shell from project root:

```
python -m t7sd_shell.t7sd_shell --identifier <IP or ANY>
```

Example:

```
python -m t7sd_shell.t7sd_shell --identifier 192.168.1.4
```

This opens the interactive prompt:

```
t7sd>
```

---

## 📂 SD Card Commands

| Command | Description |
|--------|-------------|
| `ls [path]` | List directory contents |
| `cd <path>` | Change SD working directory |
| `pwd` | Show current SD directory |
| `cat <path>` | Display a file's contents |
| `get <remote> <local>` | Download a file |
| `rm <path>` | Delete a file |
| `info` | Show SD card statistics |

---

## ⚡ Modbus Command Example

```
read AIN0
write DAC0 2.5
```

---

## 🌡️ EF Commands Example

```
ef-read AIN54
ef-set AIN54 A=0.003354 B=0.000238 C=-0.0000085 D=0.0000249
```

---

## 💾 USER_RAM Commands Example

```
user-ram-read F32 0
user-ram-write U32 10 123
```

---

## 🧠 Tab Completion

Supports:
- command names
- SD paths
- registers (if provided)

---

## 📦 Batch Mode

Run commands on multiple devices:

```
python -m t7sd_shell.batch     --devices devices.txt     --commands commands.txt     --parallel 5     --log-dir logs     --stop-on-error
```

Example `devices.txt`:

```
192.168.1.4
192.168.1.5
192.168.1.7
```

Example `commands.txt`:

```
pwd
info
read AIN0
ef-read AIN54
user-ram-read F32 0
get RMBL_ALL.csv download/$DEVICE.csv
```

---