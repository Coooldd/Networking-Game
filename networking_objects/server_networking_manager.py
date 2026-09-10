import socket
import time
import queue
import threading
import random
import itertools
from typing import Any
import logging

from networking_objects.net_msg import send_msg, recieve_exact, recieve_msg
from game_objects.player_obj import Player
from utilities.vector2 import Vector2

class ServerNetworkingManager():
    def __init__(self, port=6782):
        self.host = socket.gethostbyname(socket.gethostname())
        self.PORT = 6782

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.PORT))

        self.q = queue.Queue() # queue holds (str, str) objects
        thread_server_game_loop = threading.Thread(target=self.game_loop)
        thread_server_game_loop.start()

        # this data is all for/managed by the queue
        self._id_counter = itertools.count()

        #self.data_to_client: dict[str, dict] = dict() # player_id : info to send. See what this info looks like in server_to_client.json
        self.players: dict[str, Player] = dict() # player_id : player object class

    def game_loop(self):
        while True:
            while not self.q.empty():
                self.apply_action(*self.q.get_nowait())

            time.sleep(0.01) # to do: make the time.sleep consistent so server is ticking 100 times a second

    def apply_action(self, action, player_id):
        if action == "ADD_PLAYER":
            self.players[player_id] = Player(Vector2(random.randint(0, 1400), random.randint(0, 800)), player_id)
        elif action == "REMOVE_PLAYER":
            self.players.pop(player_id, None)
        else:
            logging.warning(f"QUEUE DOES NOT RECOGNIZE TASK: {action}")

    def listen(self):
        print("Waiting for players to connect...\n")
        self.server.listen()

        while True:
            communication_socket, address = self.server.accept()
            print(f"Got a connection from {address}")
            yield communication_socket, address # main server program for loops over this function
            # new thread is set to client begin point

    def client_begin_point(self, client_socket, client_address):
        print(f"New thread started for client {client_address}")

        player_id = str(next(self._id_counter))
        self.q.put(("ADD_PLAYER", player_id))

        try:
            while True:
                data_to_client = {"players": {}} # intialize before each loop to get fresh info

                client_input = recieve_msg(client_socket)
                self.q.put(("MANAGE_INPUT", client_input))

                # update data_to_client[player_id] to send important information
                for player in list(self.players.values()):
                    data_to_client["players"][player.id] = player._network_get_dict()

                send_msg(client_socket, data_to_client) # data_to_client is only the relevant data for the specific player
                
        except ConnectionError:
            print(f"Player {client_address} disconnected")
        finally:
            client_socket.close()
            self.q.put(("REMOVE_PLAYER", player_id))
            print(f"Thread ended, connection closed for {client_address}")

    def send_data(self, data: dict):
        send_msg(self.server, data)

    def recieve_data(self): # receieves one message sent by the server.
        return recieve_msg(self.server)