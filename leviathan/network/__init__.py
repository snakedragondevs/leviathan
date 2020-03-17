from leviathan.network.protocol.info import ProtocolInfo


class Network:  # network handler

    CHANNEL_NONE = 0
    CHANNEL_PRIORITY = 1
    CHANNEL_WORLD_CHUNKS = 2
    CHANNEL_MOVEMENT = 3
    CHANNEL_BLOCKS = 4
    CHANNEL_WORLD_EVENTS = 5
    CHANNEL_ENTITY_SPAWNING = 6
    CHANNEL_TEXT = 7
    CHANNEL_END = 31

    def __init__(self):
        self.interfaces = set()

    # network interface
    def process_interfaces(self):
        for interface in self.interfaces:
            try:
                interface.process()
            except Exception:
                pass

    def register_interface(self, interface):
        self.interfaces.add(interface)

    def unregister_interface(self, interface):
        self.interfaces.remove(interface)

    # network details
    def set_name(self, name):
        pass

    def set_subname(self, name):
        pass

    def update_name(self, name):
        pass

    # network control
    def block_address(self, address):
        pass

    def unblock_address(self, address):
        pass

    # registries
    def register_packet(self, packet_id, packet_class):
        self.packet_pool[packet_id] = packet_class

    def register_packets(self):
        self.packet_pool = [None] * 256

        self.register_packet(ProtocolInfo.ADD_ENTITY_PACKET, 'ADD_ENTITY_PACKET')
        self.register_packet(ProtocolInfo.ADD_ITEM_ENTITY_PACKET, 'ADD_ITEM_ENTITY_PACKET')
        self.register_packet(ProtocolInfo.ADD_PAINTING_PACKET, 'ADD_PAINTING_PACKET')
        self.register_packet(ProtocolInfo.ADD_PLAYER_PACKET, 'ADD_PLAYER_PACKET')
        self.register_packet(ProtocolInfo.ADVENTURE_SETTINGS_PACKET, 'ADVENTURE_SETTINGS_PACKET')
        self.register_packet(ProtocolInfo.ANIMATE_PACKET, 'ANIMATE_PACKET')
        self.register_packet(ProtocolInfo.AVAILABLE_COMMANDS_PACKET, 'AVAILABLE_COMMANDS_PACKET')
        self.register_packet(ProtocolInfo.BATCH_PACKET, 'BATCH_PACKET')
        self.register_packet(ProtocolInfo.BLOCK_ENTITY_DATA_PACKET, 'BLOCK_ENTITY_DATA_PACKET')
        self.register_packet(ProtocolInfo.BLOCK_EVENT_PACKET, 'BLOCK_EVENT_PACKET')
        self.register_packet(ProtocolInfo.BLOCK_PICK_REQUEST_PACKET, 'BLOCK_PICK_REQUEST_PACKET')
        self.register_packet(ProtocolInfo.BOSS_EVENT_PACKET, 'BOSS_EVENT_PACKET')
        self.register_packet(ProtocolInfo.CHANGE_DIMENSION_PACKET, 'CHANGE_DIMENSION_PACKET')
        self.register_packet(ProtocolInfo.CHUNK_RADIUS_UPDATED_PACKET, 'CHUNK_RADIUS_UPDATED_PACKET')
        self.register_packet(ProtocolInfo.CLIENTBOUND_MAP_ITEM_DATA_PACKET, 'CLIENTBOUND_MAP_ITEM_DATA_PACKET')
        self.register_packet(ProtocolInfo.COMMAND_REQUEST_PACKET, 'COMMAND_REQUEST_PACKET')
        self.register_packet(ProtocolInfo.CONTAINER_CLOSE_PACKET, 'CONTAINER_CLOSE_PACKET')
        self.register_packet(ProtocolInfo.CONTAINER_OPEN_PACKET, 'CONTAINER_OPEN_PACKET')
        self.register_packet(ProtocolInfo.CONTAINER_SET_DATA_PACKET, 'CONTAINER_SET_DATA_PACKET')
        self.register_packet(ProtocolInfo.CRAFTING_DATA_PACKET, 'CRAFTING_DATA_PACKET')
        self.register_packet(ProtocolInfo.CRAFTING_EVENT_PACKET, 'CRAFTING_EVENT_PACKET')
        self.register_packet(ProtocolInfo.DISCONNECT_PACKET, 'DISCONNECT_PACKET')
        self.register_packet(ProtocolInfo.ENTITY_EVENT_PACKET, 'ENTITY_EVENT_PACKET')
        self.register_packet(ProtocolInfo.ENTITY_FALL_PACKET, 'ENTITY_FALL_PACKET')
        self.register_packet(ProtocolInfo.EXPLODE_PACKET, 'EXPLODE_PACKET')
        self.register_packet(ProtocolInfo.FULL_CHUNK_DATA_PACKET, 'FULL_CHUNK_DATA_PACKET')
        self.register_packet(ProtocolInfo.GAME_RULES_CHANGED_PACKET, 'GAME_RULES_CHANGED_PACKET')
        self.register_packet(ProtocolInfo.HURT_ARMOR_PACKET, 'HURT_ARMOR_PACKET')
        self.register_packet(ProtocolInfo.INTERACT_PACKET, 'INTERACT_PACKET')
        self.register_packet(ProtocolInfo.INVENTORY_CONTENT_PACKET, 'INVENTORY_CONTENT_PACKET')
        self.register_packet(ProtocolInfo.INVENTORY_TRANSACTION_PACKET, 'INVENTORY_TRANSACTION_PACKET')
        self.register_packet(ProtocolInfo.ITEM_FRAME_DROP_ITEM_PACKET, 'ITEM_FRAME_DROP_ITEM_PACKET')
        self.register_packet(ProtocolInfo.LEVEL_EVENT_PACKET, 'LEVEL_EVENT_PACKET')
        self.register_packet(ProtocolInfo.LEVEL_SOUND_EVENT_PACKET_V1, 'LEVEL_SOUND_EVENT_PACKET_V1')
        self.register_packet(ProtocolInfo.LOGIN_PACKET, 'LOGIN_PACKET')
        self.register_packet(ProtocolInfo.MAP_INFO_REQUEST_PACKET, 'MAP_INFO_REQUEST_PACKET')
        self.register_packet(ProtocolInfo.MOB_ARMOR_EQUIPMENT_PACKET, 'MOB_ARMOR_EQUIPMENT_PACKET')
        self.register_packet(ProtocolInfo.MOB_EQUIPMENT_PACKET, 'MOB_EQUIPMENT_PACKET')
        self.register_packet(ProtocolInfo.MODAL_FORM_REQUEST_PACKET, 'MODAL_FORM_REQUEST_PACKET')
        self.register_packet(ProtocolInfo.MODAL_FORM_RESPONSE_PACKET, 'MODAL_FORM_RESPONSE_PACKET')
        self.register_packet(ProtocolInfo.MOVE_ENTITY_ABSOLUTE_PACKET, 'MOVE_ENTITY_ABSOLUTE_PACKET')
        self.register_packet(ProtocolInfo.MOVE_PLAYER_PACKET, 'MOVE_PLAYER_PACKET')
        self.register_packet(ProtocolInfo.PLAYER_ACTION_PACKET, 'PLAYER_ACTION_PACKET')
        self.register_packet(ProtocolInfo.PLAYER_INPUT_PACKET, 'PLAYER_INPUT_PACKET')
        self.register_packet(ProtocolInfo.PLAYER_LIST_PACKET, 'PLAYER_LIST_PACKET')
        self.register_packet(ProtocolInfo.PLAYER_HOTBAR_PACKET, 'PLAYER_HOTBAR_PACKET')
        self.register_packet(ProtocolInfo.PLAY_SOUND_PACKET, 'PLAY_SOUND_PACKET')
        self.register_packet(ProtocolInfo.PLAY_STATUS_PACKET, 'PLAY_STATUS_PACKET')
        self.register_packet(ProtocolInfo.REMOVE_ENTITY_PACKET, 'REMOVE_ENTITY_PACKET')
        self.register_packet(ProtocolInfo.REQUEST_CHUNK_RADIUS_PACKET, 'REQUEST_CHUNK_RADIUS_PACKET')
        self.register_packet(ProtocolInfo.RESOURCE_PACKS_INFO_PACKET, 'RESOURCE_PACKS_INFO_PACKET')
        self.register_packet(ProtocolInfo.RESOURCE_PACK_STACK_PACKET, 'RESOURCE_PACK_STACK_PACKET')
        self.register_packet(ProtocolInfo.RESOURCE_PACK_CLIENT_RESPONSE_PACKET, 'RESOURCE_PACK_CLIENT_RESPONSE_PACKET')
        self.register_packet(ProtocolInfo.RESOURCE_PACK_DATA_INFO_PACKET, 'RESOURCE_PACK_DATA_INFO_PACKET')
        self.register_packet(ProtocolInfo.RESOURCE_PACK_CHUNK_DATA_PACKET, 'RESOURCE_PACK_CHUNK_DATA_PACKET')
        self.register_packet(ProtocolInfo.RESOURCE_PACK_CHUNK_REQUEST_PACKET, 'RESOURCE_PACK_CHUNK_REQUEST_PACKET')
        self.register_packet(ProtocolInfo.RESPAWN_PACKET, 'RESPAWN_PACKET')
        self.register_packet(ProtocolInfo.RIDER_JUMP_PACKET, 'RIDER_JUMP_PACKET')
        self.register_packet(ProtocolInfo.SET_COMMANDS_ENABLED_PACKET, 'SET_COMMANDS_ENABLED_PACKET')
        self.register_packet(ProtocolInfo.SET_DIFFICULTY_PACKET, 'SET_DIFFICULTY_PACKET')
        self.register_packet(ProtocolInfo.SET_ENTITY_DATA_PACKET, 'SET_ENTITY_DATA_PACKET')
        self.register_packet(ProtocolInfo.SET_ENTITY_LINK_PACKET, 'SET_ENTITY_LINK_PACKET')
        self.register_packet(ProtocolInfo.SET_ENTITY_MOTION_PACKET, 'SET_ENTITY_MOTION_PACKET')
        self.register_packet(ProtocolInfo.SET_HEALTH_PACKET, 'SET_HEALTH_PACKET')
        self.register_packet(ProtocolInfo.SET_PLAYER_GAME_TYPE_PACKET, 'SET_PLAYER_GAME_TYPE_PACKET')
        self.register_packet(ProtocolInfo.SET_SPAWN_POSITION_PACKET, 'SET_SPAWN_POSITION_PACKET')
        self.register_packet(ProtocolInfo.SET_TITLE_PACKET, 'SET_TITLE_PACKET')
        self.register_packet(ProtocolInfo.SET_TIME_PACKET, 'SET_TIME_PACKET')
        self.register_packet(ProtocolInfo.SERVER_SETTINGS_REQUEST_PACKET, 'SERVER_SETTINGS_REQUEST_PACKET')
        self.register_packet(ProtocolInfo.SERVER_SETTINGS_RESPONSE_PACKET, 'SERVER_SETTINGS_RESPONSE_PACKET')
        self.register_packet(ProtocolInfo.SHOW_CREDITS_PACKET, 'SHOW_CREDITS_PACKET')
        self.register_packet(ProtocolInfo.SPAWN_EXPERIENCE_ORB_PACKET, 'SPAWN_EXPERIENCE_ORB_PACKET')
        self.register_packet(ProtocolInfo.TAKE_ITEM_ENTITY_PACKET, 'TAKE_ITEM_ENTITY_PACKET')
        self.register_packet(ProtocolInfo.TEXT_PACKET, 'TEXT_PACKET')
        self.register_packet(ProtocolInfo.UPDATE_ATTRIBUTES_PACKET, 'UPDATE_ATTRIBUTES_PACKET')
        self.register_packet(ProtocolInfo.UPDATE_BLOCK_PACKET, 'UPDATE_BLOCK_PACKET')
        self.register_packet(ProtocolInfo.UPDATE_TRADE_PACKET, 'UPDATE_TRADE_PACKET')
        self.register_packet(ProtocolInfo.MOVE_ENTITY_DELTA_PACKET, 'MOVE_ENTITY_DELTA_PACKET')
        self.register_packet(ProtocolInfo.SET_LOCAL_PLAYER_AS_INITIALIZED_PACKET, 'SET_LOCAL_PLAYER_AS_INITIALIZED_PACKET')
        self.register_packet(ProtocolInfo.NETWORK_STACK_LATENCY_PACKET, 'NETWORK_STACK_LATENCY_PACKET')
        self.register_packet(ProtocolInfo.UPDATE_SOFT_ENUM_PACKET, 'UPDATE_SOFT_ENUM_PACKET')
        self.register_packet(ProtocolInfo.NETWORK_CHUNK_PUBLISHER_UPDATE_PACKET, 'NETWORK_CHUNK_PUBLISHER_UPDATE_PACKET')
        self.register_packet(ProtocolInfo.AVAILABLE_ENTITY_IDENTIFIERS_PACKET, 'AVAILABLE_ENTITY_IDENTIFIERS_PACKET')
        self.register_packet(ProtocolInfo.LEVEL_SOUND_EVENT_PACKET_V2, 'LEVEL_SOUND_EVENT_PACKET_V2')
        self.register_packet(ProtocolInfo.SCRIPT_CUSTOM_EVENT_PACKET, 'SCRIPT_CUSTOM_EVENT_PACKET')
        self.register_packet(ProtocolInfo.SPAWN_PARTICLE_EFFECT_PACKET, 'SPAWN_PARTICLE_EFFECT_PACKET')
        self.register_packet(ProtocolInfo.BIOME_DEFINITION_LIST_PACKET, 'BIOME_DEFINITION_LIST_PACKET')
        self.register_packet(ProtocolInfo.LEVEL_SOUND_EVENT_PACKET, 'LEVEL_SOUND_EVENT_PACKET')
        self.register_packet(ProtocolInfo.LEVEL_EVENT_GENERIC_PACKET, 'LEVEL_EVENT_GENERIC_PACKET')
        self.register_packet(ProtocolInfo.LECTERN_UPDATE_PACKET, 'LECTERN_UPDATE_PACKET')
        self.register_packet(ProtocolInfo.VIDEO_STREAM_CONNECT_PACKET, 'VIDEO_STREAM_CONNECT_PACKET')
        self.register_packet(ProtocolInfo.CLIENT_CACHE_STATUS_PACKET, 'CLIENT_CACHE_STATUS_PACKET')
        self.register_packet(ProtocolInfo.MAP_CREATE_LOCKED_COPY_PACKET, 'MAP_CREATE_LOCKED_COPY_PACKET')
        self.register_packet(ProtocolInfo.ON_SCREEN_TEXTURE_ANIMATION_PACKET, 'ON_SCREEN_TEXTURE_ANIMATION_PACKET')
