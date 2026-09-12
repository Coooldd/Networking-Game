from math import sqrt

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def mag(self) -> float:
        return sqrt(pow(self.x, 2) + pow(self.y, 2))

    def normal(self) -> Vector2:
        mag = self.mag()
        return Vector2(self.x / mag, self.y / mag)

    def __add__(self, other: Vector2):
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)

    def __imul__(self, scalar: float):
        self.x *= scalar
        self.y *= scalar
        return self

    def __iter__(self):
        yield self.x
        yield self.y