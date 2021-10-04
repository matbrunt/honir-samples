import sys
import logging
import coloredlogs
import fire
import src


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
coloredlogs.install(fmt="%(asctime)s %(levelname)s %(message)s")


if __name__ == "__main__":
    fire.Fire(src)
