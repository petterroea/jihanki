import pytest
import zipfile
import tempfile
import shutil
from pathlib import Path

from jihanki.pipeline.output.packager import ZipPackager


@pytest.fixture
def packager():
    return ZipPackager()


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


def test_creates_zip_with_all_files(packager, code_dir, outdir):
    files = ["src/main.py", "src/util.py", "readme.txt"]
    result = packager.package("job-1", files, code_dir, outdir)

    assert len(result) == 1
    assert result[0].suffix == ".zip"
    assert result[0].name == "job-1.zip"

    with zipfile.ZipFile(result[0], "r") as z:
        assert sorted(z.namelist()) == sorted(files)


def test_zip_contents_match_source(packager, code_dir, outdir):
    files = ["src/main.py"]
    result = packager.package("job-2", files, code_dir, outdir)

    with zipfile.ZipFile(result[0], "r") as z:
        assert z.read("src/main.py") == b"print('hello')"


def test_empty_file_list(packager, code_dir, outdir):
    result = packager.package("job-3", [], code_dir, outdir)

    assert len(result) == 1
    with zipfile.ZipFile(result[0], "r") as z:
        assert z.namelist() == []


def test_zip_lands_in_outdir(packager, code_dir, outdir):
    files = ["readme.txt"]
    result = packager.package("job-4", files, code_dir, outdir)

    assert result[0].parent == outdir
