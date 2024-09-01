import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "NICKNAME":
                client_socket.send(nickname.encode("utf-8"))
            else:
                print(message)
        except:
            print("An error occurred. Closing connection.")
            client_socket.close()
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    global nickname
    nickname = input("Enter your nickname: ")

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input("")
        if message:
            client_socket.send(f"<{nickname}> {message}".encode('utf-8'))
        else:
            client_socket.close()
            break

start_client()