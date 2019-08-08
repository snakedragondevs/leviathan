"""
Specification of RUDP packet structure.
Classes:
    Packet: An RUDP packet implementing a total ordering and
        serializing to/from protobuf.
"""

import functools
import re

from leviathan.network import packet_pb2

# IP validation regexes from the Regular Expressions Cookbook.
# For now, only standard (non-compressed) IPv6 addresses are
# supported. This might change in the future.
_IPV4_REGEX = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
_IPV6_REGEX = r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$'

_IP_MATCHER = re.compile('({0})|({1})'.format(_IPV4_REGEX, _IPV6_REGEX))


class ValidationError(Exception):

    """Exception raised due to invalid data (e.g. bad IP)."""


@functools.total_ordering
class Packet(object):

    """
    An RUDP packet.
    This class serves as a wrapper class for the protobuf
    serialization class. The wrapping is necessary in order to
    enable extra functionality (e.g. total ordering) without
    disrupting the metaclass of the protobuf class.
    """

    def __init__(self):
        """Create a new empty Packet."""
        self._packet = packet_pb2.Packet()

    @classmethod
    def from_data(
        cls,
        sequence_number,
        dest_addr,
        source_addr,
        payload='',
        more_fragments=0,
        ack=0,
        fin=False,
        syn=False,
    ):
        """
        Create a Packet with the given fields.
        Args:
            sequence_number: The packet's sequence number, as an int.
            dest_addr: Tuple of destination addres (ip, port).
            source_addr: Tuple of local host addres (ip, port).
            payload: The packet's payload, as a string.
            more_fragments: The number of segments that follow this
                packet and are delivering remaining parts of the same
                payload.
            ack: If positive, it is the acknowledgement number of
                the next packet the receiver is expecting. Otherwise,
                ignore.
            fin: When True, signals that this packet ends the connection.
            syn: When True, signals the start of a new conenction.
        Return:
            An initialized Packet.
        Raises:
            TypeError: Some assignment failed due to value being
                of inappropriate type.
        NOTE: The destination address may not be the address of the
        first recipient of this packet in case where the recipient is
        a mediator node relaying packets (e.g. for NAT punching).
        """
        new_packet = cls()
        new_packet.syn = syn
        new_packet.fin = fin
        new_packet.sequence_number = sequence_number
        new_packet.more_fragments = more_fragments
        new_packet.ack = ack

        new_packet.payload = payload

        new_packet.dest_addr = dest_addr
        new_packet.source_addr = source_addr

        return new_packet

    def to_bytes(self):
        """
        Return a serialized version of this packet.
        Returns:
            A protobuf-encoded bytestring.
        Raises:
            protobuf.message.EncodeError: Serialization was
                unsuccessful; maybe the object attributes have
                not been instatiated with proper values.
        """
        return self._packet.SerializeToString()

    @classmethod
    def from_bytes(cls, data):
        """
        Create a Packet from an unvalidated bytestring.
        Args:
            data: A protobuf-encoded bytestring.
        Returns:
            A new Packet instance, populated with the contents
            of the bytestring.
        Raises:
            protobuf.message.DecodeError: Decoding the bytestring
                into Packet was unsuccessful.
            ValidationError: One or more values was invalid.
        """
        new_packet = cls()
        new_packet._packet.ParseFromString(data)
        cls.validate(new_packet)
        return new_packet

    def __eq__(self, other):
        if isinstance(other, Packet):
            return self.sequence_number == other.sequence_number
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Packet):
            return self.sequence_number < other.sequence_number
        else:
            return NotImplemented

    @staticmethod
    def validate(packet):
        """
        Ensure packet values are valid.
        Args:
            packet: The Packet to validate.
        Raises:
            ValidationError: One or more values was invalid.
        """
        dest_ip, dest_port = packet.dest_addr
        if _IP_MATCHER.match(dest_ip) is None:
            raise ValidationError(
                'Bad destination IP: {0}.'.format(dest_ip)
            )

        if not 1 <= dest_port <= 65535:
            raise ValidationError(
                'Bad destination port: {0}.'.format(dest_port)
            )

        source_ip, source_port = packet.source_addr
        if _IP_MATCHER.match(source_ip) is None:
            raise ValidationError(
                'Bad source IP: {0}.'.format(source_ip)
            )

        if not 1 <= source_port <= 65535:
            raise ValidationError(
                'Bad source port: {0}.'.format(source_port)
            )

    def get_syn(self):
        return self._packet.syn

    def set_syn(self, value):
        """
        Set the Packet's SYN flag.
        Args:
            value: True or False.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.syn = value

    def get_fin(self):
        return self._packet.fin

    def set_fin(self, value):
        """
        Set the Packet's FIN flag.
        Args:
            value: True or False.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.fin = value

    def get_sequence_number(self):
        return self._packet.sequence_number

    def set_sequence_number(self, value):
        """
        Set the Packet's sequence number.
        Args:
            value: A non-negative integer.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.sequence_number = value

    def get_more_fragments(self):
        return self._packet.more_fragments

    def set_more_fragments(self, value):
        """
        Set the number of fragments following this Packet.
        Args:
            value: A non-negative integer.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.more_fragments = value

    def get_ack(self):
        return self._packet.ack

    def set_ack(self, value):
        """
        Set the Packet's acknowledgement number.
        Args:
            value: A non-negative integer.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.ack = value

    def get_payload(self):
        return self._packet.payload

    def set_payload(self, value):
        """
        Set the Packet's payload.
        Args:
            value: Packet's payload, in bytes.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.payload = value

    def get_dest_addr(self):
        return self._packet.dest_ip, self._packet.dest_port

    def set_dest_addr(self, value):
        """
        Set the Packet's destination address.
        Args:
            value: An (IP, port) tuple.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.dest_ip, self._packet.dest_port = value

    def get_source_addr(self):
        return self._packet.source_ip, self._packet.source_port

    def set_source_addr(self, value):
        """
        Set the Packet's source address.
        Args:
            value: An (IP, port) tuple.
        Raises:
            TypeError: Value has inappropriate type.
        """
        self._packet.source_ip, self._packet.source_port = value

    syn = property(get_syn, set_syn)
    fin = property(get_fin, set_fin)
    sequence_number = property(get_sequence_number, set_sequence_number)
    more_fragments = property(get_more_fragments, set_more_fragments)
    ack = property(get_ack, set_ack)
    payload = property(get_payload, set_payload)
    dest_addr = property(get_dest_addr, set_dest_addr)
    source_addr = property(get_source_addr, set_source_addr)
