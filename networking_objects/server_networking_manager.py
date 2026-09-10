import socket
import json
import time

from networking_objects.net_msg import send_msg, recieve_exact, recieve_msg

class ServerNetworkingManager():
    def __init__(self, port=6782):
        self.host = socket.gethostbyname(socket.gethostname())
        self.PORT = 6782

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.PORT))

        print("Server started")

        self.data = dict()

    def listen(self):
        print("Waiting for players to connect...\n")
        self.server.listen()

        while True:
            communication_socket, address = self.server.accept()
            print(f"Got a connection from {address}")
            yield communication_socket, address # while loop still runs after we get a connection

    def client_begin_point(self, client_socket, client_address):
        print(f"New thread started for client {client_address}")
        try:
            while True:
                client_input = recieve_msg(client_socket)
                print(client_input)
                # parse client input into a queue, for a main server thread to update game state objects
                send_msg(client_socket, self.data) # self.data should be only the relevant data for the player
                # update data here.
                
        except ConnectionResetError:
            print(f"Player {client_address} disconnected")
        finally:
            client_socket.close()
            print(f"Thread ended, connection closed for {client_address}")

    def send_data(self, data: dict):
        send_msg(self.server, data)

    def recieve_data(self): # receieves one message sent by the server.
        return recieve_msg(self.server)