from abc import ABCMeta, abstractmethod


class RakLib(metaclass=ABCMeta):

    VERSION = "0.12.0"

    DEFAULT_PROTOCOL_VERSION = 6

    PRIORITY_NORMAL = 0
    PRIORITY_IMMEDIATE = 1

    FLAG_NEED_ACK = 0b00001000

    SYSTEM_ADDRESS_COUNT = 20

    def __init__(self):
        pass
