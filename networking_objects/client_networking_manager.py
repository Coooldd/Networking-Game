import socket
import json

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
        try:
            self.conn.sendall(json.dumps(data).encode('utf-8'))
        except socket.error as e:
            print(f"Error sending data: {e}")

    def recieve_data(self):
        try:
            raw_data = self.conn.recv(2048).decode('utf-8')
            if not raw_data:
                return {}
            return json.loads(raw_data)
        except Exception as e:
            print(f"Error receiving data: {e}")
            return {}