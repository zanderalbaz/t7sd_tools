def register_modbus_commands(registry):
    @registry.command("read")
    def cmd_read(dev, args):
        print(dev.modbus.read(args[0]))

    @registry.command("write")
    def cmd_write(dev, args):
        name, value = args
        dev.modbus.write(name, float(value))
