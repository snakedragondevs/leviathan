import unittest

from leviathan.network.engine import heap, packet


class TestHeapAPI(unittest.TestCase):

    def test_init(self):
        h = heap.Heap()
        self.assertEqual(len(h), 0)

    @staticmethod
    def _make_packet_with_seqnum(seqnum):
        return packet.Packet.from_data(
            seqnum,
            ('123.45.67.89', 12345),
            ('98.76.54.32', 54321)
        )

    def test_push(self):
        p1 = self._make_packet_with_seqnum(1)
        p2 = self._make_packet_with_seqnum(2)
        h = heap.Heap()
        self.assertEqual(len(h), 0)
        h.push(p1)
        self.assertEqual(len(h), 1)
        self.assertIn(p1.sequence_number, h)
        self.assertNotIn(p2.sequence_number, h)

    def test_pop_all_fragments_from_empty_heap(self):
        h = heap.Heap()
        self.assertIsNone(h.pop_min_and_all_fragments())

    def test_pop_all_fragments_with_fragments_missing(self):
        p1 = self._make_packet_with_seqnum(1)
        p2 = self._make_packet_with_seqnum(2)
        p4 = self._make_packet_with_seqnum(4)
        p1.more_fragments = 3
        p2.more_fragments = 2
        p4.more_fragments = 0

        h = heap.Heap()
        h.push(p2)
        h.push(p4)
        h.push(p1)

        self.assertIsNone(h.pop_min_and_all_fragments())

        self.assertEqual(len(h), 3)
        self.assertIn(1, h)
        self.assertIn(2, h)
        self.assertIn(4, h)
        self.assertNotIn(3, h)

    def test_pop_all_fragments_with_all_fragments_available(self):
        p1 = self._make_packet_with_seqnum(1)
        p2 = self._make_packet_with_seqnum(2)
        p3 = self._make_packet_with_seqnum(3)
        p4 = self._make_packet_with_seqnum(4)
        p1.more_fragments = 2
        p2.more_fragments = 1
        p3.more_fragments = 0

        h = heap.Heap()
        h.push(p2)
        h.push(p3)
        h.push(p4)
        h.push(p1)

        packet_list = h.pop_min_and_all_fragments()
        self.assertEqual(packet_list, (p1, p2, p3))

        self.assertEqual(len(h), 1)
        self.assertNotIn(1, h)
        self.assertNotIn(2, h)
        self.assertNotIn(3, h)
        self.assertIn(4, h)
