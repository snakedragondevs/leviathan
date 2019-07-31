import threading


class RakLibServer(threading.Thread):

    def __init__(self, address, max_mtu_size=1492):
        self.__address = None
        self._logger = None

        self._shutdown = False
        self._ready = False

        self._external_queue = []
        self._internal_queue = []

        self._server_id = None
        self._max_mtu_size = None
        self.__protocol_version = None

        threading.Thread.__init__(self)
        self.start()

    # todo shutdown methods

    # todo
    def push_main_to_thread_packet(self, data):
        self._internal_queue.append(data)

    def run(self):
        pass
