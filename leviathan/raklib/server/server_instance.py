from abc import ABCMeta, abstractmethod


class ServerInstance(metaclass=ABCMeta):

    @abstractmethod
    def open_session(self, session_id, address, port, client_id):
        pass

    @abstractmethod
    def close_session(self, session_id, reason):
        pass

    @abstractmethod
    def handle_encapsulated(self, session_id, packet, flags):
        pass

    @abstractmethod
    def handle_raw(self, address, port, payload):
        pass

    @abstractmethod
    def notify_ack(self, session_id, identifier_ack):
        pass

    @abstractmethod
    def handle_option(self, option, value):
        pass

    @abstractmethod
    def update_ping(self, session_id, ping_ms):
        pass
