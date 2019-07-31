from leviathan.network.twisted.twisted_server import TwistedServer


class TwistedManager:

    def __init__(self):
        self.twisted = TwistedServer()
