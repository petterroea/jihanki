# Jihanki

_vending machine_

A simple one-shot build system that allows you to run preconfigured build processes using a REST api. "Buiding as a service". It's the opposite of CI/CD: Instead of building as many different releases of software as possible, jihanki is a factory that uses the same code with different build arguments to pop out the same thing over and over.

Useful for when you have a project where you need to give every user a custom release. Jihanki can build anything that can run inside a Docker container.

## Example

```
version: "1"
pipelines:
  # Compile c program and package it as zip
  c_compile:
    build:
      command: ./build.sh
      container: "build_c_example"
      workdir: "/build"
      force_pull: false
    input:
      environment:
        # Provide the name of the person
        PERSON_NAME:
          source: field
          fieldname: person_name
    output:
      - patterns:
          - main
        packager: zip
        destination:
          provider: filesystem
          options:
            location: /tmp/buildout
        notify:
          destination: cli
```

Running it:

```
curl -X POST http://localhost:8000/api/v1/job -H "Authorization: Token foo" --json '{"pipeline": "example_pipeline", "person_name": "Jeff"}'
```

## Running jihanki

jihanki is supposed to run in docker, albeit it can be a bit tricky since you have to wrap your brain around filesystem locations in up to 2 layers of containers. In general, see the provided `docker-compose.yml`.

If you want to run it locally (for testing, f.ex) you could do this:

```
# Start redis
docker compose up redis # The redis port is exposed so you can use access it outside the compose network

# Start the webserver
PIPELINES_LOCATION=test-pipelines/c_compile/pipelines.yml BOB_TOKEN=foo REDIS_HOST=localhost sanic jihanki.webserver --host=0.0.0.0 --reload

# Start the worker
SCRATCH_DIR=/tmp/jihanki_scratch rq worker --with-scheduler --url redis://localhost

```

If you want to run it in Kubernetes, you have to particularly pay attention to making sure both the worker and the dind pod share the same scratch directory location.
