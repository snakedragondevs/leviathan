class BinaryStream:
    _offset = None
    _buffer = None

    def __init__(self, buffer: bytes = "", offset: int = 0):
        self._buffer = buffer
        self._offset = offset

    def reset(self):
        self._buffer = ""
        self._offset = 0

    def rewind(self):
        self._offset = 0

    def set_offset(self, offset: int) -> None:
        self._offset = offset

    def set_buffer(self, buffer: str) -> None:
        self._buffer = buffer

    # todo: binary stream / binary - handling binary utility

