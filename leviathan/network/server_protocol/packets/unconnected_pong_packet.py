from leviathan.network.constants import OFFLINE_MESSAGE_DATA_ID
from leviathan.network.packet import Packet
from leviathan.utils.binary import Binary


class UnconnectedPongPacket(Packet):

    def __init__(self, ping_id, server_id, string):
        self.packet_id = b'\x1c'
        self.ping_id = ping_id
        self.server_id = server_id
        self.string = string
        self.packet = b''

    def encode(self):
        string_to_bytearray = str.encode(self.string)
        return self.packet.join([
            self.packet_id,
            Binary.write_long_long(self.ping_id),
            Binary.write_long_long(self.server_id),
            OFFLINE_MESSAGE_DATA_ID,
            Binary.write_short(len(string_to_bytearray)),
            string_to_bytearray
        ])

    def decode(self):
        pass
