from logzero import logger

from leviathan.api.level.level import Level
from leviathan.api.math.vector3 import Vector3


class Position(Vector3):

    def __init__(self, x=0, y=0, z=0, level=None):
        Vector3.__init__(self, x, y, z)
        self.level = level

    @staticmethod
    def from_object(pos: Vector3, level: Level):
        return Position(pos.x, pos.y, pos.z, level)

    def as_position(self):
        return Position(self.x, self.y, self.z, self.level)

    def get_level(self):
        if self.level is not None and self.level.is_closed():
            logger.debug("Position was holding a reference to an unloaded Level")
            self.level = None

        return self.level

    def set_level(self, level: Level=None):
        if level is not None and level.is_closed():
            raise AttributeError("Specified level has been unloaded and cannot be used")

        self.level = level
        return self

    def is_valid(self) -> bool:
        if self.level is not None and self.level.is_closed():
            self.level = None

            return False

        return self.level is not None

    def get_side(self, side: int, step: int = 1):
        assert self.is_valid()

        return Position.from_object(self.get_side(side, step), self.level)

    def _tostring(self):
        return "Position(level=" + self.get_level().get_name() if self.is_valid() else None + ",x=" + self.x + ",y=" + self.y + ",z=" + self.z + ")"

    def equals(self, v) -> bool:
        if isinstance(v, Position):
            return Vector3.equals(self, v) and v.get_level() == self.get_level()
