import socket

def clientchat():
    host = '127.0.0.1'
    port = 6824
    client_socket = socket.socket()
    client_socket.connect((host, port))
    message = input(" Entrez un message :  ")
    while message.lower().strip() != 'bye':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        if data == "bye":
            break
        print('Reçu du serveur : ' + data)
        message = input(" Répondre :  ")
    client_socket.close()


if __name__ == '__main__':
    clientchat()