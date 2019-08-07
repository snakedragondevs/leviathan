import random

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from leviathan.network.constants import OFFLINE_MESSAGE_DATA_ID
from leviathan.network.reliable_udp import ConnectionMultiplexer
from leviathan.network.server_protocol.packets.unconnected_pong_packet import UnconnectedPongPacket


class Heartbeat(DatagramProtocol):

    def datagramReceived(self, datagram, addr):
        print('received in receiver', datagram, addr)

        packet_id = datagram[0]


class Server:

    def __init__(self):

        self.server_id = random.randint(10000000, 99999999)

        # listen to pings
        connection_multiplexer = ConnectionMultiplexer()
        # server_id = random.randint(10000000, 99999999)
        # string = 'MCPE;Leviathan Server;361;1.12.0;0;20;{};name;Survival'.format(server_id)
        # packet = UnconnectedPongPacket(0, server_id, string)
        reactor.listenUDP(19136, connection_multiplexer)

        reactor.run()
