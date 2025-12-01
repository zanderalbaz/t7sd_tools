import argparse
import shlex
import os
import sys
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from t7sd_api import LabJackSD

from t7sd_shell.command_registry import CommandRegistry
from t7sd_shell.commands.sd_commands import register_sd_commands
from t7sd_shell.commands.modbus_commands import register_modbus_commands
from t7sd_shell.commands.ef_commands import register_ef_commands
from t7sd_shell.commands.user_ram_commands import register_user_ram_commands
from t7sd_shell.commands.system_commands import register_system_commands

# -------------------------------------------------------
# Utility: corrects the path for directories.
# -------------------------------------------------------
def add_trailing_slash_os(path):
    if not path.endswith(os.sep):
        path += os.sep
    return path

# -------------------------------------------------------
# Utility: load lines from a file (skipping blanks + #)
# -------------------------------------------------------
def load_lines(path):
    with open(path, "r") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            yield stripped


# -------------------------------------------------------
# Connect helper
# -------------------------------------------------------
def connect_device(identifier):
    try:
        return LabJackSD.connect(identifier=identifier, quiet=True)
    except Exception as e:
        print(f"❌ Could not connect to {identifier}: {e}")
        return None


# -------------------------------------------------------
# Single device execution
# -------------------------------------------------------
def run_commands_on_device(identifier, commands, registry, log_dir=None, stop_on_error=False):
    """
    Executes a list of commands on a single device.
    Returns True if all succeeded, False otherwise.
    """
    dev = connect_device(identifier)
    if dev is None:
        return False

    # per-device logger
    log_path = None
    log_file = None

    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
        log_dir = add_trailing_slash_os(log_dir)
        log_path = os.path.join(log_dir, f"{identifier}.log")
        log_file = open(log_path, "a", encoding="utf-8")

        def log(msg):
            now = datetime.now()
            formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S')
            print(formatted_datetime, msg)
            log_file.write(formatted_datetime + " " + msg + "\n")
        print(f"=== DEVICE {identifier} START ===")
        log_file.write(f"=== DEVICE {identifier} START ===\n")
    else:
        log = print

    success = True

    for line in commands:
        # variable substitution
        line_resolved = line.replace("$DEVICE", identifier)

        log(f" -> {line_resolved}")

        # parse command + args
        try:
            parts = shlex.split(line_resolved)
        except Exception as e:
            log(f"Parse error: {e}")
            if stop_on_error:
                success = False
                break
            else:
                continue

        if not parts:
            continue

        cmd, *args = parts

        if cmd not in registry.commands:
            log(f"Unknown command '{cmd}'")
            if stop_on_error:
                success = False
                break
            continue

        # execute
        try:
            registry.commands[cmd](dev, args)
        except Exception as e:
            log(f"❌ Error executing '{line_resolved}': {e}")
            success = False
            if stop_on_error:
                break

    if log_file:
        log_file.write(f"=== DEVICE {identifier} END ===\n\n")
        log_file.close()

    dev.close()
    return success


# -------------------------------------------------------
# Main program
# -------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Batch command runner for multiple LabJack T7 devices."
    )

    parser.add_argument("--devices", required=True, help="File containing device identifiers")
    parser.add_argument("--commands", required=True, help="Command script file")
    parser.add_argument("--parallel", type=int, default=1, help="Number of devices to run in parallel")
    parser.add_argument("--log-dir", default=None, help="Optional directory for per-device logs")
    parser.add_argument("--stop-on-error", action="store_true", help="Stop execution for a device on first error")

    args = parser.parse_args()

    devices = list(load_lines(args.devices))
    if not devices:
        print("No devices found.")
        return

    commands = list(load_lines(args.commands))
    if not commands:
        print("No commands found.")
        return

    # Build the registry exactly like the shell
    registry = CommandRegistry()
    register_sd_commands(registry)
    register_modbus_commands(registry)
    register_ef_commands(registry)
    register_user_ram_commands(registry)
    register_system_commands(registry)

    print(f"🌐 Running {len(commands)} commands for {len(devices)} devices\n")

    if args.parallel <= 1:
        # sequential mode
        for identifier in devices:
            print("=" * 60)
            print(f"DEVICE {identifier}")
            print("=" * 60)
            run_commands_on_device(
                identifier, commands, registry,
                log_dir=args.log_dir,
                stop_on_error=args.stop_on_error
            )
    else:
        # parallel mode
        print(f"⚡ Executing in parallel with {args.parallel} workers\n")
        with ThreadPoolExecutor(max_workers=args.parallel) as pool:
            futures = {
                pool.submit(
                    run_commands_on_device,
                    identifier, commands, registry,
                    args.log_dir,
                    args.stop_on_error
                ): identifier
                for identifier in devices
            }

            for future in as_completed(futures):
                identifier = futures[future]
                try:
                    ok = future.result()
                    if ok:
                        print(f"✔  {identifier} completed successfully")
                    else:
                        print(f"❌ {identifier} had errors")
                except Exception as e:
                    print(f"❌ {identifier} crashed: {e}")


if __name__ == "__main__":
    main()
