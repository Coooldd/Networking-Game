import pygame
import threading
import time
from typing import Any


from game_objects.player_obj import Player
from utilities.vector2 import Vector2
from networking_objects.client_networking_manager import ClientNetworkingManager


class ClientGameFunctionality():
    def __init__(self, server_ip: str):
        pygame.init()

        self.SCR_WIDTH = 1400
        self.SCR_HEIGHT = 800
        self.screen = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT))
        self.clock = pygame.time.Clock()

        self.network = ClientNetworkingManager(server_ip) # creates socket, connects to server

        self.game_running = True

        self.players = []

        self.thread_networking = threading.Thread(target=self.manage_networking, daemon=True)

        self.data_to_server = dict()
        self.data_to_server['key_a'] = False

        self.data_from_server: dict[str, Any] = {} # see server_to_client.json for example object

    def start_game_loop(self) -> None:
        self.thread_networking.start()

        while self.game_running:
            self.manage_input()
            self.draw()
            self.clock.tick(60)

        pygame.quit()

    def manage_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("game_running is false now")
                self.game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.data_to_server["input"]['key_a'] = True
                if event.key == pygame.K_d:
                    self.data_to_server["input"]['key_d'] = True
            if event.type == pygame.KEYUP:
                # dont send info when player is not pressing, we will know by the lack of value for those keys
                if event.key == pygame.K_a:
                    self.data_to_server["input"].pop("key_a")
                if event.key == pygame.K_d: 
                    self.data_to_server["input"].pop("key_d")

    def draw(self) -> None:
        self.screen.fill((150, 150, 150))

        # draw players
        player_info = self.data_from_server.get("players", {})
        for pos_object in list(player_info.values()):
            pos = pos_object['pos']
            pygame.draw.circle(self.screen, (150, 100, 200), pos, 20)

        pygame.display.flip()

    def manage_networking(self):
        while self.game_running:
            self.network.send_data(self.data_to_server)
            incoming_data = self.network.recieve_data()
            if incoming_data is not None:
                self.data_from_server = incoming_data
            else:
                print("There was an error with the server")
                self.game_running = False
                break
            time.sleep(0.01)