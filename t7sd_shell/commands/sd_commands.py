import os
import datetime

def register_sd_commands(registry):
    @registry.command("ls")
    def cmd_ls(dev, args):
        path = args[0] if args else None
        entries = dev.sd.list_dir(path)
        for e in entries:
            if e.is_file:
                print(f"{e.name:<32}  FILE   {e.size} bytes")
            elif e.is_dir:
                print(f"{e.name:<32}  DIR")
            else:
                print(f"{e.name:<32}  OTHER")

    @registry.command("cd")
    def cmd_cd(dev, args):
        dev.sd.chdir(args[0])

    @registry.command("pwd")
    def cmd_pwd(dev, args):
        print(dev.sd.get_cwd())

    @registry.command("cat")
    def cmd_cat(dev, args):
        print(dev.sd.read_file_text(args[0]))

    @registry.command("get")
    def cmd_get(dev, args):
        if len(args) != 2:
            print("Usage: get <remote_path> <local_path>")
            return

        remote_path, local_path = args

        # -------------------------------------------------------
        # 1. Read file bytes from the device SD card
        # -------------------------------------------------------
        try:
            data = dev.sd.read_file_bytes(remote_path)
        except Exception as e:
            print(f"Error reading remote file '{remote_path}': {e}")
            return

        # -------------------------------------------------------
        # 2. Build timestamped directory structure
        # -------------------------------------------------------
        now = datetime.datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H%M%S")

        # device identifier (IP, serial number, etc.)
        identifier = dev.identifier.replace("/", "_").replace("\\", "_")

        # If user gave a directory rather than a full file path:
        if local_path.endswith("/") or os.path.isdir(local_path):
            filename = os.path.basename(remote_path)
            local_path = os.path.join(local_path, filename)

        # Construct final structured path:
        base_name = os.path.basename(local_path)
        base_dir = os.path.dirname(local_path)

        # root of logs for this device
        full_dir = os.path.join(base_dir, identifier, date_str)

        # final filename has timestamp prefix
        final_path = os.path.join(full_dir, f"{time_str}_{base_name}")

        # -------------------------------------------------------
        # 3. Ensure directories exist
        # -------------------------------------------------------
        try:
            os.makedirs(full_dir, exist_ok=True)
        except Exception as e:
            print(f"Error creating directories for '{full_dir}': {e}")
            return

        # -------------------------------------------------------
        # 4. Auto-rename duplicates
        # -------------------------------------------------------
        path_no_ext, ext = os.path.splitext(final_path)
        counter = 1
        candidate_path = final_path

        while os.path.exists(candidate_path):
            candidate_path = f"{path_no_ext} ({counter}){ext}"
            counter += 1

        final_path = candidate_path

        # -------------------------------------------------------
        # 5. Write file
        # -------------------------------------------------------
        try:
            with open(final_path, "wb") as f:
                f.write(data)
            print(f"Downloaded '{remote_path}' → '{final_path}'")
        except Exception as e:
            print(f"Error writing to '{final_path}': {e}")

    @registry.command("rm")
    def cmd_rm(dev, args):
        dev.sd.delete_file(args[0])

    @registry.command("info")
    def cmd_info(dev, args):
        info = dev.sd.get_disk_info()
        print(
            f"Total: {info.total_mb:.2f} MB\n"
            f"Free:  {info.free_mb:.2f} MB\n"
            f"Sector: {info.sector_size_bytes} bytes\n"
        )
