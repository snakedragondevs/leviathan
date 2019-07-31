import threading

from logzero import logger

from leviathan.network import Network


class Server:

    def __init__(self, data_path, plugin_path):
        self.is_running = True
        self.current_thread = threading.currentThread()

        # instantiate network
        self.__network = Network(self)
