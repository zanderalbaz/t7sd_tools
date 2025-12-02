from t7sd_shell.help_pages import print_help
import os
def register_system_commands(registry):
    @registry.command("help")
    def cmd_help(dev, args):
        if args:
            print_help(args[0])
        else:
            for sec in ["sd", "modbus", "ef", "user_ram", "system"]:
                print_help(sec)

    @registry.command("quit")
    @registry.command("exit")
    def cmd_exit(dev, args):
        raise SystemExit


    @registry.command("clear")
    @registry.command("cls")
    def cmd_clear(dev, args):
        if os.name == "nt": #if Windows
            os.system('cls')
        else:
            os.system('clear')
