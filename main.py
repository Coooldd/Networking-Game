import socket
import threading

from client_game_functionality import ClientGameFunctionality


game = ClientGameFunctionality('10.137.137.98')
game.start_game_loop() # initializes the network, threads, starts game loop
