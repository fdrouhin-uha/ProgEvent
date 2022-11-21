import socket
import threading
host = '127.0.0.1'
port = 6824
client = socket.socket()
client.connect((host, port))

def listen():
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        elif data == 'bye':
            break
        print(' Reçu : ' + data)
    client.close()

def write():
    while True:
        data = input()
        if data == "arret":
            break
        client.send(data.encode())
    client.close()

if __name__ == '__main__':
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=write)
    t1.start()
    t2.start()
    t1.join()
    t2.join()