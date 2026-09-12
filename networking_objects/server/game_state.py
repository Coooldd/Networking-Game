import queue
import random
import itertools
import logging

from game_objects.player_obj import Player
from utilities.vector2 import Vector2
from networking_objects.server.game_clock import GameClock


# this class owns all simulation management
class GameState:

    def __init__(self):
        self._id_counter = itertools.count()
        self._action_queue = queue.Queue()  # (action_name, payload) tuples
        self.players: dict[str, Player] = dict()

    # --- called from networking threads ---

    def register_player(self, _address=None) -> str:
        player_id = str(next(self._id_counter))
        self._action_queue.put(("ADD_PLAYER", player_id))
        return player_id

    def unregister_player(self, player_id: str):
        self._action_queue.put(("REMOVE_PLAYER", player_id))

    def queue_input(self, player_id: str, input_state: dict):
        self._action_queue.put(("APPLY_INPUT", (player_id, input_state)))

    def get_snapshot(self) -> dict:
        return {"players": {p.id: p._network_get_dict() for p in self.players.values()}}

    # function ran by the queue
    def run(self):
        clock = GameClock(target_fps=100)

        while True:
            # update the state of objects based off of the clients input
            while not self._action_queue.empty():
                action, payload = self._action_queue.get_nowait()
                self._apply_action(action, payload)

            # update the movement of objects, etc... based off of their state
            for _ in range(clock.tick()):
                for player in self.players.values():
                    player.update_player(clock.tick_rate) # must run at a fixed rate, 60 tims a second, etc...

            clock.sleep_until_next_frame()


    def _apply_action(self, action, payload):
        if action == "ADD_PLAYER":
            # payload is the player_id
            self.players[payload] = Player(Vector2(random.randint(0, 1400), random.randint(0, 800)), payload)
        elif action == "REMOVE_PLAYER":
            # payload is the player_id
            self.players.pop(payload, None)
        elif action == "APPLY_INPUT":
            player_id, input_state = payload
            player = self.players.get(player_id)
            if player is not None:
                player.manage_input(input_state)
        else:
            logging.warning(f"QUEUE DOES NOT RECOGNIZE TASK: {action}")