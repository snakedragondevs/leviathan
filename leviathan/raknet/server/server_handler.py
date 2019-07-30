class ServerHandler:

    def __init__(self, raknet_server, server_instance):
        self.server = raknet_server
        self.instance = server_instance

    # todo handle_packet
    def handle_packet(self) -> bool:
        return False
