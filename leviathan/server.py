import threading

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from logzero import logger

from leviathan.network import Network


class Echo(DatagramProtocol):

    def datagramReceived(self, datagram, address):
        print("received %r from %s" % (datagram, address))
        self.transport.write('reply example'.encode(), address)


class Server:

    def __init__(self, data_path, plugin_path):
        self.is_running = True
        self.current_thread = threading.currentThread()

        self.__network = Network(self)

        self.start()

    def start(self):
        pass
        # self.tick_processor()
