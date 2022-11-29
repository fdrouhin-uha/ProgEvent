import socket
import threading

host = '127.0.0.1'
port = 6824
server = socket.socket()
server.bind((host, port))
server.listen(2)
conn, address = server.accept()

def listen():
    while True:
        data = conn.recv(1024).decode()
        print(' Reçu : ' + data)
        if not data:
            conn.close()
            break
        elif data == 'bye':
            conn.close()
            break
        elif data == 'arret':
            server.close()
            break
    print('Déconnexion')

if __name__ == '__main__':
    t1 = threading.Thread(target=listen)
    t1.start()
    while True:
        data = input()
        if data == "arret":
            break
        conn.send(data.encode())
    t1.join()