from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import os

from labjack import ljm
from . import sd_utils


@dataclass
class SDEntry:
    name: str
    size: int
    is_file: bool
    is_dir: bool
    raw_attr: int


@dataclass
class DiskInfo:
    sector_size_bytes: int
    sectors_per_cluster: int
    total_clusters: int
    free_clusters: int

    @property
    def total_bytes(self) -> int:
        return self.sector_size_bytes * self.sectors_per_cluster * self.total_clusters

    @property
    def free_bytes(self) -> int:
        return self.sector_size_bytes * self.sectors_per_cluster * self.free_clusters

    @property
    def total_mb(self) -> float:
        return self.total_bytes / 1048576.0

    @property
    def free_mb(self) -> float:
        return self.free_bytes / 1048576.0


class SDInterface:
    """
    Encapsulates SD-card operations for a single device handle.
    """

    def __init__(self, handle: int):
        self.handle = handle

    # ------------------ internal helpers ------------------ #

    def _sanitize_path_for_sd(self, path: str) -> str:
        if not path:
            path = "/"
        return sd_utils.sanitizePath(path)

    def _resolve_dir_and_file(self, sd_path: str) -> Tuple[str, str]:
        if not sd_path:
            raise ValueError("Empty SD path is not valid.")
        dir_part, filename = os.path.split(sd_path)
        if not filename:
            raise ValueError(f"Path '{sd_path}' does not contain a filename.")
        return dir_part, filename

    # ------------------ public SD API ------------------ #

    def get_cwd(self) -> str:
        """
        Get current working directory on SD card (without trailing null).
        """
        raw = sd_utils.getCWD(self.handle)
        return raw.rstrip("\x00")

    def chdir(self, path: str):
        """
        Change current working directory on SD card.
        """
        sd_path = self._sanitize_path_for_sd(path)
        sd_utils.goToPath(self.handle, sd_path)

    def list_dir(self, path: Optional[str] = None) -> List[SDEntry]:
        """
        List contents of the given directory.
        If path is None, uses the current working directory.
        """
        start_dir = self.get_cwd()
        try:
            if path is not None:
                self.chdir(path)

            raw_contents: Dict[str, Tuple[int, int]] = sd_utils.getCurDirContents(
                self.handle
            )
            entries: List[SDEntry] = []
            for raw_name, (size, attr) in raw_contents.items():
                name = raw_name.rstrip("\x00")
                is_file = bool(attr & (1 << 5))
                is_dir = bool(attr & (1 << 4))
                entries.append(
                    SDEntry(
                        name=name,
                        size=size,
                        is_file=is_file,
                        is_dir=is_dir,
                        raw_attr=attr,
                    )
                )
            return entries
        finally:
            self.chdir(start_dir)

    def read_file_bytes(self, sd_path: str) -> bytes:
        """
        Read a file from the SD card and return its raw bytes.
        """
        original_cwd = self.get_cwd()
        try:
            dir_part, filename = self._resolve_dir_and_file(sd_path)
            if dir_part:
                self.chdir(dir_part)

            # Get directory contents to find file size & real name
            dir_contents = sd_utils.getCurDirContents(self.handle)
            matched_key = None
            for key in dir_contents.keys():
                if key.rstrip("\x00") == filename:
                    matched_key = key
                    break

            if matched_key is None:
                raise FileNotFoundError(f"File not found on SD: {sd_path}")

            file_size = dir_contents[matched_key][0]

            # Prepare filename for FILE_IO
            filename_nt = sd_utils.sanitizePath(filename)
            name_len = len(filename_nt)
            name_bytes = bytearray(filename_nt, "ascii")

            ljm.eWriteName(self.handle, "FILE_IO_PATH_WRITE_LEN_BYTES", name_len)
            ljm.eWriteNameByteArray(
                self.handle, "FILE_IO_PATH_WRITE", name_len, name_bytes
            )
            ljm.eWriteName(self.handle, "FILE_IO_OPEN", 1)
            data_bytes = ljm.eReadNameByteArray(
                self.handle, "FILE_IO_READ", file_size
            )
            ljm.eWriteName(self.handle, "FILE_IO_CLOSE", 1)

            return bytes(data_bytes)
        finally:
            self.chdir(original_cwd)

    def read_file_text(
        self, sd_path: str, encoding: str = "utf-8", errors: str = "replace"
    ) -> str:
        data = self.read_file_bytes(sd_path)
        return data.decode(encoding, errors=errors)

    def delete_file(self, sd_path: str):
        """
        Delete a file from the SD card.
        """
        sd_utils.deleteFile(self.handle, sd_path)

    def get_disk_info(self) -> DiskInfo:
        """
        Return SD card disk info as a DiskInfo object.
        """
        names = [
            "FILE_IO_DISK_SECTOR_SIZE_BYTES",
            "FILE_IO_DISK_SECTORS_PER_CLUSTER",
            "FILE_IO_DISK_TOTAL_CLUSTERS",
            "FILE_IO_DISK_FREE_CLUSTERS",
        ]
        vals = ljm.eReadNames(self.handle, len(names), names)
        return DiskInfo(
            sector_size_bytes=int(vals[0]),
            sectors_per_cluster=int(vals[1]),
            total_clusters=int(vals[2]),
            free_clusters=int(vals[3]),
        )
