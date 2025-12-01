class CommandRegistry:
    def __init__(self):
        self.commands = {}

    def command(self, name):
        def decorator(fn):
            self.commands[name] = fn
            return fn
        return decorator

    def dispatch(self, dev, line):
        parts = line.split()
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]
        if cmd not in self.commands:
            print(f"Unknown command: {cmd}")
            return
        self.commands[cmd](dev, args)

    def print_help(self):
        print("Available commands:")
        for name in sorted(self.commands.keys()):
            print(f"  {name}")
