# player object class, holds player health, velocity, etc...
from utilities.vector2 import Vector2
import json

class Player(object):
    def __init__(self, pos: Vector2, id):
        self.pos = pos
        self.id = id # unique id for player

        self.input = {}

    def manage_input(self):
        pass

    def _network_get_dict(self):
        return {"pos": list(self.pos)}