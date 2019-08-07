class ValidationError(Exception):
    pass


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
