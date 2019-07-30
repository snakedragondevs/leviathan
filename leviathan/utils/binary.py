import uuid
from struct import unpack, pack

"""
Author: anullihate
Leviathan
"""


class Binary:

    """
    TRIADS
    - read_triad
    - write_triad
    - read_l_triad
    - write_l_triad
    """
    @staticmethod
    def read_triad(_bytes: bytes) -> int:
        return unpack('>l', b''.join([b'\x00',_bytes[0],_bytes[1],_bytes[2]]))[0]

    @staticmethod
    def write_triad(value: int) -> bytes:
        return pack('>l', value)[1:]

    # Triad - Little
    @staticmethod
    def read_l_triad(_bytes: bytes) -> int:
        return unpack('<l', b''.join([_bytes[0], _bytes[1], _bytes[2], b'\x00']))[0]

    @staticmethod
    def write_l_triad(value: int) -> bytes:
        return pack('<l', value)[0:-1]

    """
    BOOL
    - read_bool
    - write_bool
    """
    @staticmethod
    def read_uuid(_bytes: bytes):
        return uuid.UUID(hex(Binary.read_l_long(_bytes)), bytes(Binary.read_l_long(bytes([
            _bytes[8],
            _bytes[9],
            _bytes[10],
            _bytes[11],
            _bytes[12],
            _bytes[13],
            _bytes[14],
            _bytes[15]
        ]))))

    @staticmethod
    def write_uuid(_bytes: bytes):
        pass

    """
    BOOL
    - read_bool
    - write_bool
    """
    @staticmethod
    def read_bool(b: bytes) -> bool:
        return unpack('?', b)[0]

    @staticmethod
    def write_bool(b: bool) -> bytes:
        return b'\x01' if b else b'\x00'

    """
    BYTE
    - read_byte
    - write_byte
    """
    @staticmethod
    def read_byte(b: bytes) -> int:
        return ord(b)

    @staticmethod
    def write_byte(b: int) -> bytes:
        return chr(b).encode()

    """
    SHORT
    - read_short
    - write_short
    - read_l_short
    - write_l_short
    """
    @staticmethod
    def read_short(s: bytes) -> int:
        return unpack('>h', s)[0]

    @staticmethod
    def write_short(s: int) -> bytes:
        return pack('>h', s)

    @staticmethod
    def read_l_short(s: bytes) -> int:
        return unpack('<h', s)[0]

    @staticmethod
    def write_l_short(s: int) -> bytes:
        return pack('<h', s)

    """
    INT
    - read_int
    - write_int
    - read_l_int
    - write_l_int
    """
    @staticmethod
    def read_int(i: bytes) -> int:
        return unpack('>i', i)[0]

    @staticmethod
    def write_int(i: int) -> bytes:
        return pack('>i', i)

    @staticmethod
    def read_l_int(i: bytes) -> int:
        return unpack('<i', i)[0]

    @staticmethod
    def write_l_int(i: int) -> bytes:
        return pack('<i', i)

    """
    FLOAT
    - read_float
    - write_float
    - read_l_float
    - write_l_float
    """
    @staticmethod
    def read_float(f: bytes) -> int:
        return unpack('>f', f)[0]

    @staticmethod
    def write_float(f: int) -> bytes:
        return pack('>f', f)

    @staticmethod
    def read_l_float(f: bytes) -> int:
        return unpack('<f', f)[0]

    @staticmethod
    def write_l_float(f: int) -> bytes:
        return pack('<f', f)

    """
    DOUBLE
    - read_double
    - write_double
    - read_l_double
    - write_l_double
    """
    @staticmethod
    def read_double(d: bytes) -> int:
        return unpack('>d', d)[0]

    @staticmethod
    def write_double(d: int) -> bytes:
        return pack('>d', d)

    @staticmethod
    def read_l_double(d: bytes) -> int:
        return unpack('<d', d)[0]

    @staticmethod
    def write_l_double(d: int) -> bytes:
        return pack('<d', d)

    """
    LONG
    - read_long
    - write_long
    - read_l_long
    - write_l_long
    """
    @staticmethod
    def read_long(l: bytes) -> int:
        return unpack('>l', l)[0]

    @staticmethod
    def write_long(l: int) -> bytes:
        return pack('>l', l)

    @staticmethod
    def read_l_long(l: bytes) -> int:
        return unpack('<l', l)[0]

    @staticmethod
    def write_l_long(l: int) -> bytes:
        return pack('>l', l)
