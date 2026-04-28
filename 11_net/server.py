import socket
from time import sleep

server = socket.socket()
server.bind(('localhost', 9090))
server.listen(1)
client, addr = server.accept()
print("Connected", addr)

while True:
    data = client.recv(1024)
    if not data:
        break
    print(data.decode())
    
    message = input()

    if message.split()[0] == '/sleep':
        print(f"Режим сна: {message.split()[1]} c")
        sleep(int(message.split()[1]))

    if message == '/deactivate':
        client.send(message.encode())
        break
    
    client.send(message.encode())

