import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except:
            break
    print("Сервер отключился")

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))
    print("Подключено к серверу")
    
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()
    
    send_messages(client)
    
    client.close()

if __name__ == "__main__":
    main()