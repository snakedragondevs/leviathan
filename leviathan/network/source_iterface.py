class SourceInterface:

    def put_packet(self, player, packet, need_ack, immediate):
        pass

    def process(self) -> bool:
        pass
