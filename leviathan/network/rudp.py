import collections

from twisted.internet import protocol


class ConnectionMultiplexer(
    protocol.DatagramProtocol,
    collections.MutableMapping
):

    """
    Multiplexes many virtual connections over single UDP socket.
    Handles graceful shutdown of active connections.
    """

    def __init__(self):
        super(ConnectionMultiplexer, self).__init__()
        self.port = None
        self._active_connections = {}
        self.addr = None

    def startProtocol(self):
        super(ConnectionMultiplexer, self).startProtocol()
        self.port = self.transport.getHost().port

    def __len__(self):
        return len(self._active_connections)

    def __getitem__(self, addr):
        return self._active_connections[addr]

    def __setitem__(self, addr, con):
        prev_con = self._active_connections.get(addr)
        if prev_con is not None:
            prev_con.shutdown()
        self._active_connections[addr] = con

    def __delitem__(self, addr):
        del self._active_connections[addr]

    def __iter__(self):
        return iter(self._active_connections)

    def datagramReceived(self, datagram, addr):
        print(datagram, addr)
        self.addr = addr

    def send_datagram(self, datagram, addr):
        self.transport.write(datagram, addr)
