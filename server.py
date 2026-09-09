import threading
import socket

host = socket.gethostbyname(socket.gethostname())
PORT = 6782

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, PORT))

threads = []

def client_begin_point(client_socket) -> None:
    pass

server.listen()

while True:
    communication_socket, address = server.accept()
    print(f"Got a connection from {address}, initializating player...")

    t = threading.Thread(target=client_begin_point, args=[communication_socket])
    threads.append(t)
    t.start()