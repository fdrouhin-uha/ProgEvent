import socket

host = '127.0.0.1'
port = 6824
server = socket.socket()
server.bind((host, port))
server.listen(2)

def server_program():
    conn, address = server.accept()
    print("Connection depuis : "+str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            print('Utilisateur deconnecté, retour à l\'écoute')
            conn, address = server.accept()
        elif data =="disconnect":
            conn.close()
            print('Utilisateur deconnecté, retour à l\'écoute')
            conn, address = server.accept()
        elif data =="kill":
            break
        elif data =='reset':
            server.close()
            server_program()
        print("Reçu d'un utilisateur connecté : "+str(data))
    server.close()

if __name__ == '__main__':
    server_program()
