import socket, struct, time

def recv_all(sock, length):
    data = b''
    while(len(data) < length):
        packet = sock.recv(length - len(data))
        if not packet:
            raise ConnectionError("SocketClosed")
        data += packet
    return data

sock = socket.create_connection(("127.0.0.1", 5000))

for _ in range(10):
    print("Sendind X")
    sock.sendall(b'X')
    print("Waiting for response")
    data = recv_all(sock, 4)
    value = struct.unpack('f', data)[0]
    print(value)
for _ in range(10):
    sock.sendall(b'S')
    data = recv_all(sock, 4)
    value = struct.unpack('f', data)[0]
    print(value)