import shutil
from pathlib import Path
import os
import logging

log = logging.getLogger(__name__)


class DestinationHandler:
    """Base class for delivering packaged build artifacts to their final destination."""

    def deliver(self, filename):
        raise RuntimeError("Not implemented")


class RedisDestinationHandler(DestinationHandler):
    """Stores packaged build artifacts in Redis with configurable key prefix and expiry.

    Only supports delivering a single file. Files are stored as binary data in Redis.
    """

    def __init__(self, options):
        self.prefix = options.get("key_prefix", "")
        self.expiry = options.get("expiry_seconds", 60 * 60 * 24)

    def deliver(self, foundfiles_dir: Path):
        # yolo-import to establish the redis connection
        log.debug("Connecting to redis")
        from ..redis import redis_connection

        # List files in folder. If more than one - not supported
        files = list(foundfiles_dir.iterdir())
        if len(files) != 1:
            raise RuntimeError(
                f"Redis destination handler only supports one file - got {len(files)}"
            )

        with files[0].open("rb") as file:
            keyname = "%s%s" % (self.prefix, files[0].stem)
            redis_connection.set(keyname, file.read())
            redis_connection.expire(keyname, self.expiry)
            log.info("Delivered payload to redis")


class FilesystemDestinationHandler(DestinationHandler):
    """Delivers packaged build artifacts to a filesystem location.

    Copies all files from the source directory to the configured destination path,
    setting web-readable permissions on all delivered files and directories.
    """

    def __init__(self, options):
        self.location = Path(options["location"])

    def deliver(self, foundfiles_dir: Path):
        log.info(f"Delivering output to {self.location}")
        destination_existed = self.location.exists()
        self.location.mkdir(parents=True, exist_ok=True)
        if not destination_existed:
            os.chmod(self.location, 0o755)

        for entry in foundfiles_dir.iterdir():
            destination = self.location / entry.name

            if entry.is_dir():
                shutil.copytree(entry, destination, dirs_exist_ok=True)
                os.chmod(destination, 0o755)

                for root, dirs, files in os.walk(entry):
                    rel_root = Path(root).relative_to(entry)

                    for d in dirs:
                        os.chmod(destination / rel_root / d, 0o755)

                    for f in files:
                        os.chmod(destination / rel_root / f, 0o644)
            elif entry.is_file():
                shutil.copy2(entry, destination)
                os.chmod(destination, 0o644)
