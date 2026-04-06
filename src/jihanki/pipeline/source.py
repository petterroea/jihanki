import shutil
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


class BuildMaterialSource:
    def get_code(self, source):
        raise RuntimeError("Not implemented")


class FilesystemBuildMaterialSource(BuildMaterialSource):
    def __init__(self, location: Path):
        self.location = location

    def get_code(self, destination):
        # Copy setup files
        logger.info("Getting build files from file system")
        shutil.copytree(self.location, destination)
