def register_system_commands(registry):
    @registry.command("help")
    def cmd_help(dev, args):
        registry.print_help()

    @registry.command("exit")
    @registry.command("quit")
    def cmd_exit(dev, args):
        raise SystemExit

from t7sd_shell.help_pages import print_help

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
