import base64
import datetime
import os
import threading
import time
from pathlib import Path

from logzero import logger

from leviathan.network import Network
from leviathan.utils.config import Config


def TimestampMillisec64():
    return int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)


class Server:

    def __init__(self, data_path, plugin_path):
        self.is_running = True
        self.current_thread = threading.currentThread()

        self.__network = Network(self)

        # self.__network.register_interface(LeviathanInterface(self))

        self.start()

    def start(self):
        pass
        # self.tick_processor()
