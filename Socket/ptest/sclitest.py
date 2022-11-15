import socket
import threading
host = '127.0.0.1'
port = 6824
client = socket.socket()
client.connect((host, port))

def listen(socket):
    while True:
        data = client.recv(1024).decode()
        print(' Reçu : ' + data)
        if not data:
            break
        elif data == 'bye':
            break
    client.close()

if __name__ == '__main__':
    t1 = threading.Thread(target=listen, args=[client])
    t1.start()
    while True:
        data = input()
        if data == "arret":
            client.close()
        client.send(data.encode())
    t1.join()
    client.close()
