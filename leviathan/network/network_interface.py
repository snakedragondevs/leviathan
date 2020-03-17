from logzero import logger
import mock
from leviathan.network.engine import connection, rudp


class NetworkInterface:

    def __init__(self):
        print('interface initialized')
        connection_factory = mock.Mock(spec_set=connection.ConnectionFactory)
        self.connection_multiplexer = rudp.ConnectionMultiplexer(
            connection_factory,
            '123.45.67.89',
            logger=logger
        )

    def process(self):
        print('process is ticking')

    def shutdown(self):
        self.connection_multiplexer.shutdown()

    def emergency_shutdown(self):
        self.connection_multiplexer.shutdown()
