import pytest
import tempfile
import shutil
from pathlib import Path

from jihanki.pipeline.output.packager import CopyPackager


@pytest.fixture
def packager():
    return CopyPackager()


@pytest.fixture
def code_dir():
    d = Path(tempfile.mkdtemp())
    (d / "src").mkdir()
    (d / "src" / "main.py").write_text("print('hello')")
    (d / "src" / "util.py").write_text("x = 1")
    (d / "readme.txt").write_text("readme")
    yield d
    shutil.rmtree(d)


@pytest.fixture
def outdir():
    d = Path(tempfile.mkdtemp())
    yield d
    shutil.rmtree(d)


def test_copies_all_files(packager, code_dir, outdir):
    files = ["src/main.py", "src/util.py", "readme.txt"]
    result = packager.package("job-1", files, code_dir, outdir)

    assert len(result) == 3
    names = sorted(p.name for p in result)
    assert names == ["main.py", "readme.txt", "util.py"]


def test_files_in_job_subdirectory(packager, code_dir, outdir):
    files = ["readme.txt"]
    result = packager.package("job-2", files, code_dir, outdir)

    assert result[0].parent == outdir / "job-2"


def test_copied_content_matches_source(packager, code_dir, outdir):
    files = ["src/main.py"]
    result = packager.package("job-3", files, code_dir, outdir)

    assert result[0].read_text() == "print('hello')"


def test_empty_file_list(packager, code_dir, outdir):
    result = packager.package("job-4", [], code_dir, outdir)

    assert result == []
    assert (outdir / "job-4").is_dir()


def test_flattens_paths(packager, code_dir, outdir):
    """CopyPackager uses only filename, not full path."""
    files = ["src/main.py", "src/util.py"]
    result = packager.package("job-5", files, code_dir, outdir)

    for f in result:
        # All files should be directly inside job dir, not in src/
        assert f.parent == outdir / "job-5"
