import socket

from networking_objects.net_msg import send_msg, recieve_msg


class NetworkServer:
    """
    Pure networking layer. Owns the listening socket, accepts connections,
    and runs a generic per-client loop.
    """

    def __init__(self, port=6782, host=None):
        self.host = host or socket.gethostbyname(socket.gethostname())
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))

    def listen(self): # main function where server listens for users
        print("Waiting for players to connect...\n")
        self.server_socket.listen()

        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Got a connection from {address}")
            yield client_socket, address

    def run_client_loop(self, client_socket, client_address, *, on_connect, on_message, on_disconnect):
        """
        on_connect(address) -> client_id
        on_message(client_id, message) -> dict to send back
        on_disconnect(client_id) -> None
        """
        print(f"New thread started for client {client_address}")
        client_id = on_connect(client_address) # on_connect is registering the player to the queue, then returning the new ID

        try:
            while True:
                message = recieve_msg(client_socket)
                response = on_message(client_id, message) # this responses should match server_to_client.json
                send_msg(client_socket, response)
        except ConnectionError:
            print(f"Player {client_address} disconnected")
        finally:
            client_socket.close()
            on_disconnect(client_id) # send the queue: REMOVE_PLAYER, client_id
            print(f"Thread ended, connection closed for {client_address}")