import socket
import subprocess
import threading

import psutil
import platform

class Server:
    def __init__(self, hostname, port):
        self.__port = port
        self.__hostname = port
        self.__socket = None

    def isConnected(self):
        return (self.__socket!=None)

    def __connect(self):
        socket = socket.socket()
        socket.connect((self.__hostname, self.__port))

    def __send(self,message):
        if self.isConnected():
            socket.send(message.encode())
            msg = self.__socket.recv(1024).decode()
            print(msg)
        else:
            print('Pas de connexion')

    def __close(self):
        socket.close()

    def connect(self):
        threading.Thread(target=self.__connect)
    def send(self):
        threading.Thread(target=self.__send)
