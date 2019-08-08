import functools
import re

# IP validation regexes from the Regular Expressions Cookbook.
# For now, only standard (non-compressed) IPv6 addresses are
# supported. This might change in the future.
_IPV4_REGEX = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
_IPV6_REGEX = r'^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$'

_IP_MATCHER = re.compile('({0})|({1})'.format(_IPV4_REGEX, _IPV6_REGEX))


class ValidationError(Exception):
    pass


@functools.total_ordering
class Packet(object):

    def __init__(self):
        self._packet = b''

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
        pass
