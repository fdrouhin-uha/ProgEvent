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
        print(data)
    client.close()

if __name__ == '__main__':
    t1 = threading.Thread(target=listen)
    t1.start()
    try:
        while True:
            data = input()
            client.send(data.encode())
            if data=='disconnect':
                data = ''
                break
        client.close()
        t1.join()
    except OSError:
        print('Le socket n\'est pas connecté !')
        co = str(input('Pour vous reconnecter tapper "yes" : '))
        if co == "yes":
            client.connect((host, port))
