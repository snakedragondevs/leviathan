"""
RUDP state machine implementation.
Classes:
    Connection: Endpoint of an RUDP connection
    ConnectionFactory: Creator of Connections.
"""

import abc
import collections
import enum
import random

from twisted.internet import reactor, task

from leviathan.network import constants, heap, packet


REACTOR = reactor

State = enum.Enum('State', ('CONNECTING', 'CONNECTED', 'SHUTDOWN'))


class Connection(object):

    """
    A virtual connection over UDP.
    It sequences inbound and outbound packets, acknowledges inbound
    packets, and retransmits lost outbound packets. It may also relay
    packets via other connections, to help with NAT traversal.
    """

    _Address = collections.namedtuple('Address', ['ip', 'port'])

    class ScheduledPacket(object):

        """A packet scheduled for sending or currently in flight."""

        def __init__(self, rudp_packet, timeout, timeout_cb, retries=0):
            """
            Create a new scheduled packet.
            Args:
                rudp_packet: A packet.Packet in string format.
                timeout: Seconds to wait before activating timeout_cb,
                    as an integer.
                timeout_cb: Callback to invoke upon timer expiration;
                    the callback should implement a `cancel` method.
                retries: Number of times this package has already
                    been sent, as an integer.
            """
            self.rudp_packet = rudp_packet
            self.timeout = timeout
            self.timeout_cb = timeout_cb
            self.retries = retries

        def __repr__(self):
            return '{0}({1}, {2}, {3}, {4})'.format(
                self.__class__.__name__,
                self.rudp_packet,
                self.timeout,
                self.timeout_cb,
                self.retries
            )

    def __init__(self, proto, handler, own_addr, dest_addr, relay_addr=None):
        """
        Create a new connection and register it with the protocol.
        Args:
            proto: Handler to underlying protocol.
            handler: Upstream recipient of received messages and
                handler of other events. Should minimally implement
                `receive_message` and `handle_shutdown`.
            own_addr: Tuple of local host address (ip, port).
            dest_addr: Tuple of remote host address (ip, port).
            relay_addr: Tuple of relay host address (ip, port).
        If a relay address is specified, all outgoing packets are
        sent to that adddress, but the packets contain the address
        of their final destination. This is used for routing.
        """
        self.own_addr = self._Address(*own_addr)
        self.dest_addr = self._Address(*dest_addr)
        if relay_addr is None:
            self.relay_addr = dest_addr
        else:
            self.relay_addr = self._Address(*relay_addr)

        self.handler = handler

        self._proto = proto
        self._state = State.CONNECTING

        self._next_sequence_number = random.randrange(2**16 - 2)
        self._next_expected_seqnum = 0
        self._next_delivered_seqnum = 0

        self._segment_queue = collections.deque()
        self._sending_window = collections.OrderedDict()

        self._receive_heap = heap.Heap()

        self._looping_send = task.LoopingCall(self._dequeue_outbound_message)
        self._looping_receive = task.LoopingCall(self._pop_received_packet)

        # Initiate SYN sequence after receiving any pending SYN message.
        REACTOR.callLater(0, self._send_syn)

        # Setup and immediately cancel the ACK loop; it should only
        # be activated once the connection is in CONNECTED state.
        # However, initializing here helps avoiding `is None` checks.
        self._ack_handle = REACTOR.callLater(1, self._send_ack)
        self._ack_handle.cancel()

    @property
    def state(self):
        """Get the current state."""
        return self._state

    def set_relay_address(self, relay_addr):
        """
        Change the relay address used on this connection.
        Args:
            relay_addr: Tuple of relay host address (ip, port).
        """
        self.relay_addr = self._Address(*relay_addr)

    def send_message(self, message):
        """
        Send a message to the connected remote host, asynchronously.
        If the message is too large for proper transmission over UDP,
        it is first segmented appropriately.
        Args:
            message: The message to be sent, as bytes.
        """
        for segment in self._gen_segments(message):
            self._segment_queue.append(segment)
        self._attempt_enabling_looping_send()

    def receive_packet(self, rudp_packet, from_addr):
        """
        Process received packet and update connection state.
        Called by protocol when a packet arrives for this connection.
        NOTE: It is guaranteed that this method will be called
        exactly once for each inbound packet, so it is the ideal
        place to do pre- or post-processing of any Packet.
        Consider this when subclassing Connection.
        Args:
            rudp_packet: Received packet.Packet.
            from_addr: Sender's address as Tuple (ip, port).
        """
        if self._state == State.SHUTDOWN:
            # A SHUTDOWN connection shall not process any packet
            # whatsoever. In particular, it shall not be revived via a
            # SYN packet.
            return

        if from_addr not in (rudp_packet.source_addr, self.relay_addr):
            self.set_relay_address(from_addr)

        if rudp_packet.fin:
            self._process_fin_packet(rudp_packet)
        elif rudp_packet.syn:
            if self._state == State.CONNECTING:
                self._process_syn_packet(rudp_packet)
        else:
            if self._state == State.CONNECTED:
                self._process_casual_packet(rudp_packet)

    def shutdown(self):
        """
        Terminate connection with remote endpoint.
        1. Send a single FIN packet to remote host.
        2. Stop sending and acknowledging messages.
        3. Cancel all retransmission timers.
        4. Alert handler about connection shutdown.
        The handler should prevent the connection from receiving
        any future messages. The simplest way to do this is to
        remove the connection from the protocol.
        """
        self._state = State.SHUTDOWN

        self._send_fin()
        self._cancel_ack_timeout()
        self._attempt_disabling_looping_send(force=True)
        self._attempt_disabling_looping_receive()
        self._clear_sending_window()

        self.handler.handle_shutdown()

    def unregister(self):
        """
        Remove this connection from the protocol.
        This should be called only after the connection is
        SHUTDOWN. Note that shutting down the connection will
        *not* automatically remove the connection from the
        protocol, to prevent a malicious remote node from
        creating and destroying connections endlessly.
        """
        assert self.state == State.SHUTDOWN
        del self._proto[self.dest_addr]

    @staticmethod
    def _gen_segments(message):
        """
        Split a message into segments appropriate for transmission.
        Args:
            message: The message to sent, as a string.
        Yields:
            Tuples of two elements; the first element is the number
            of remaining segments, the second is the actual string
            segment.
        """
        max_size = constants.UDP_SAFE_SEGMENT_SIZE
        count = (len(message) + max_size - 1) // max_size
        segments = (
            (count - i - 1, message[i * max_size: (i + 1) * max_size])
            for i in range(count)
        )
        return segments

    def _attempt_enabling_looping_send(self):
        """
        Enable dequeuing if a packet can be scheduled immediately.
        """
        if (
            not self._looping_send.running and
            self._state == State.CONNECTED and
            len(self._sending_window) < constants.WINDOW_SIZE and
            len(self._segment_queue)
        ):
            self._looping_send.start(0, now=True)

    def _attempt_disabling_looping_send(self, force=False):
        """
        Disable dequeuing if a packet cannot be scheduled.
        Args:
            force: If True, force disabling.
        """
        if (
            self._looping_send.running and (
                force or
                len(self._sending_window) >= constants.WINDOW_SIZE or
                not len(self._segment_queue)
            )
        ):
            self._looping_send.stop()

    def _get_next_sequence_number(self):
        """Return-then-increment the next available sequence number."""
        cur = self._next_sequence_number
        self._next_sequence_number += 1
        return cur

    def _send_syn(self):
        """
        Create and schedule the initial SYN packet.
        The current ACK number is included; if it is greater than
        0, then this actually is a SYNACK packet.
        """
        syn_packet = packet.Packet.from_data(
            self._get_next_sequence_number(),
            self.dest_addr,
            self.own_addr,
            ack=self._next_expected_seqnum,
            syn=True
        )
        self._schedule_send_in_order(syn_packet, constants.PACKET_TIMEOUT)

    def _send_ack(self):
        """
        Create and schedule a bare ACK packet.
        Bare ACK packets are sent out-of-order, do not have a
        meaningful sequence number and cannot be ACK-ed. It is of
        no use to retransmit a lost bare ACK packet, since the local
        host's ACK number may have advanced in the meantime. Instead,
        each ACK timeout sends the latest ACK number available.
        """
        ack_packet = packet.Packet.from_data(
            0,
            self.dest_addr,
            self.own_addr,
            ack=self._next_expected_seqnum
        )
        self._schedule_send_out_of_order(ack_packet)

    def _send_fin(self):
        """
        Create and schedule a FIN packet.
        No acknowledgement of this packet is normally expected.
        In addition, no retransmission of this packet is performed;
        if it is lost, the packet timeouts at the remote host will
        cause the connection to be broken. Since the packet is sent
        out-of-order, there is no meaningful sequence number.
        """
        fin_packet = packet.Packet.from_data(
            0,
            self.dest_addr,
            self.own_addr,
            ack=self._next_expected_seqnum,
            fin=True
        )
        self._schedule_send_out_of_order(fin_packet)

    def _schedule_send_out_of_order(self, rudp_packet):
        """
        Schedule a package to be sent out of order.
        Current implementation sends the packet as soon as possible.
        Args:
            rudp_packet: The packet.Packet to be sent.
        """
        final_packet = self._finalize_packet(rudp_packet)
        self._proto.send_datagram(final_packet, self.relay_addr)

    def _schedule_send_in_order(self, rudp_packet, timeout):
        """
        Schedule a package to be sent and set the timeout timer.
        Args:
            rudp_packet: The packet.Packet to be sent.
            timeout: The timeout for this packet type.
        """
        final_packet = self._finalize_packet(rudp_packet)
        seqnum = rudp_packet.sequence_number
        timeout_cb = REACTOR.callLater(0, self._do_send_packet, seqnum)
        self._sending_window[seqnum] = self.ScheduledPacket(
            final_packet,
            timeout,
            timeout_cb,
            0
        )

    def _dequeue_outbound_message(self):
        """
        Deque a message, wrap it into an RUDP packet and schedule it.
        Pause dequeueing if it would overflow the send window.
        """
        assert self._segment_queue, 'Looping send active despite empty queue.'
        more_fragments, message = self._segment_queue.popleft()

        rudp_packet = packet.Packet.from_data(
            self._get_next_sequence_number(),
            self.dest_addr,
            self.own_addr,
            message,
            more_fragments,
            ack=self._next_expected_seqnum
        )
        self._schedule_send_in_order(rudp_packet, constants.PACKET_TIMEOUT)

        self._attempt_disabling_looping_send()

    def _finalize_packet(self, rudp_packet):
        """
        Convert a packet.Packet to bytes.
        NOTE: It is guaranteed that this method will be called
        exactly once for each outbound packet, so it is the ideal
        place to do pre- or post-processing of any Packet.
        Consider this when subclassing Connection.
        Args:
            rudp_packet: A packet.Packet
        Returns:
            The protobuf-encoded version of the packet, as bytes.
        """
        return rudp_packet.to_bytes()

    def _do_send_packet(self, seqnum):
        """
        Immediately dispatch packet with given sequence number.
        The packet must have been previously scheduled, that is, it
        should reside in the send window. Upon successful dispatch,
        the timeout timer for this packet is reset and the
        retransmission counter is incremented. If the retries exceed a
        given limit, the connection is considered broken and the
        shutdown sequence is initiated. Finally, the timeout for the
        looping ACK sender is reset.
        Args:
            seqnum: Sequence number of a ScheduledPacket, as an integer.
        Raises:
            KeyError: No such packet exists in the send window; some
                invariant has been violated.
        """
        sch_packet = self._sending_window[seqnum]
        if sch_packet.retries >= constants.MAX_RETRANSMISSIONS:
            self.shutdown()
        else:
            self._proto.send_datagram(sch_packet.rudp_packet, self.relay_addr)
            sch_packet.timeout_cb = REACTOR.callLater(
                sch_packet.timeout,
                self._do_send_packet,
                seqnum
            )
            sch_packet.retries += 1
            self._cancel_ack_timeout()

    def _reset_ack_timeout(self, timeout):
        """
        Reset timeout for next bare ACK packet.
        Args:
            timeout: Seconds until a bare ACK packet is sent.
        """
        if self._ack_handle.active():
            self._ack_handle.reset(timeout)
        else:
            self._ack_handle = REACTOR.callLater(timeout, self._send_ack)

    def _cancel_ack_timeout(self):
        """Cancel timeout for next bare ACK packet."""
        if self._ack_handle.active():
            self._ack_handle.cancel()

    def _clear_sending_window(self):
        """
        Purge send window from scheduled packets.
        Cancel all retransmission timers.
        """
        for sch_packet in self._sending_window.values():
            if sch_packet.timeout_cb.active():
                sch_packet.timeout_cb.cancel()
        self._sending_window.clear()

    def _process_ack_packet(self, rudp_packet):
        """
        Process the ACK field on a received packet.
        Args:
            rudp_packet: A packet.Packet with positive ACK field.
        """
        if self._sending_window:
            self._retire_packets_with_seqnum_up_to(
                min(rudp_packet.ack, self._next_sequence_number)
            )

    def _process_fin_packet(self, rudp_packet):
        """
        Process a received FIN packet.
        Terminate connection after possibly dispatching any
        last messages to handler.
        Args:
            rudp_packet: A packet.Packet with FIN flag set.
        """
        self.shutdown()

    def _process_casual_packet(self, rudp_packet):
        """
        Process received packet.
        This method can only be called if the connection has been
        established; ignore status of SYN flag.
        Args:
            rudp_packet: A packet.Packet with SYN and FIN flags unset.
        """
        if rudp_packet.ack > 0:
            self._process_ack_packet(rudp_packet)

        seqnum = rudp_packet.sequence_number
        if seqnum > 0:
            self._reset_ack_timeout(constants.BARE_ACK_TIMEOUT)
            if seqnum >= self._next_expected_seqnum:
                self._receive_heap.push(rudp_packet)
                if seqnum == self._next_expected_seqnum:
                    self._next_expected_seqnum += 1
                    self._attempt_enabling_looping_receive()

    def _process_syn_packet(self, rudp_packet):
        """
        Process received SYN packet.
        This method can only be called if the connection has not yet
        been established; thus ignore any payload.
        We use double handshake and consider the connection to the
        remote endpoint established upon receiving a SYN packet.
        Args:
            rudp_packet: A packet.Packet with SYN flag set.
        """
        if rudp_packet.ack > 0:
            self._process_ack_packet(rudp_packet)

        self._update_next_expected_seqnum(rudp_packet.sequence_number)
        self._update_next_delivered_seqnum(rudp_packet.sequence_number)
        self._state = State.CONNECTED
        self._attempt_enabling_looping_send()

    def _update_next_expected_seqnum(self, seqnum):
        if self._next_expected_seqnum <= seqnum:
            self._next_expected_seqnum = seqnum + 1

    def _update_next_delivered_seqnum(self, seqnum):
        if self._next_delivered_seqnum <= seqnum:
            self._next_delivered_seqnum = seqnum + 1

    def _retire_packets_with_seqnum_up_to(self, acknum):
        """
        Remove from send window any ACKed packets.
        Args:
            acknum: Acknowledgement number of next expected
                outbound packet.
        """
        if not self._sending_window:
            return
        lowest_seqnum = iter(self._sending_window).next()
        if acknum >= lowest_seqnum:
            for seqnum in range(lowest_seqnum, acknum):
                self._retire_scheduled_packet_with_seqnum(seqnum)
            self._attempt_enabling_looping_send()

    def _retire_scheduled_packet_with_seqnum(self, seqnum):
        """
        Retire ScheduledPacket with given seqnum.
        Args:
            seqnum: Sequence number of retired packet.
        """
        sch_packet = self._sending_window.pop(seqnum)
        sch_packet.timeout_cb.cancel()

    def _attempt_enabling_looping_receive(self):
        """Activate looping receive."""
        if (
            not self._looping_receive.running and
            self._state == State.CONNECTED and
            self._receive_heap
        ):
            self._looping_receive.start(0, now=True)

    def _attempt_disabling_looping_receive(self):
        """Deactivate looping receive."""
        if self._looping_receive.running:
            self._looping_receive.stop()

    def _pop_received_packet(self):
        """
        Attempt to reconstruct a received packet and process payload.
        If successful, advance ACK number.
        """
        fragments = self._receive_heap.pop_min_and_all_fragments()
        if fragments is None:
            self._attempt_disabling_looping_receive()
        else:
            last_seqnum = fragments[-1].sequence_number
            self._update_next_expected_seqnum(last_seqnum)
            self._update_next_delivered_seqnum(last_seqnum)
            payload = ''.join(f.payload for f in fragments)
            self.handler.receive_message(payload)

            if self._next_delivered_seqnum not in self._receive_heap:
                self._attempt_disabling_looping_receive()


class Handler(object):

    """
    Abstract base class for handler objects.
    Each Connection should be linked to one such object.
    """

    __metaclass__ = abc.ABCMeta

    connection = None

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """Create a new Handler."""

    @abc.abstractmethod
    def receive_message(self, message):
        """
        Receive a message from the given connection.
        Args:
            message: The payload of a Packet, as a string.
        """

    @abc.abstractmethod
    def handle_shutdown(self):
        """Handle connection shutdown."""


class HandlerFactory(object):

    """Abstract base class for handler factory."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """Create a new HandlerFactory."""

    @abc.abstractmethod
    def make_new_handler(self, *args, **kwargs):
        """Create a new handler."""


class ConnectionFactory(object):

    """
    A factory for Connections.
    Subclass according to need.
    """

    def __init__(self, handler_factory):
        """
        Create a new ConnectionFactory.
        Args:
            handler_factory: An instance of a HandlerFactory,
                providing a `make_new_handler` method.
        """
        self.handler_factory = handler_factory

    def make_new_connection(
        self,
        proto_handle,
        own_addr,
        source_addr,
        relay_addr
    ):
        """
        Create a new Connection.
        In addition, create a handler and attach the connection to it.
        """
        handler = self.handler_factory.make_new_handler(
            own_addr,
            source_addr,
            relay_addr
        )
        connection = Connection(
            proto_handle,
            handler,
            own_addr,
            source_addr,
            relay_addr
        )
        handler.connection = connection
        return connection
