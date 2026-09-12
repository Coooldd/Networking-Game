import threading

from networking_objects.network_server import NetworkServer
from networking_objects.game_state import GameState


class GameServer:
    def __init__(self, port=6782):
        self.network = NetworkServer(port=port)
        self.state = GameState()

    def start(self):
        # thread for the queue handling tasks
        threading.Thread(target=self.state.run, daemon=True).start()

        for client_socket, client_address in self.network.listen():
            threading.Thread(
                target=self.network.run_client_loop,
                args=(client_socket, client_address),
                kwargs=dict(
                    on_connect=self.state.register_player,
                    on_message=self._on_message,
                    on_disconnect=self.state.unregister_player,
                ),
                daemon=True,
            ).start()

    def _on_message(self, player_id, message):
        # handle the inputs, and then send the state back out.
        if not message:
            print(f"There was an error with the payload from {player_id}: {message}")
            return {}
        self.state.queue_input(player_id, message.get("input", {})) # update this clients player
        return self.state.get_snapshot()