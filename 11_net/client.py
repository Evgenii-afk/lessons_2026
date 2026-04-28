import socket

client = socket.socket()
client.connect(('localhost', 9090))

while True:
    message = input()
    client.send(message.encode())
    
    data = client.recv(1024)

    if data.decode == '/deactivate':
        break

    if not data:
        break
    print(f"Server: {data.decode()}")