import math

from pyblox.math.facing import Facing
from pyblox.math.vector2 import Vector2


class Vector3:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_z(self):
        return self.z

    def get_floor_x(self) -> int:
        return math.floor(self.x)

    def get_floor_y(self) -> int:
        return math.floor(self.y)

    def get_floor_z(self) -> int:
        return math.floor(self.z)

    def get_chunk_x(self):
        return self.get_floor_x() >> 4

    def get_chunk_z(self):
        return self.get_floor_z() >> 4

    def get_right(self):
        return self.x

    def get_up(self):
        return self.y

    def get_forward(self):
        return self.z

    def get_south(self):
        return self.x

    def get_west(self):
        return self.z

    def add(self, x, y=None, z=None):
        if isinstance(x, Vector3):
            return Vector3(self.x + x.get_x(), self.y + x.get_y(), self.z + x.get_z())
        elif x is not None and y is None and z is None:
            return self.add(x, 0, 0)
        elif x is not None and y is not None and z is None:
            return self.add(x, y, 0)
        else:
            return Vector3(self.x + x, self.y + y, self.z + z)

    def substract(self,x=0, y=0, z=0):
        if isinstance(x, Vector3):
            return self.add(-x.x, -x.y, -x.z)
        else:
            return self.add(-x, -y, -z)

    def multiply(self, number: float):
        return Vector3(self.x * number, self.y * number, self.z * number)

    def divide(self, number: float):
        return Vector3(self.x / number, self.y / number, self.z / number)

    def ceil(self):
        return Vector3(math.ceil(self.x), math.ceil(self.y), math.ceil(self.z))

    def floor(self):
        return Vector3(math.floor(self.x), math.floor(self.y), math.floor(self.z))

    def round(self):
        return Vector3(round(self.x), round(self.y), round(self.z))

    def abs(self):
        return Vector3(abs(self.x), abs(self.y), abs(self.z))

    def get_side(self, side: int, step: int):
        if side is Facing.DOWN:
            return Vector3(self.x, self.y - step, self.z)
        elif side is Facing.UP:
            return Vector3(self.x, self.y + step, self.z)
        elif side is Facing.NORTH:
            return Vector3(self.x, self.y, self.z - step)
        elif side is Facing.SOUTH:
            return Vector3(self.x, self.y, self.z + step)
        elif side is Facing.WEST:
            return Vector3(self.x - step, self.y, self.z)
        elif side is Facing.EAST:
            return Vector3(self.x + step, self.y, self.z)
        else:
            return self

    def up(self, step: int):
        return self.get_side(Facing.UP, step)

    def down(self, step: int):
        return self.get_side(Facing.DOWN, step)

    def north(self, step: int):
        return self.get_side(Facing.NORTH, step)

    def south(self, step: int):
        return self.get_side(Facing.SOUTH, step)

    def east(self, step: int):
        return self.get_side(Facing.EAST, step)

    def west(self, step: int):
        return self.get_side(Facing.WEST, step)

    def distance(self, pos):
        return math.sqrt(self.distance_squared(pos))

    def distance_squared(self, pos):
        return math.pow(self.x - pos.x, 2) + math.pow(self.y - pos.y, 2) + math.pow(self.z - pos.z, 2)

    def max_plain_distance(self, x=None, z=None):
        if isinstance(x, Vector2):
            return self.max_plain_distance(x.x, x.y)
        elif isinstance(x, Vector3):
            return self.max_plain_distance(x.x, x.z)
        elif x is None and z is None:
            return self.max_plain_distance(0, 0)
        elif x is not None and x is None:
            return self.max_plain_distance(x, 0)
        else:
            return max(abs(self.x - x), abs(self.z - z))

    def length(self):
        return math.sqrt(self.length_squared())

    def length_squared(self):
        return self.x * self.x + self.y * self.y + self.z * self.z

    def normalize(self):
        _len = self.length_squared()
        if _len > 0:
            return self.divide(math.sqrt(_len))
        return Vector3(0, 0, 0)

    def dot(self, v):
        return self.x * v.x + self.y * v.y + self.z * v.z

    def cross(self, v):
        return Vector3(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x
        )

    def equals(self, v) -> bool:
        return self.x is v.x and self.y is v.y and self.z is v.z

    def get_intermediate_with_x_value(self, v, x: int):
        xdiff = v.x - self.x
        ydiff = v.y - self.y
        zdiff = v.z - self.z
        if xdiff * xdiff < 0.0000001:
            return None
        f = (x - self.x) / xdiff
        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + xdiff * f, self.y + ydiff * f, self.z + zdiff * f)

    def get_intermediate_with_y_value(self, v, y: int):
        xdiff = v.x - self.x
        ydiff = v.y - self.y
        zdiff = v.z - self.z
        if ydiff * ydiff < 0.0000001:
            return None
        f = (y - self.y) / ydiff
        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + xdiff * f, self.y + ydiff * f, self.z + zdiff * f)

    def get_intermediate_with_z_value(self, v, z: int):
        xdiff = v.x - self.x
        ydiff = v.y - self.y
        zdiff = v.z - self.z
        if zdiff * zdiff < 0.0000001:
            return None
        f = (z - self.z) / zdiff
        if f < 0 or f > 1:
            return None
        else:
            return Vector3(self.x + xdiff * f, self.y + ydiff * f, self.z + zdiff * f)

    def set_components(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        return self
