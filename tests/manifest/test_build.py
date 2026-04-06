import pytest
from pathlib import Path
from pydantic import ValidationError
from jihanki.pipeline.build import Build
from jihanki.pipeline.source import FilesystemBuildMaterialSource
from jihanki.pipeline.schema import BuildSchema


def test_minimal_build():
    s = BuildSchema(command="./run.sh", container="my-image:latest")
    b = Build(s, Path("/"))
    assert b.command == "./run.sh"
    assert b.container == "my-image:latest"
    assert b.privileged_command == ""
    assert b.workdir == "/var/runner"
    assert b.regcred_directory == ""
    assert b.build_material_source is None


def test_all_fields():
    s = BuildSchema(
        command="./build.sh",
        container="builder:1.0",
        privileged_command="./setup.sh",
        workdir="/workspace",
        regcred_directory="/creds/config.json",
        build_material={
            "source": "filesystem",
            "options": {"location": "/src"},
        },
    )
    b = Build(s, Path("/"))
    assert b.command == "./build.sh"
    assert b.container == "builder:1.0"
    assert b.privileged_command == "./setup.sh"
    assert b.workdir == "/workspace"
    assert b.regcred_directory == "/creds/config.json"
    assert isinstance(b.build_material_source, FilesystemBuildMaterialSource)


def test_build_material_none_explicit():
    s = BuildSchema(
        command="./run.sh",
        container="img",
        build_material={"source": "none"},
    )
    b = Build(s, Path("/"))
    assert b.build_material_source is None


def test_build_material_invalid_source():
    with pytest.raises(ValidationError):
        BuildSchema(
            command="./run.sh",
            container="img",
            build_material={"source": "git"},
        )


def test_missing_command():
    with pytest.raises(ValidationError):
        BuildSchema(container="img")


def test_missing_container():
    with pytest.raises(ValidationError):
        BuildSchema(command="./run.sh")


def test_wrong_type_command():
    with pytest.raises(ValidationError):
        BuildSchema(command=123, container="img")
