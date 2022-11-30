import socket
import subprocess
import threading
import psutil
import platform

class Server:
    def __init__(self, hostname, port):
        self.__port = port
        self.__hostname = hostname
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def isConnected(self):
        return (self.__socket!=None)

    def __connect(self):
        self.__socket.bind((self.__hostname, self.__port))
        self.__socket.listen(2)

    def listen(self):
        conn, addr = self.__socket.accept()
        print("Connection depuis : " + str(addr))
        while True:
            data = conn.recv(1024).decode()
            print(data)

    def __send(self,message):
        if self.isConnected():
            self.__socket.send(message.encode())
            msg = self.__socket.recv(1024).decode()
            print(msg)
        else:
            print('Pas de connexion')

    def close(self):
        self.__socket.close()

    def connect(self):
        threading.Thread(target=self.__connect)

    def send(self):
        threading.Thread(target=self.__send)


if __name__ == '__main__':
    srv1 = Server('127.0.0.1', 6824)
    srv1.connect()
    srv1.send()
    srv1.listen()