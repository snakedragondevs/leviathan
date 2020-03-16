import abc


class DataPacket(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def decode():
        pass

    @abc.abstractmethod
    def encode():
        pass

    def compress():
        try:
            # compressions
            # return packet
            pass
        finally:
            pass
        pass
