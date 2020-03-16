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
        self.start()

    def start(self):
        loop = asyncio.get_event_loop()
        try:
            # worker
            asyncio.ensure_future(self.tick_processor())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    async def tick_processor(self):
        while True:
            logger.debug('ticking')
            await asyncio.sleep(1)
            logger.debug('finished')
