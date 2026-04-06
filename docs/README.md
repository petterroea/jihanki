# Jihanki

Welcome to Jihanki. While CI/CD tools run the same processes on different (new iterations of) code, Jihanki lets you build the same thing over and over again, changing only the provided arguments. This is useful for situations where you want to provide custom builds of things for different people.

## How does bob work

Jihanki can build anything you can build inside Docker. Jihanki spins up a docker container of your choice, and runs the build from inside it. Volume mounts are used to alternatively provide the source code from outside the container, and to extract the final result. See the manifest documentation for more information.

Jihanki builds using an unprivileged user, but allows you to run privileged actions during startup. This allows you to separate privileged actions from the build itself, where some of the inputs may be user-provided.

## What does bob need

Jihanki needs dockerd and redis.

## Typical bob build process

 * Something makes HTTP API request to jihanki
 * Docker container is spun up with arguments provided in the API call
 * Command is ran, build happens
   * see [manifest/build.md](manifest.md)
 * Build-end cleanup happens:
   * A packager is used to package the resulting artefacts
   * A delivery mechanism is used to ship the packaged artefacts it to its final destination
   * A notification handler optionally notifies of the build being complete
   * see [manifest/output.md](manifest/output.md) for more info

## Where to go from here

Read the [manifest docs](manifest.md)