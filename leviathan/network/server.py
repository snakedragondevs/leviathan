import random

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from leviathan.network.constants import OFFLINE_MESSAGE_DATA_ID
from leviathan.network.rudp import ConnectionMultiplexer
from leviathan.utils.binary import Binary


# class Heartbeat(DatagramProtocol):
#
#     def datagramReceived(self, datagram, addr):
#         print('received in receiver', datagram, addr)
#
#         packet_id = datagram[0]
#         server_id = random.randint(10000000, 99999999)
#         string = 'MCPE;Leviathan Server;361;1.12.0;0;20;{};name;Survival'.format(server_id)
#
#         packet = b''.join([
#             b'\x1c',
#             Binary.write_long_long(0),
#             Binary.write_long_long(random.randint(10000000, 99999999)),
#             Binary.write_short(len(string)),
#             string.encode()
#         ])
#         self.transport.write(packet, addr)



class Server:

    raknet_server = None

    def __init__(self):
        self.raknet_server = None
        # self.server_id = random.randint(10000000, 99999999)
        # listen to pings
        # server_id = random.randint(10000000, 99999999)
        # string = 'MCPE;Leviathan Server;361;1.12.0;0;20;{};name;Survival'.format(server_id)
        # packet = UnconnectedPongPacket(0, server_id, string)

        # reactor.listenUDP(19136, connection_multiplexer)
        # reactor.listenUDP(19136, Heartbeat())
        #
        # reactor.run()
