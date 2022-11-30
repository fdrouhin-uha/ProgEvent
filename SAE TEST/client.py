import socket
import threading



if __name__ == '__main__':
    host = input('hostname : ')
    port = input('port : ')
    client = socket.socket
    client.connect((host, port))
    rep = client.send('cc'.encode())
        if rep == '':
            print('serv nn connecté')
        else:
            print(rep)