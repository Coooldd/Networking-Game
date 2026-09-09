import socket

from game_objects.game_functionality import GameFunctionality

SERVER_HOST = '10.137.148.149' # <- do later: change dynamically instead of hard coded
PORT = 6782

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

with client:
    try:
        print(f"Connecting to server at {SERVER_HOST}:{PORT}...")
        client.connect((SERVER_HOST, PORT))
        print("Successfully connected to the server!")

        game = GameFunctionality()
        game.game_loop()
    except ConnectionRefusedError:
        print("Could not connect.")
