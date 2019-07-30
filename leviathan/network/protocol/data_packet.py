from abc import ABC, abstractmethod

from leviathan.utils.binary_stream import BinaryStream


class DataPacket(ABC, BinaryStream):
    NETWORK_ID = 0

    def pid(self):
        return self.NETWORK_ID

    def get_name(self) -> str:
        return self.get_name()
