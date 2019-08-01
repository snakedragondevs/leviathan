import threading

from logzero import logger

from leviathan.network import Network


class LeviathanCore:

    def __init__(self, data_path, plugin_path):
        self.is_running = True
        self.current_thread = threading.currentThread()

        # instantiate network
        self.__network = Network(self)
