import threading
import socket


class RaknetServer(threading.Thread):

    def __init__(self, port, interface):
        self.port = port
        if port < 1 or port > 65536:
            raise ValueError("Invalid port range")

        self.interface = interface

        self.external_queue = threading.Thread()
        self.internal_queue = threading.Thread()

        threading.Thread.__init__(self)
        self.start()

    def run(self):
        self.setName("Raknet {}".format(self.getName()))

        print("running " + self.getName())
        # todo use to add udpsocket server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        try:
            s.connect((self.interface, self.port))
            print("connected to {} on {}".format(self.interface, self.port))
        except socket.error as e:
            print(e)
