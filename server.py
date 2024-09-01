import socket
import threading

clients = []
nicknames = []
host = "127.0.0.1"
port = 5555

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            broadcast(message,client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def broadcast(message, current_client):
    for client in clients:
        if client != current_client:
            try:
                client.send(message.encode("utf-8"))
            except:
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames[index]
                broadcast(f"{nickname} has left the chat.".encode("utf-8"))
                nicknames.remove(nickname)
                client.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(5)
    print(f"Server started on port {port}.")

    while True:
        client_socket, client_address = server.accept()
        print(f"New connection from {client_address}.")
        clients.append(client_socket)
        client_socket.send("NICKNAME".encode("utf-8"))
        nickname = client_socket.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        thread = threading.Thread(target = handle_client, args = (client_socket,))
        thread.start()

start_server()