import socket
import threading
client = socket.socket()
host = '127.0.0.1'
port = 6824
client.connect((host, port))

def send():
    while True:
        data = input()
        client.send(data.encode())

def receive():
    while True:
        data = client.recv(1024).decode()
        print(" Reçu : ", data)

if __name__ == '__main__':
    t1 = threading.Thread(target= send)
    t2 = threading.Thread(target= receive)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
