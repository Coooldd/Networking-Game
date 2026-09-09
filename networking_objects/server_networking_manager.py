import socket
import json
import time

class ServerNetworkingManager():
    def __init__(self, port=6782):
        self.host = socket.gethostbyname(socket.gethostname())
        self.PORT = 6782

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.PORT))

        print("Server started")

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
                data = client_socket.recv(1024)
                if not data: 
                    break # client disconnected
                # update data here.
                
        except ConnectionResetError:
            print(f"Player {client_address} disconnected")
        finally:
            client_socket.close()
            print(f"Thread ended, connection closed for {client_address}")