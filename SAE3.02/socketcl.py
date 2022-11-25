import socket
import threading
machine1 = ['127.0.0.1',6824]
client = socket.socket()


def connexion(machine):
    client.connect((machine[0],machine[1]))
    t1 = threading.Thread(target=listen)
    t2 = threading.Thread(target=write)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

def listen():
    while True:
        data = client.recv(1024).decode()
        if not data:
            break
        print(' Reçu : ' + data)
    client.close()


def write():
    while True:
        try:
            data = input()
            if data == "arret":
                break
            elif data =="disconnect":
                client.send(data.encode())
                client.close()
                connexion(machine1)
            client.send(data.encode())
        except OSError:
            print('Le socket n\'est pas connecté !')
            co = str(input('Pour vous reconnecter tapper "yes" : '))
            if co == "yes":
                connexion(machine1)
    client.close()

if __name__ == '__main__':
    connexion(machine1)