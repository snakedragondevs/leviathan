from leviathan.raklib.raklib import RakLib
from leviathan.raklib.server.itc_protocol import ITCProtocol
from leviathan.utils.binary import Binary


class ServerHandler:

    def __init__(self, server, instance):
        self._server = server
        self.instance = instance

    def send_encapsulated(self, identifier, packet, flags=RakLib.PRIORITY_NORMAL):
        # todo encapsulated protocol
        buffer = chr(ITCProtocol.PACKET_ENCAPSULATED) + str(Binary.write_int(identifier)) + chr(flags) + packet.to_internal_binary()
        self._server.push_main_to_thread_packet(buffer)
