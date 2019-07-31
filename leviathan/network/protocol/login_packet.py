from leviathan.network.protocol.data_packet import DataPacket
from leviathan.network.protocol.protocol_info_pmmp import ProtocolInfo


class LoginPacket(DataPacket):
    NETWORK_ID = ProtocolInfo.LOGIN_PACKET

    EDITION_PACKET = 0

    def __init__(self):
        self.username = None
        self.protocol = None
        self.client_uuid = None
        self.client_id = None
        self.xuid = None
        self.identity_public_key = None
        self.server_address = None
        self.locale = None

        self.chain_data = []
        self.client_data_jwt = None
        self.client_data = None

        self.skip_verification = False
