from leviathan.network.advance_source_interface import AdvanceSourceInterface
from leviathan.raknet.server.raknet_server import RaknetServer
from leviathan.raknet.server.server_handler import ServerHandler
from leviathan.raknet.server.server_instance import ServerInstance


class RaknetInterface(ServerInstance, AdvanceSourceInterface):
    network = None

    def __init__(self, server):
        self.server = server

        self.raknet = RaknetServer(19136, '0.0.0.0')
        self.handler = ServerHandler(self.raknet, self)

    def set_network(self, network):
        self.network = network

    def process(self) -> bool:
        work = False

        if self.handler.handle_packet():
            work = True
            while self.handler.handle_packet():
                pass

        return work

