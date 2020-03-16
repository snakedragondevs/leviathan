"""Simple heap used as reorder buffer for received packets."""

import collections
import heapq


class Heap(collections.Container, collections.Sized):

    """
    A min-heap for packets implementing total ordering.
    The packet with the minimum sequence number is always at the
    front of the sequence, i.e at index 0.
    """

    def __init__(self):
        """Create a new (empty) Heap."""
        self._heap = []
        self._seqnum_set = set()

    def __contains__(self, sequence_number):
        """
        Check whether the Heap contains a packet with given seqnum.
        Args:
            sequence_number: The sequence_number, as an integer.
        """
        return sequence_number in self._seqnum_set

    def __len__(self):
        """Return the size of the heap."""
        return len(self._heap)

    def push(self, rudp_packet):
        """
        Push a new packet in the heap.
        Args:
            rudp_packet: A packet.Packet.
        """
        if rudp_packet.sequence_number not in self._seqnum_set:
            heapq.heappush(self._heap, rudp_packet)
            self._seqnum_set.add(rudp_packet.sequence_number)

    def _pop_min(self):
        """Pop the packet at the top of the heap."""
        rudp_packet = heapq.heappop(self._heap)
        self._seqnum_set.remove(rudp_packet.sequence_number)
        return rudp_packet

    def pop_min_and_all_fragments(self):
        """
        Attempt to pop the packet at the top, and its fragments.
        For the operation to succedd, all the fragments of the minimum
        packet should reside in the heap. If so, all fragments are
        popped from the heap and returned in order.
        Returns:
            Tuple of packet.Packet(s), ordered by increasing seqnum,
            or None if operation was unsuccessful for any reason.
        """
        if not self._heap:
            return None

        min_packet = self._heap[0]
        fragments_seqnum_set = set(
            min_packet.sequence_number + i
            for i in range(min_packet.more_fragments + 1)
        )
        if not fragments_seqnum_set.issubset(self._seqnum_set):
            return None

        # If all the requirements are satisfied, then, because the
        # fragments have 'sequential' sequence numbers, we can get all
        # of them with repeated calls to `_pop_min`.
        return tuple(
            self._pop_min()
            for _ in range(min_packet.more_fragments + 1)
        )
