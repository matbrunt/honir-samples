# Fire CLI

The [fire](https://github.com/google/python-fire) python package turns any source code tree into a CLI structure.

You can use it with module imports, classes or functions, and it will automatically turn them into CLI args.

In the current setup, we import each packages underlying job in `src/__init__.py`, then we can specify which job to run.

## Build

Build the image with `DOCKER_BUILDKIT=1 docker build -t firecli .`.

## Execute
You can see what commands have been picked up in the Fire CLI by calling `main.py` without any arguments.

e.g. `docker run --rm -ti firecli python main.py`.

The CLI can be called from within the container by spawning a bash shell with `docker run --rm -ti firecli bash`, then running the commands below.

```shell
$ python main.py job run
2021-10-04 14:16:41 INFO Running job A
2021-10-04 14:16:41 INFO Running job B
```

```shell
$ python main.py job_a run
2021-10-04 14:16:46 INFO Running job A
```

```shell
$ python main.py job_b run
2021-10-04 14:16:50 INFO Running job B
```

Alternatively, you can call the CLI directly by passing the full command to the Docker container runtime.

```shell
docker run --rm -ti firecli python main.py job run
docker run --rm -ti firecli python main.py job_a run
docker run --rm -ti firecli python main.py job_b run
```