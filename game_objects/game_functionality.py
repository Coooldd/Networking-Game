import pygame


from game_objects.player_obj import Player
from utilities.vector2 import Vector2

class GameFunctionality():
    def __init__(self):
        self.SCR_WIDTH = 1400
        self.SCR_HEIGHT = 800

        self.screen = pygame.display.set_mode((self.SCR_WIDTH, self.SCR_HEIGHT))

        self.game_running = True

        self.players = []

    def game_loop(self) -> None:
        while self.game_running:
            self.manage_input()
            # self.update() <- to be added
            self.draw()

    def manage_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                continue

    def draw(self) -> None:
        self.screen.fill((150, 150, 150))

        # draw players
        for player in self.players:
            pygame.draw.circle(self.screen, (150, 100, 200), tuple(player.pos), 20)

        pygame.display.flip()