def register_ef_commands(registry):
    @registry.command("ef-read")
    def cmd_ef_read(dev, args):
        print(dev.ef.read_ef_value(args[0]))

    @registry.command("ef-set")
    def cmd_ef_set(dev, args):
        ain = args[0]
        kv = dict(a.split("=") for a in args[1:])
        A = float(kv["A"])
        B = float(kv["B"])
        C = float(kv["C"])
        D = float(kv["D"])
        dev.ef.configure_thermistor_SH(ain, A, B, C, D)
