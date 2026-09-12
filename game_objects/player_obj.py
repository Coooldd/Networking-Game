# player object class, holds player health, velocity, etc...
from utilities.vector2 import Vector2
import json

class Player(object):
    def __init__(self, pos: Vector2, id):
        self.pos = pos
        self.vel = Vector2(0, 0)

        self.id = id # unique id for player

    def manage_input(self, input_load):
        """
        Input load matches that in client_to_server.py["input"]
        {
            "key_a": True
            "key_space": True, etc...
        }

        """
        a_pressed = input_load.get("key_a", False)
        d_pressed = input_load.get("key_d", False)
        if (a_pressed and d_pressed) or (not (a_pressed or d_pressed)): # if both keys are being pressed or none
            self.vel.x = 0
        elif a_pressed:
            self.vel.x = -5
        elif d_pressed:
            self.vel.x = 5

    def update_player(self):
        self.pos += self.vel

    def _network_get_dict(self):
        return {"pos": list(self.pos)}

