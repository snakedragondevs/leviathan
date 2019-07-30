import os

from leviathan.server import Server
from logzero import logger

from leviathan.thread_manager import ThreadManager

DATA_PATH = os.getcwd() + "/"
PLUGIN_PATH = DATA_PATH + "plugins"

def main(args=None):
    try:
        Server(DATA_PATH, PLUGIN_PATH)
    except Exception as e:
        print(e)

    logger.info("Stopping other threads")


if __name__ == "__main__":
    main()
