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
    print("Клиент отключился")

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message.lower() == 'exit':
            break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8888))
    server.listen(1)
    
    print("Сервер запущен. Ожидание подключения...")
    client_socket, addr = server.accept()
    print(f"Клиент {addr} подключился")
    
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()
    
    send_messages(client_socket)
    
    client_socket.close()
    server.close()

if __name__ == "__main__":
    main()