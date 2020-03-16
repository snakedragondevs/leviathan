import os
from logzero import logger

from leviathan.core import Core

DATA_PATH = os.getcwd() + '/'
PLUGIN_PATH = DATA_PATH + 'plugins'


def main(args=None):
    # init instance
    core = Core(DATA_PATH, PLUGIN_PATH)
    try:
        # run server core
        core.run()
    except Exception as e:
        print(e)

    logger.info('stopping other threads')

    # stop running threads

    logger.info('server stopped')


if __name__ == '__main__':
    main()
