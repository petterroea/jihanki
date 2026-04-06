import shutil
from zipfile import ZipFile

from pathlib import Path

import logging

logger = logging.getLogger(__name__)


class Packager:
    """Base class for packaging build artifacts into deliverable formats."""

    def package(self, job_id: str, files, code_dir: Path, outdir: Path):
        raise RuntimeError("Not implemented")


class ZipPackager(Packager):
    """Packages build artifacts by creating a ZIP archive containing all matched files."""

    def package(self, job_id: str, files, code_dir: Path, outdir: Path):
        if len(files) == 0:
            logger.warning("Found no artifacts")

        zipfile = outdir / f"{job_id}.zip"

        with ZipFile(zipfile, "w") as z:
            for file in files:
                z.write(code_dir / file, arcname=file)
        return [zipfile]


class CopyPackager(Packager):
    """Packages build artifacts by copying all files to a named folder in the destination directory.

    Files are copied to a subdirectory named after the job ID, preserving only the filename - not paths.
    """

    def package(self, job_id: str, files, code_dir: Path, outdir: Path):
        if len(files) == 0:
            logger.warning("Found no artifacts")

        target_dir = outdir / job_id
        target_dir.mkdir(parents=True)
        copied_files = []

        for file in files:
            source_file = code_dir / file
            target_file = target_dir / Path(file).name

            logger.debug(f"{source_file} -> {target_file}")

            shutil.copy(source_file, target_file)
            copied_files.append(target_file)
        return copied_files
