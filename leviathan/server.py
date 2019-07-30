import base64
import os
import threading
from pathlib import Path

from logzero import logger

from leviathan.network import Network
from leviathan.network.raknet_interface import RaknetInterface
from leviathan.utils.config import Config


class Server:

    is_running = True

    def __init__(self, data_path, plugin_path):
        self.current_thread = threading.currentThread()

        self.__network = Network(self)

        self.__network.register_interface(RaknetInterface(self))

        self.start()

    def start(self):
        self.tick_processor()

    def tick_processor(self):
        self.tick()
        pass

    def tick(self):
        self.__network.process_interface()
        pass
