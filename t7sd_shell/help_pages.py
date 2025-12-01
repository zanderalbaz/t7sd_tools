HELP_SECTIONS = {
    "sd": """
SD CARD COMMANDS
----------------
ls [path]            List directory contents
cd <path>            Change working directory
pwd                  Print working directory
cat <file>           View file contents
get <remote> <local> Download file to PC
rm <remote>          Delete a file
info                 Show disk info
""",

    "modbus": """
MODBUS COMMANDS
---------------
read <register>             Read a register value
write <register> <value>    Write a register
""",

    "ef": """
EF / THERMISTOR COMMANDS
------------------------
ef-read <AINx>          
ef-set <AINx> A=<a> B=<b> C=<c> D=<d>
""",

    "ram": """
USER RAM COMMANDS
-----------------
user-ram-read <type> <index>
user-ram-write <type> <index> <value>

types: F32, I32, U32, U16
""",

    "system": """
SYSTEM COMMANDS
---------------
help                Show this help
help <section>      Show help for SD, EF, RAM, SYSTEM, etc.
quit / exit         Exit the shell
"""
}


def print_help(section=None):
    if section is None:
        print("AVAILABLE HELP SECTIONS:")
        for s in HELP_SECTIONS:
            print(f"  {s}")
        print("\nType: help <section>  for more details.")
        return

    section = section.lower()
    if section in HELP_SECTIONS:
        print(HELP_SECTIONS[section])
    else:
        print(f"No help section named '{section}'.")
