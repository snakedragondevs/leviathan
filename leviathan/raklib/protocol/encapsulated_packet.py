class EncapsulatedPacket:
    RELIABILITY_SHIFT = 5
    RELIABILITY_FLAGS = 0b111 << RELIABILITY_SHIFT
    SPLIT_FLAG = 0b00010000

    def __init__(self):

        self.reliability = None

        self.has_split = False
        self.length = 0
        self.buffer = ""
        self.need_ack = False

    @staticmethod
    def from_internal_binary(bytez):
        packet = EncapsulatedPacket()

        offset = 0
        offset += 1
        packet.reliability = ord(bytez[offset])

        return packet
