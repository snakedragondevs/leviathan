import unittest

import six

from leviathan.network.engine import packet


class TestPacketAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.dest_addr = ('123.45.67.89', 12345)
        cls.source_addr = ('132.45.67.89', 54321)

    def test_from_data_with_minimal_parametres(self):
        p = packet.Packet.from_data(1, self.dest_addr, self.source_addr)
        self.assertEqual(p.sequence_number, 1)
        self.assertEqual(p.dest_addr, self.dest_addr)
        self.assertEqual(p.source_addr, self.source_addr)
        self.assertEqual(p.payload, b'')
        self.assertEqual(p.more_fragments, 0)
        self.assertEqual(p.ack, 0)
        self.assertFalse(p.fin)
        self.assertFalse(p.syn)

    def test_from_data_with_all_parametres(self):
        p = packet.Packet.from_data(
            sequence_number=1,
            dest_addr=self.dest_addr,
            source_addr=self.source_addr,
            payload=b'Yellow submarine',
            more_fragments=4,
            ack=28,
            fin=True,
            syn=True
        )
        self.assertEqual(p.sequence_number, 1)
        self.assertEqual(p.dest_addr, self.dest_addr)
        self.assertEqual(p.source_addr, self.source_addr)
        self.assertEqual(p.payload, b'Yellow submarine')
        self.assertEqual(p.more_fragments, 4)
        self.assertEqual(p.ack, 28)
        self.assertTrue(p.fin)
        self.assertTrue(p.syn)

    def _make_packet_with_seqnum(self, seqnum):
        return packet.Packet.from_data(seqnum, self.dest_addr, self.source_addr)

    def test_ordering(self):
        p1 = self._make_packet_with_seqnum(1)
        p2 = self._make_packet_with_seqnum(2)
        p3 = self._make_packet_with_seqnum(1)

        self.assertEqual(p1, p1)
        self.assertNotEqual(p1, p2)
        self.assertEqual(p1, p3)

        self.assertGreater(p2, p1)
        self.assertLess(p1, p2)

        self.assertGreaterEqual(p1, p1)
        self.assertLessEqual(p1, p1)

    def _assert_packets_entirely_equal(self, p1, p2):
        self.assertEqual(p1.sequence_number, p2.sequence_number)
        self.assertEqual(p1.dest_addr, p2.dest_addr)
        self.assertEqual(p1.source_addr, p2.source_addr)
        self.assertEqual(p1.payload, p2.payload)
        self.assertEqual(p1.more_fragments, p2.more_fragments)
        self.assertEqual(p1.ack, p2.ack)
        self.assertEqual(p1.fin, p2.fin)
        self.assertEqual(p1.syn, p2.syn)

    def test_serialization_and_deserialization(self):
        p1 = packet.Packet.from_data(
            sequence_number=1,
            dest_addr=self.dest_addr,
            source_addr=self.source_addr,
            payload=b'Yellow submarine',
            more_fragments=4,
            ack=28,
            fin=True,
            syn=True
        )
        bytes1 = p1.to_bytes()
        self.assertIsInstance(bytes1, six.binary_type)

        p2 = packet.Packet.from_bytes(bytes1)
        self._assert_packets_entirely_equal(p1, p2)

    def _assert_packet_fails_validation(self, rudp_packet):
        with self.assertRaises(packet.ValidationError):
            packet.Packet.validate(rudp_packet)

    def test_validate_with_bad_dest_ip(self):
        p = packet.Packet.from_data(1, self.dest_addr, self.source_addr)

        p.dest_addr = ('127.0', 1)
        self._assert_packet_fails_validation(p)

        p.dest_addr = ('FE80:0000:0000::z:B3FF:FE1E:8329', 1)
        self._assert_packet_fails_validation(p)

    def test_validate_with_bad_dest_port(self):
        p = packet.Packet.from_data(1, self.dest_addr, self.source_addr)

        p.dest_addr = ('127.0.0.1', 0)
        self._assert_packet_fails_validation(p)

        p.dest_addr = ('127.0.0.1', 65536)
        self._assert_packet_fails_validation(p)

    def test_validate_with_bad_source_ip(self):
        p = packet.Packet.from_data(1, self.source_addr, self.source_addr)

        p.source_addr = ('127.0', 1)
        self._assert_packet_fails_validation(p)

        p.source_addr = ('FE80:0000:0000::z:B3FF:FE1E:8329', 1)
        self._assert_packet_fails_validation(p)

    def test_validate_with_bad_source_port(self):
        p = packet.Packet.from_data(1, self.source_addr, self.source_addr)

        p.source_addr = ('127.0.0.1', 0)
        self._assert_packet_fails_validation(p)

        p.source_addr = ('127.0.0.1', 65536)
        self._assert_packet_fails_validation(p)
