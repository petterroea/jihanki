# Pipeline Manifest

A pipeline manifest is a YAML file that defines one or more pipelines for Bob to run. Each pipeline describes how to build, what inputs it expects, and where to deliver results.

In general, there are two major ways of running jihanki:
 * Everything in docker image (including build material / source code)
   - A docker image is used to package both the tools needed to build, as well as the source code.
 * Source material copied and volume mounted in
   - jihanki will make a copy of the source code, stored on the host, and volume mount it into the container.

See [build](build.md) for info on how to configure this.


## File Structure

```yaml
version: "1"
pipelines:
  pipeline_name:
    build: { ... }
    input: { ... }
    output: [ ... ]
```

- `version` (string, required): Must be `"1"`.
- `pipelines` (map, required): A map of pipeline names to their definitions.

Each pipeline has three sections:

| Section | Required | Description |
|---------|----------|-------------|
| [build](build.md) | Yes | Container, commands, and build material |
| [input](input.md) | No | Environment variables and files injected into the build |
| [output](output.md) | Yes | Artifact packaging, delivery, and notifications |
