import socket
import threading

host = '127.0.0.1'
port = 6824
server = socket.socket()
server.bind((host, port))
server.listen(2) # Nombre de clients max qui seront connectés
conn, address = server.accept()


def listen():
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        elif data == 'bye':
            break
        print(' Reçu : ' + data)
    conn.close()
    print('Déconnexion')

if __name__ == '__main__':
    t1 = threading.Thread(target=listen)
    t1.start()
    data =''
    while data !='bye':
        data = input()
        if data == 'arret':
            conn.close()
            server.close()
            listen()
        conn.send(data.encode())
    print('Déconnexion')
    t1.join()