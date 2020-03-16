import threading
import asyncio

from logzero import logger

# from leviathan.network import Network


class LeviathanCore:

    NAME = "Leviathan"
    API_VERSION = "0.1.0"
    MINECRAFT_VERSION = "1.12.0"

    def __init__(self, data_path, plugin_path):

        # TODO Console

        # TODO Configurations

        # TODO File Loaders (banlist, operators, whitelists)

        # TODO Language/Locale (Low Priority) default=eng

        # TODO Plugin Loaders

        # TODO levels and players directories

        # TODO load default level

        # TODO other levels

        # TODO Networks and Server Core
        self.leviathan_server = None

        # TODO autosaving

        # TODO game loop
        asyncio.run(self.loop())

    async def loop(self):
        tick_counter = 0
        while 1:
            try:
                # tick
                self.tick()
                tick_counter += 1
                logger.debug('tick {}'.format(tick_counter))
                await asyncio.sleep(1)
            except RuntimeError:
                logger.error('exception')

    def tick(self):
        logger.debug('ticking')
