from abc import ABC, abstractmethod


class Generator(ABC):

    TYPE_OLD = 0
    TYPE_INFINITE = 1
    TYPE_FLAT = 2
    TYPE_NETHER = 3

    @abstractmethod
    def get_id(self):
        pass

    def get_dimension(self):
        pass

    name_list = dict()
    type_list = dict()

    @staticmethod
    def add_generator(cls, name, typ):
        name = str(name).lower()
        if cls is not None and name not in Generator.name_list:
            Generator.name_list[name] = cls
            if typ not in Generator.type_list:
                Generator.type_list[typ] = cls
            return True
        return False
