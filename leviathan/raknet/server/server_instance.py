class ServerInstance:
    def open_session(self, identifier, address, port, client_id):
        pass

    def close_session(self, identifier, reason):
        pass

    def handle_encapsulated(self, identifier, packet, flags):
        pass

    def handle_raw(self, address, port, payload):
        pass

    def notify_ack(self, identifier, identifier_ack):
        pass

    def handle_option(self, option, value):
        pass
