# Sample Implementations

## Build

Most samples should have container build instructions in the form of a `Dockerfile`, sometimes additionally there will be a `docker-compose.yml` orchestration file where multiple services are required to run the sample.

Build commands for the images should take the form:
```shell
DOCKER_BUILDKIT=1 docker build -t <image tag> .
```

The layers within built images can be examined using a tool like [dive](https://github.com/wagoodman/dive).

First change to the sample directory, then run the following command to open a CLI application that allows you to examine each layer in turn.

```shell
docker run --rm -it \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v  "$(pwd)":"$(pwd)" \
  -w "$(pwd)" \
  -v "$HOME/.dive.yaml":"$HOME/.dive.yaml" \
  wagoodman/dive:latest build -t <image tag> .
```

## Samples
Samples are detailed below, with a summary of the technology/concepts they demonstrate, and the languages they utilise.
### Async HTTP Requests

- Path: `./async-http-get`
- Language: **Python**

Async HTTP requests with payloads, with request metrics, connection pooling and rate limiting.

### Fire CLI

- Path: `./fire-cli`
- Language: **Python**

Python package that turns a collection of modules or classes into a CLI interface, without having to hardcode specifics.
