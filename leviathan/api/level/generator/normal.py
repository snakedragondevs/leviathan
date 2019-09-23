from leviathan.api.level.generator import Generator


class Normal(Generator):

    def get_id(self):
        return self.TYPE_INFINITE
