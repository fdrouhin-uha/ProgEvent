import socket


def server_program():
    host = '127.0.0.1'
    port = 6824
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(5)
    conn, address = server_socket.accept()
    print("Connection depuis : "+str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            server_socket.close()
            print('Utilisateur deconnecté, retour à l\'écoute')
            server_program()
        elif data =="arret":
            break
        print("Reçu d'un utilisateur connecté : "+str(data))
        data = input(' Répondre :  ')
        if data =="arret":
            break
        conn.send(data.encode())
    server_socket.close()

if __name__ == '__main__':
    server_program()