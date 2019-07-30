class ServerHandler:

    def __init__(self, raknet_server, server_instance):
        self.server = raknet_server
        self.instance = server_instance

    # todo handle_packet
    def handle_packet(self) -> bool:
        # todo will invoke every ticks and always check main packet for data then handle protocols
        if True:
            # do something
            pass
        return False
