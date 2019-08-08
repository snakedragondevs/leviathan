"""Constants governing operation of txrudp package."""

# [bytes]
UDP_SAFE_SEGMENT_SIZE = 1000

# [length]
WINDOW_SIZE = 65535 // UDP_SAFE_SEGMENT_SIZE

# [seconds]
PACKET_TIMEOUT = 0.6

# [seconds]
BARE_ACK_TIMEOUT = 0.01

# [seconds]
MAX_PACKET_DELAY = 15

# If a packet is retransmitted more than that many times,
# the connection should be considered broken.
MAX_RETRANSMISSIONS = int(MAX_PACKET_DELAY // PACKET_TIMEOUT)

# packet related
OFFLINE_MESSAGE_DATA_ID = bytearray.fromhex("00 ff ff 00 fe fe fe fe fd fd fd fd 12 34 56 78")
