def register_user_ram_commands(registry):
    @registry.command("user-ram-read")
    def cmd_ram_read(dev, args):
        typ, idx = args[0], int(args[1])
        if typ == "F32":
            print(dev.user_ram.read_f32(idx))
        elif typ == "I32":
            print(dev.user_ram.read_i32(idx))
        elif typ == "U32":
            print(dev.user_ram.read_u32(idx))
        elif typ == "U16":
            print(dev.user_ram.read_u16(idx))

    @registry.command("user-ram-write")
    def cmd_ram_write(dev, args):
        typ, idx, val = args[0], int(args[1]), args[2]
        if typ == "F32":
            dev.user_ram.write_f32(idx, float(val))
        elif typ == "I32":
            dev.user_ram.write_i32(idx, int(val))
        elif typ == "U32":
            dev.user_ram.write_u32(idx, int(val))
        elif typ == "U16":
            dev.user_ram.write_u16(idx, int(val))
