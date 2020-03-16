#! /usr/bin/env python

import collections
import random
import time

from leviathan.network.engine import rudp, constants, connection


class StubHandler(connection.Handler):

    def __init__(self):
        super(StubHandler, self).__init__()
        self.shutdown = False
        self.received_count = 0
        self.last_message = None

    def receive_message(self, message):
        self.received_count += 1
        self.last_message = message

    def handle_shutdown(self):
        self.shutdown = True


class StubHandlerFactory(connection.HandlerFactory):

    def __init__(self, *args, **kwargs):
        super(StubHandlerFactory, self).__init__(*args, **kwargs)

    def make_new_handler(self, *args, **kwargs):
        return StubHandler()


class BenchmarkLocalFullDuplex(object):

    def __init__(self, cm):
        self.port = 53241
        self.addr1 = ('127.0.0.1', 12345)
        self.addr2 = ('127.0.0.1', 13245)
        self.relay_addr = ('127.0.0.1', 53241)

        self.con1 = cm.make_new_connection(
            self.addr1,
            self.addr2,
            self.relay_addr
        )
        self.con2 = cm.make_new_connection(
            self.addr2,
            self.addr1,
            self.relay_addr
        )

        self.socket_handle = connection.REACTOR.listenUDP(
            port=self.relay_addr[1],
            protocol=cm,
            interface=self.relay_addr[0]
        )

    def run(self, repetitions, timeout):
        connection.REACTOR.callLater(timeout, self.stop)
        self.stuff_connections(repetitions)
        connection.REACTOR.run()

    def packet_from_repetition(self, rep):
        return str(rep)

    def stuff_connections(self, repetitions):
        for i in range(repetitions):
            self.con1.send_message(self.packet_from_repetition(i))
            self.con2.send_message(self.packet_from_repetition(i))

    def stop(self):
        connection.REACTOR.stop()


class BenchmarkLocalFullDuplexBigPacket(
    BenchmarkLocalFullDuplex
):
    big_message = constants.UDP_SAFE_SEGMENT_SIZE * 'a'

    def packet_from_repetition(self, rep):
        return self.big_message


class BenchmarkLocalFullDuplexOversizedPacket(
    BenchmarkLocalFullDuplex
):
    oversized_message = 20 * constants.UDP_SAFE_SEGMENT_SIZE * 'a'

    def packet_from_repetition(self, rep):
        return self.oversized_message


class BadConnectionMultiplexer(rudp.ConnectionMultiplexer):

    pass_prob = 99

    def __init__(self, *args, **kwargs):
        super(BadConnectionMultiplexer, self).__init__(*args, **kwargs)
        self._queue_dict = collections.defaultdict(collections.deque)

    def send_datagram(self, datagram, addr):
        """Simulate a bad channel that randomly drops packets."""
        if self.pass_prob > random.randrange(0, 100):
            super(BadConnectionMultiplexer, self).send_datagram(datagram, addr)


def main():
    cf = connection.CryptoConnectionFactory(StubHandlerFactory())
    cm = BadConnectionMultiplexer(cf, '127.0.0.1', relaying=False)
    benchmark = BenchmarkLocalFullDuplexBigPacket(cm)
    sec_start = int(time.time())
    benchmark.run(20000, 10)
    sec_end = int(time.time())

    rec1 = benchmark.con1.handler.received_count
    rec2 = benchmark.con2.handler.received_count
    duration = sec_end - sec_start

    print(
        """Stats:
            Duration: {0} seconds
            Connection 1: Received {1} packets; {2} packets/second
            Connection 2: Received {3} packets; {4} packets/second
            """.format(
            duration, rec1, rec1 / duration, rec2, rec2 / duration
        )
    )


if __name__ == '__main__':
    main()
