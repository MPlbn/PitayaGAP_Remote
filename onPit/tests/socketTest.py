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
sendval:float = 1.34
for _ in range(10):
    print("Sending S")
    sock.sendall(b'S')
    print("Waiting for R...")
    ready = sock.recv(1, 0)
    print(f"Recieved: {ready}")
    if(ready == b'R'):
        print(f'Sending value: {sendval}')
        sock.sendall(struct.pack('f', sendval))
        data = recv_all(sock, 8)
        value, value2= struct.unpack('ff', data)
        print('recieved:', value, value2)
    else:
        print("something went wrong...")