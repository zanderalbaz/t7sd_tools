import threading

class SDCache:
    """
    A safe-on-T7 SD directory cache.
    Does NOT recursively walk the filesystem.
    Caches only the directories that the user actually visits or requests.
    """

    def __init__(self, dev):
        self.dev = dev
        self.cache = {}      # path -> [entries]
        self.lock = threading.Lock()

    def get(self, path):
        """
        Return cached list for `path`, or fetch and store it safely.
        """
        # Normalize path
        if not path or path == "":
            path = "/"

        with self.lock:
            if path in self.cache:
                return self.cache[path]

        # Fetch from device, safely (no recursion)
        try:
            entries = self.dev.sd.list_dir(path)
            names = [e.name for e in entries]
        except Exception as e:
            # Avoid spamming output
            return []

        with self.lock:
            self.cache[path] = names

        return names

    def complete_path(self, prefix):
        """
        Autocomplete a path prefix using cached directory listings.
        """
        # Handle root
        if prefix.startswith("/"):
            dir_part, _, partial = prefix.rpartition("/")
            dir_part = dir_part if dir_part else "/"
        else:
            # relative paths -> use CWD
            cwd = self.dev.sd.get_cwd()
            dir_part = cwd
            partial = prefix

        names = self.get(dir_part)
        return [
            (dir_part.rstrip("/") + "/" + name)
            for name in names
            if name.startswith(partial)
        ]
