

class Connection(object):

    class ScheduledPacket(object):

        pass

    def __init__(self):
        self._state = 'CONNECTING'
        pass

    @property
    def state(self):
        return self._state
