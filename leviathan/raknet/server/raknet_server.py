import threading
import socket

from leviathan.raknet.server.session_manager import SessionManager


class RaknetServer(threading.Thread):

    def __init__(self, port, host):
        self.port = port
        if port < 1 or port > 65536:
            raise ValueError("Invalid port range")

        self.host = host

        self.external_queue = threading.Thread()
        self.internal_queue = threading.Thread()

        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.setName("Raknet {}".format(self.getName()))

        print("running " + self.getName())
        # todo use to add udpsocket server
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.host, self.port))
        while True:
            print("waiting to receive message")
            data, address = sock.recvfrom(4096)
            print('received %s bytes from %s' % (len(data), address))
            print(data)

        # try:
        #
        #     print("connected to {} on {}".format(self.host, self.port))
        #     SessionManager(self, s)
        # except socket.error as e:
        #     print(e)
