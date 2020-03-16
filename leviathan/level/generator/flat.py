from leviathan.api.level.generator import Generator


class Flat(Generator):

    def get_id(self):
        return self.TYPE_FLAT

    def __init__(self):
        pass
