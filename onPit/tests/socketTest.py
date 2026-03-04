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
    print("Sending X")
    sock.sendall(b'X')
    print("Sending S")
    sock.sendall(b'S')
    data = recv_all(sock, 8)
    value, value2= struct.unpack('ff', data)
    print(value, value2)