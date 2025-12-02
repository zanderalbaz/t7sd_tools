try:
    import readline  # works on macOS/Linux or pyreadline3 on Windows
except ImportError:
    try:
        import pyreadline3 as readline
    except ImportError:
        readline = None
        print("[WARN] Readline/pyreadline3 not available. Tab completion disabled.")
import os

class ShellCompleter:
    def __init__(self, registry, dev, sd_cache):
        self.registry = registry
        self.dev = dev
        self.sd_cache = sd_cache

    def complete(self, text, state):
        buffer = readline.get_line_buffer() if readline is not None else ""
        tokens = buffer.split()

        # COMMAND COMPLETION
        if len(tokens) <= 1:
            matches = [cmd for cmd in self.registry.commands if cmd.startswith(text)]
            try:
                return matches[state]
            except IndexError:
                return None

        # ARG COMPLETION BASED ON COMMAND TYPE
        cmd = tokens[0]

        # SD PATH COMPLETION
        if cmd in ("ls", "cd", "cat", "get", "rm"):
            paths = self.sd_cache.complete_path(text)
            try:
                return paths[state]
            except IndexError:
                return None

        # REGISTER COMPLETION
        if cmd in ("read", "write", "ef-read"):
            matches = [r for r in self.registry.register_names if r.startswith(text)]
            try:
                return matches[state]
            except IndexError:
                return None

        return None
