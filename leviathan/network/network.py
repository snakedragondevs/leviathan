from leviathan.network.raknet_interface import RaknetInterface
from leviathan.network.source_iterface import SourceInterface


class Network:

    interfaces = set()

    upload = 0
    download = 0

    def __init__(self, server):
        self.server = server

    def process_interface(self):
        interface: SourceInterface
        for interface in self.interfaces:
            try:
                interface.process()
            except Exception as e:
                print(e)

    def register_interface(self, interface: RaknetInterface):
        self.interfaces.add(interface)
        interface.set_network(self)

