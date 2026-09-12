# netmsg.py — shared by both client and server
import json
import struct

def send_msg(sock, obj: dict):
    data = json.dumps(obj).encode("utf-8")
    header = struct.pack("!I", len(data))  # 4 bytes integer lenght of the data
    sock.sendall(header + data)

def recieve_exact(sock, n): # recieves exactly n bytes
    buffer = bytearray()
    while len(buffer) < n:
        chunk = sock.recv(n - len(buffer))
        if not chunk:
            raise ConnectionError("socket closed mid-message")
        buffer.extend(chunk)
    return bytes(buffer)

def recieve_msg(sock) -> dict | None:
    try:
        header = recieve_exact(sock, 4)
    except ConnectionError:
        return None
    (length,) = struct.unpack("!I", header)
    payload = recieve_exact(sock, length)
    return json.loads(payload.decode("utf-8"))