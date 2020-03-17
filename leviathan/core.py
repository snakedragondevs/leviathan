import asyncio

from logzero import logger

from leviathan.network import Network
from leviathan.network.network_interface import NetworkInterface


class Core:

    # is_running = True
    # has_stopped = False

    def __init__(self, data_path, plugin_path):
        # some initialize at instance level

        # setup defaults

        # registries

        # initialize server console
        # initialize console thread
        pass

    def run(self):
        # TODO directories
        # worlds/ players/

        # (console thread).start

        # TODO Configurations
        # if not leviathan.yml, write new including language selection
        # and setup default properties and more default network configurations

        # TODO metadata

        # TODO more configs (ops.txt, white-list.txt, banned-players.json, banned-ips.json)

        # TODO autosaving

        # TODO initialize console commands

        # TODO managers

        # TODO packs

        # TODO registries
        # block, item, entity, etc

        # TODO Levels

        # TODO network instance, and engine interface
        self.network = Network()
        self.network.register_interface(NetworkInterface())

        # TODO game loop
        self.start_server()

    def start_server(self):
        loop = asyncio.get_event_loop()
        self.tick_counter = 0
        try:
            # worker
            asyncio.ensure_future(self.tick_processor())
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()

    async def tick_processor(self):
        while True:  # while server is running
            self.tick()
            logger.debug('ticking {}'.format(self.tick_counter))
            await asyncio.sleep(1)

    def tick(self):
        self.tick_counter += 1

        self.network.process_interfaces()
