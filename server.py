import socket
from threading import Thread

HOST = '0.0.0.0'
PORT = 8080
users =[]

def broadcast(data, exclude_socket = None):
    for client in users:
        if client != exclude_socket:
            try:
                client.sendall(data)
            except:
                pass

def handle_client(connection):
    while True:
        try:
            data = connection.recv(4096)
            if not data:
                break
            broadcast(data, exclude_socket=connection)
        except:
            break

    
    if connection in users:
        users.remove(connection)
    connection.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    while True:
        connection, address = server_socket.accept()
        users.append(connection)

        t = Thread(target=handle_client, args=(connection, ))
        t.start()

if __name__ == '__main__':
    main()

