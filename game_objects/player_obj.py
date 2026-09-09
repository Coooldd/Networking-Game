# player object class, holds player health, velocity, etc...
from utilities.vector2 import Vector2

class Player(object):
    def __init__(self, pos: Vector2):
        self.pos = pos
        self.vel = Vector2(0, 0)