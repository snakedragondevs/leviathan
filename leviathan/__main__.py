import os

from leviathan.leviathan_core import LeviathanCore
from logzero import logger


DATA_PATH = os.getcwd() + "/"
PLUGIN_PATH = DATA_PATH + "plugins"


def main(args=None):
    try:
        LeviathanCore(DATA_PATH, PLUGIN_PATH)
    except Exception as e:
        print(e)

    logger.info("Stopping other threads")


if __name__ == "__main__":
    main()
