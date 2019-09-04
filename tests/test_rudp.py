import collections
import logging
import unittest

import mock
from twisted.internet import address, protocol, udp

from leviathan.network import connection, packet, rudp


class TestConnectionManagerAPI(unittest.TestCase):  # todo TypeError: '' has type str, but expected one of: bytes

    @classmethod
    def setUpClass(cls):
        cls.public_ip = '123.45.67.89'
        cls.port = 12345
        cls.addr1 = (cls.public_ip, cls.port)
        cls.addr2 = ('132.54.76.98', 54321)
        cls.addr3 = ('231.76.45.89', 15243)

    def _make_cm(self):
        cf = mock.Mock(spec_set=connection.ConnectionFactory)
        return rudp.ConnectionMultiplexer(
            cf,
            self.public_ip,
            logger=logging.Logger('CM')
        )

    def test_default_init(self):
        cf = mock.Mock()
        cm = rudp.ConnectionMultiplexer(cf, self.public_ip)
        self.assertIsInstance(cm, protocol.DatagramProtocol)
        self.assertIsInstance(cm, collections.MutableMapping)
        self.assertEqual(cm.public_ip, self.public_ip)
        self.assertIsNone(cm.port)
        self.assertFalse(cm.relaying)
        self.assertEqual(len(cm), 0)

    def test_full_init(self):
        cf = mock.Mock()
        cm = rudp.ConnectionMultiplexer(
            connection_factory=cf,
            public_ip=self.public_ip,
            relaying=True,
            logger=logging.Logger('CM')
        )
        self.assertEqual(cm.public_ip, self.public_ip)
        self.assertIsNone(cm.port)
        self.assertTrue(cm.relaying)

    def test_get_nonexistent_connection(self):
        cm = self._make_cm()
        self.assertNotIn(self.addr1, cm)
        with self.assertRaises(KeyError):
            _ = cm[self.addr1]

    def test_set_and_get_new_connection(self):
        cm = self._make_cm()
        mock_connection = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection
        self.assertIn(self.addr1, cm)
        self.assertIs(cm[self.addr1], mock_connection)

    def test_set_existent_connection(self):
        cm = self._make_cm()
        mock_connection1 = mock.Mock(spec_set=connection.Connection)
        mock_connection2 = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection1
        cm[self.addr1] = mock_connection2
        self.assertIn(self.addr1, cm)
        self.assertIs(cm[self.addr1], mock_connection2)
        mock_connection1.shutdown.assert_called_once_with()
        mock_connection2.shutdown.assert_not_called()

    def test_del_nonexistent_connection(self):
        cm = self._make_cm()
        self.assertNotIn(self.addr1, cm)
        with self.assertRaises(KeyError):
            del cm[self.addr1]

    def test_del_existent_connection(self):
        cm = self._make_cm()
        mock_connection = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection
        del cm[self.addr1]
        self.assertNotIn(self.addr1, cm)

    def test_iter(self):
        cm = self._make_cm()
        mock_connection1 = mock.Mock(spec_set=connection.Connection)
        mock_connection2 = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection1
        cm[self.addr2] = mock_connection2
        self.assertEqual(set(cm), {self.addr1, self.addr2})

    def test_receive_bad_protobuf_datagram(self):
        cm = self._make_cm()
        mock_connection = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection
        datagram = '!@#4noise%^&*'
        cm.datagramReceived(datagram, self.addr1)
        mock_connection.receive_packet.assert_not_called()

    def test_receive_bad_rudp_datagram(self):
        cm = self._make_cm()
        mock_connection = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection
        datagram = packet.Packet.from_data(
            1,
            ('127.0.0.1', 2**20),  # Bad port value
            self.addr1
        ).to_bytes()

        cm.datagramReceived(datagram, self.addr1)
        mock_connection.receive_packet.assert_not_called()

    def test_receive_from_banned_ip(self):
        cm = self._make_cm()
        cm.ban_ip(self.addr1[0])

        datagram = '!@#4noise%^&*'
        cm.datagramReceived(datagram, self.addr1)
        cm.connection_factory.make_new_connection.assert_not_called()

        datagram = packet.Packet.from_data(
            1,
            self.addr2,
            self.addr1
        ).to_bytes()
        cm.datagramReceived(datagram, self.addr3)
        cm.connection_factory.make_new_connection.assert_not_called()

        source_addr = self.addr1
        mock_connection = cm.make_new_connection(
            (self.public_ip, self.port),
            source_addr
        )
        cm[source_addr] = mock_connection
        rudp_packet = packet.Packet.from_data(
            1,
            (self.public_ip, self.port),
            source_addr
        )
        datagram = rudp_packet.to_bytes()

        cm.datagramReceived(datagram, source_addr)
        mock_connection.receive_packet.assert_not_called()

    def _make_connected_cm(self):
        cm = self._make_cm()
        transport = mock.Mock(spec_set=udp.Port)
        ret_val = address.IPv4Address('UDP', self.public_ip, self.port)
        transport.attach_mock(mock.Mock(return_value=ret_val), 'getHost')
        cm.makeConnection(transport)
        return cm

    def test_receive_relayed_datagram_but_not_relaying(self):
        cm = self._make_connected_cm()

        dest_ip = '231.54.67.89'  # not the same as self.public_ip
        source_addr = self.addr1
        datagram = packet.Packet.from_data(
            1,
            (dest_ip, 12345),
            source_addr
        ).to_bytes()

        cm.datagramReceived(datagram, source_addr)
        self.assertNotIn((dest_ip, 12345), cm)
        cm.transport.write.assert_not_called()
        cm.connection_factory.make_new_connection.assert_not_called()

    def test_receive_relayed_datagram_while_relaying(self):
        cm = self._make_connected_cm()
        cm.relaying = True

        dest_ip = '231.54.67.89'  # not the same as self.public_ip
        source_addr = self.addr1
        datagram = packet.Packet.from_data(
            1,
            (dest_ip, 12345),
            source_addr
        ).to_bytes()

        cm.datagramReceived(datagram, source_addr)
        self.assertNotIn((dest_ip, 12345), cm)
        cm.transport.write.assert_called_once_with(datagram, (dest_ip, 12345))
        cm.connection_factory.make_new_connection.assert_not_called()

    def test_receive_datagram_in_existing_connection(self):
        cm = self._make_connected_cm()

        source_addr = self.addr3
        mock_connection = cm.make_new_connection(
            (self.public_ip, self.port),
            source_addr
        )
        cm[source_addr] = mock_connection
        rudp_packet = packet.Packet.from_data(
            1,
            (self.public_ip, self.port),
            source_addr
        )
        datagram = rudp_packet.to_bytes()

        cm.datagramReceived(datagram, source_addr)
        # cm.connection_factory.make_new_connection.assert_not_called()
        mock_connection.receive_packet.assert_called_once_with(rudp_packet, source_addr)

    def test_receive_datagram_in_new_connection(self):
        cm = self._make_connected_cm()

        source_addr = self.addr3
        rudp_packet = packet.Packet.from_data(
            1,
            (self.public_ip, self.port),
            source_addr,
            syn=True
        )
        datagram = rudp_packet.to_bytes()

        cm.datagramReceived(datagram, source_addr)
        cm.connection_factory.make_new_connection.assert_called_once_with(
            cm,
            (self.public_ip, self.port),
            source_addr,
            source_addr
        )
        self.assertIn(source_addr, cm)
        mock_connection = cm[source_addr]
        mock_connection.receive_packet.assert_called_once_with(rudp_packet, source_addr)

    def test_receive_datagram_in_new_relayed_connection(self):
        cm = self._make_connected_cm()

        source_addr = self.addr3
        relay_addr = self.addr3
        rudp_packet = packet.Packet.from_data(
            1,
            (self.public_ip, self.port),
            source_addr,
            syn=True
        )
        datagram = rudp_packet.to_bytes()

        cm.datagramReceived(datagram, relay_addr)
        cm.connection_factory.make_new_connection.assert_called_once_with(
            cm,
            (self.public_ip, self.port),
            source_addr,
            relay_addr
        )
        self.assertIn(source_addr, cm)
        mock_connection = cm[source_addr]
        mock_connection.receive_packet.assert_called_once_with(rudp_packet, relay_addr)

    def test_make_new_connection(self):
        cm = self._make_cm()
        cm.make_new_connection(self.addr1, self.addr2)
        self.assertIn(self.addr2, cm)
        cm.connection_factory.make_new_connection.assert_called_once_with(
            cm,
            self.addr1,
            self.addr2,
            None
        )

    def test_make_new_relaying_connection(self):
        cm = self._make_cm()
        cm.make_new_connection(self.addr1, self.addr2, self.addr3)
        self.assertIn(self.addr2, cm)
        cm.connection_factory.make_new_connection.assert_called_once_with(
            cm,
            self.addr1,
            self.addr2,
            self.addr3
        )

    def test_send_datagram(self):
        transport = mock.Mock()
        cm = self._make_cm()
        cm.makeConnection(transport)
        rudp_packet = packet.Packet.from_data(
            1,
            ('132.54.76.98', 23456),
            (self.public_ip, self.port)
        )
        datagram = rudp_packet.to_bytes()

        cm.send_datagram(datagram, ('132.54.76.98', 23456))
        transport.write.assert_called_once_with(
            datagram,
            ('132.54.76.98', 23456)
        )

    def test_shutdown(self):
        cm = self._make_cm()
        mock_connection1 = mock.Mock(spec_set=connection.Connection)
        mock_connection2 = mock.Mock(spec_set=connection.Connection)
        cm[self.addr1] = mock_connection1
        cm[self.addr2] = mock_connection2

        transport = mock.Mock()
        cm.makeConnection(transport)

        cm.shutdown()
        mock_connection1.shutdown.assert_called_once_with()
        mock_connection2.shutdown.assert_called_once_with()
        transport.loseConnection.assert_called_once_with()
