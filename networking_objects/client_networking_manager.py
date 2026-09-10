import socket
import json

from networking_objects.net_msg import send_msg, recieve_exact, recieve_msg

class ClientNetworkingManager():
    def __init__(self, server_host, port=6782):
        self.server_host = server_host
        self.port = port

        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.inputs = dict()

        try:
            print(f"Connecting to server at {self.server_host}:{self.port}...")
            self.conn.connect((self.server_host, self.port))
            print("Successfully connected to the server!")
        except ConnectionRefusedError:
            print("Could not connect.")

    def send_data(self, data: dict):
        send_msg(self.conn, data)

    def recieve_data(self): # receieves one message sent by the server.
        return recieve_msg(self.conn)