import threading
import asyncio

from logzero import logger

from leviathan.network import Network


class LeviathanCore:

    NAME = "Leviathan"
    API_VERSION = "0.1.0"
    MINECRAFT_VERSION = "1.12.0"

    def __init__(self, data_path, plugin_path):
        self.is_running = True
        self.current_thread = threading.currentThread()

        # instantiate network
        self.__network = Network(self)

        # todo main thread loop
        asyncio.run(self.loop())


    async def loop(self):
        print('Hello ...')
        await asyncio.sleep(1)
        print('... World!')
