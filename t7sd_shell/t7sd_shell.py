"""
Modular refactored shell using new t7sd_api package.
"""

import argparse
from t7sd_api import LabJackSD
from t7sd_shell.command_registry import CommandRegistry
from t7sd_shell.completer import ShellCompleter
from t7sd_shell.sd_cache import SDCache   

from t7sd_shell.commands.sd_commands import register_sd_commands
from t7sd_shell.commands.modbus_commands import register_modbus_commands
from t7sd_shell.commands.ef_commands import register_ef_commands
from t7sd_shell.commands.user_ram_commands import register_user_ram_commands
from t7sd_shell.commands.system_commands import register_system_commands


# ----------------------
# Tab Completion Support (Windows-safe)
# ----------------------
try:
    import readline  # works on macOS/Linux or pyreadline3 on Windows
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None
        print("[WARN] Readline/pyreadline3 not available. Tab completion disabled.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--identifier", default="ANY")
    args = parser.parse_args()

    
    # Build registry
    registry = CommandRegistry()
    register_sd_commands(registry)
    register_modbus_commands(registry)
    register_ef_commands(registry)
    register_user_ram_commands(registry)
    register_system_commands(registry)

    dev = LabJackSD.connect(identifier=args.identifier)

    # Load SD cache
    sd_cache = SDCache(dev)

    # Make registry aware of register names
    registry.register_names = ["AIN0", "AIN1", "DAC0", "DAC1", "FIO0", ...]  # TODO populate properly

    # Enable tab completion
    if readline is not None:
        completer = ShellCompleter(registry, dev, sd_cache)
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")

    dev = LabJackSD.connect(identifier=args.identifier)

    while True:
        try:
            line = input("t7sd> ").strip()
            registry.dispatch(dev, line)
        except SystemExit:
            break
        except Exception as e:
            print("Error:", e)

    dev.close()


if __name__ == "__main__":
    main()
