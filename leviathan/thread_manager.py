class ThreadManager:

    def __init__(self):
        self.instance = self.__class__

    def add(self, thread):
        self.__setattr__(hash(thread), thread)
