from abc import ABC, abstractmethod


class Packet(ABC):

    @abstractmethod
    def encode(self):
        pass

    @abstractmethod
    def decode(self):
        pass


def packet_registry():
    pass
