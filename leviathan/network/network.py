

class Network:

    BATCH_THRESHOLD = 512

    upload = 0
    download = 0

    def __init__(self, server):
        self.server = server

    def register_interface(self):
        pass

