import threading
import socket

from networking_objects.server_networking_manager import ServerNetworkingManager

server_networking_manager = ServerNetworkingManager()


for client_socket, client_address in server_networking_manager.listen():
    t = threading.Thread(target=server_networking_manager.client_begin_point, args=(client_socket, client_address))
    t.start()
