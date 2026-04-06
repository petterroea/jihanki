import pytest
import tempfile
import shutil
from pathlib import Path

import logging

logging.basicConfig(level=logging.DEBUG)


@pytest.fixture
def test_file_structure():
    """Create a temporary directory with test files at different depths"""
    test_dir = tempfile.mkdtemp()
    test_path = Path(test_dir)

    # Level 1 files
    (test_path / "file1.txt").write_text("content1")
    (test_path / "file2.py").write_text("content2")
    (test_path / "README.md").write_text("readme")

    # Level 2 files
    (test_path / "subdir1").mkdir()
    (test_path / "subdir1" / "nested1.txt").write_text("nested1")
    (test_path / "subdir1" / "nested1.py").write_text("nested1 py")

    (test_path / "subdir2").mkdir()
    (test_path / "subdir2" / "nested2.txt").write_text("nested2")

    # Level 3 files
    (test_path / "subdir1" / "deepdir").mkdir()
    (test_path / "subdir1" / "deepdir" / "deep1.txt").write_text("deep1")
    (test_path / "subdir1" / "deepdir" / "deep1.py").write_text("deep1 py")

    # Level 4 files
    (test_path / "subdir1" / "deepdir" / "verydeep").mkdir()
    (test_path / "subdir1" / "deepdir" / "verydeep" / "very1.txt").write_text("very1")

    # Create a directory (should be filtered out)
    (test_path / "emptydir").mkdir()

    yield test_dir

    # Cleanup
    shutil.rmtree(test_dir)
