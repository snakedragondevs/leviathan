

class Network:

    def __init__(self, server):
        self.interfaces = set()

        self.upload = 0
        self.download = 0

        self.server = server

    # def process_interface(self):
    #     interface: SourceInterface
    #     for interface in self.interfaces:
    #         try:
    #             interface.process()
    #         except Exception as e:
    #             print(e)

    def register_interface(self, interface):
        self.interfaces.add(interface)

