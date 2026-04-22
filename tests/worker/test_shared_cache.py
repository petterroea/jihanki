import os
from pathlib import Path

from jihanki.pipeline import Pipeline
from jihanki.pipeline.schema import PipelineSchema
from jihanki.worker import get_job_environment, init_volumes


def test_shared_cache_in_volumes(tmp_path):
    os.environ["SCRATCH_DIR"] = str(tmp_path)

    schema = PipelineSchema.model_validate(
        {
            "build": {
                "command": "./build.sh",
                "container": "test-image",
                "workdir": "/build",
                "shared_cache": [
                    "/host/cache:/build/cache",
                    "/host/temp:/build/temp",
                ],
            },
            "output": [
                {
                    "patterns": ["*.bin"],
                    "destination": {
                        "provider": "filesystem",
                        "options": {"location": "/tmp/out"},
                    },
                    "notify": {"destination": "cli"},
                }
            ],
        }
    )
    pipeline = Pipeline("test", schema, Path("/fake/pipelines.yml"))

    with init_volumes("test-job", {}, pipeline) as (volumes, output_dir):
        assert "/host/cache:/build/cache" in volumes
        assert "/host/temp:/build/temp" in volumes


def test_no_shared_cache_in_volumes(tmp_path):
    os.environ["SCRATCH_DIR"] = str(tmp_path)

    schema = PipelineSchema.model_validate(
        {
            "build": {
                "command": "./build.sh",
                "container": "test-image",
                "workdir": "/build",
            },
            "output": [
                {
                    "patterns": ["*.bin"],
                    "destination": {
                        "provider": "filesystem",
                        "options": {"location": "/tmp/out"},
                    },
                    "notify": {"destination": "cli"},
                }
            ],
        }
    )
    pipeline = Pipeline("test", schema, Path("/fake/pipelines.yml"))

    with init_volumes("test-job", {}, pipeline) as (volumes, output_dir):
        # Only the /output mount should be present
        assert len(volumes) == 1
        assert "/output" in volumes[0]


def test_job_environment_includes_full_and_short_job_id():
    schema = PipelineSchema.model_validate(
        {
            "build": {
                "command": "./build.sh",
                "container": "test-image",
                "workdir": "/build",
            },
            "input": {
                "environment": {
                    "FROM_REQUEST": {"source": "field", "fieldname": "value"},
                },
            },
            "output": [
                {
                    "patterns": ["*.bin"],
                    "destination": {
                        "provider": "filesystem",
                        "options": {"location": "/tmp/out"},
                    },
                    "notify": {"destination": "cli"},
                }
            ],
        }
    )
    pipeline = Pipeline("test", schema, Path("/fake/pipelines.yml"))

    env = get_job_environment(
        pipeline,
        {"value": "from-user"},
        "c70565e2-1234-5678-90ab-abcdefabcdef",
    )

    assert env["FROM_REQUEST"] == "from-user"
    assert env["JIHANKI_JOB_ID"] == "c70565e2-1234-5678-90ab-abcdefabcdef"
    assert env["JIHANKI_JOB_ID_SHORT"] == "c70565e2"
