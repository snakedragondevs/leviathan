class SessionManager:

    def __init__(self, server, socket):
        self.server = server
        self.socket = socket

        self.run()

    def run(self):
        print("session manager run")
        pass

    def tick_processor(self):
        pass
