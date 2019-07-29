class PacketPool:

    pool = None

    @staticmethod
    def init():
        pool = [None] * 256

