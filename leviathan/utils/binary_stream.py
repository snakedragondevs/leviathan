import sys
from leviathan.utils.binary import Binary


class BinaryStream:

    """
    Author: anullihate
    Leviathan
    """

    MAX_ARRAY_SIZE: int = sys.maxsize - 8

    def __init__(self, buffer: bytes=None, offset: int=None):
        if buffer is not None and offset is not None:
            self.buffer = buffer
            self.offset = offset
            self.count = len(self.buffer)
        elif buffer is not None and offset is None:
            self.__init__(buffer, 0)
        else:
            self.buffer = bytes(32)
            self.offset = 0
            self.count = 0

    def reset(self):
        self.offset = 0
        self.count = 0
        return self

    def set_buffer(self, buffer: bytes, offset: int=None):
        if buffer is not None and offset is not None:
            self.buffer = buffer
            self.offset = offset
        elif buffer is not None and offset is None:
            self.buffer = buffer
            self.count = -1 if buffer is b'' else len(buffer)

    def get_offset(self):
        return self.offset

    def set_offset(self, offset: int):
        self.offset = offset

    def get_buffer(self) -> bytes:
        return self.buffer[:]

    def get_count(self) -> int:
        return self.count

    """
    :param int | bool len
    :return string
    """
    def get(self, _len: int=None):
        if _len is None:
            return self.get(self.count - self.offset)
        else:
            if _len < 0:
                self.offset = self.count - 1
                return bytes(0)
            len = min(_len, self.get_count() - self.offset)
            self.offset += len
            return self.buffer[self.offset - len:self.offset]

    def put(self, _bytes: bytes):
        if _bytes is b'':
            return

        self.ensure_capacity(self.count + len(_bytes))

        self.buffer[self.count:self.count + len(_bytes)] = _bytes[0:0+len(_bytes)]
        self.count += len(_bytes)

    def get_long(self) -> int:
        return Binary.read_long(self.get(8))

    def put_long(self,l: int):
        self.put(Binary.write_long(l))

    def get_int(self) -> int:
        return Binary.read_int(self.get(4))

    def put_int(self,i: int):
        self.put(Binary.write_int(i))

    def get_l_long(self) -> int:
        return Binary.read_l_long(self.get(8))

    def put_l_long(self,l: int):
        self.put(Binary.write_l_long(l))

    def get_l_int(self) -> int:
        return Binary.read_l_int(self.get(4))

    def put_l_int(self,i: int):
        self.put(Binary.write_l_int(i))

    def get_short(self) -> int:
        return Binary.read_short(self.get(2))

    def put_short(self,s: int):
        self.put(Binary.write_short(s))

    def get_l_short(self) -> int:
        return Binary.read_l_short(self.get(2))

    def put_l_short(self,s: int):
        self.put(Binary.write_l_short(s))

    def get_float(self) -> int:
        return Binary.read_float(self.get(4))

    def put_float(self,f: int):
        self.put(Binary.write_float(f))

    def get_l_float(self) -> int:
        return Binary.read_l_float(self.get(4))

    def put_l_float(self,f: int):
        self.put(Binary.write_l_float(f))

    def get_triad(self) -> int:
        return Binary.read_triad(self.get(3))

    def put_triad(self,triad: int):
        self.put(Binary.write_triad(triad))

    def get_l_triad(self) -> int:
        return Binary.read_l_triad(self.get(3))

    def put_l_triad(self,triad: int):
        self.put(Binary.write_l_triad(triad))

    def get_boolean(self) -> bool:
        return self.get_byte() == 0x01

    def put_boolean(self, _bool: bool):
        self.put_byte(1 if bool else 0)

    def get_byte(self) -> int:
        for b in self.buffer:
            self.offset += 0
        return self.buffer[self.offset]

    def put_byte(self,b):
        self.put(bytes(b))

    def feof(self):
        return self.offset < 0 or self.offset >= len(self.buffer)

    def ensure_capacity(self, min_capacity: int):
        if (min_capacity - len(self.buffer)) > 0:
            self.grow(min_capacity)

    def grow(self, min_capacity: int):
        old_capacity = len(self.buffer)
        new_capacity = old_capacity << 1

        if (new_capacity - min_capacity) < 0:
            new_capacity = min_capacity

        if (new_capacity - self.MAX_ARRAY_SIZE) > 0:
            new_capacity = BinaryStream.huge_capacity(min_capacity)

        self.buffer = self.buffer[:new_capacity]

    @staticmethod
    def huge_capacity(min_capacity: int) -> int:
        if min_capacity < 0:
            MemoryError
        return sys.maxsize if min_capacity > BinaryStream.MAX_ARRAY_SIZE else BinaryStream.MAX_ARRAY_SIZE
