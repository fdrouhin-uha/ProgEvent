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
        if not data:
            break
        elif data == 'disconnect':
            conn.close()
            print('Client déconnecté')
            connexion()
        elif data == 'askOS':
            data = 'cmd ok'
            conn.send(data.encode())
        elif data == 'askRAM':
            data = 'cmd ok'
            conn.send(data.encode())
        elif data == 'askCPU':
            data = 'cmd ok'
            conn.send(data.encode())
        elif data == 'askIP':
            data = 'cmd ok'
            conn.send(data.encode())
        elif data == 'askNAME':
            data = 'cmd ok'
            conn.send(data.encode())
        print(' Reçu : ' + data)
    conn.close()

def connexion():
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=write)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    conn.close()

def write():
    while True:
        data = input()
        if data == "arret":
            server.close()
        conn.send(data.encode())

if __name__ == '__main__':
    connexion()
