import socket
import threading

host = '127.0.0.1'
port = 6824
server = socket.socket()
server.bind((host, port))
clients = 8
server.listen(clients) # Nombre de clients max qui seront connectés
conn1, address1 = server.accept()
conn2, address2 = server.accept()
conn3, address3 = server.accept()
conn4, address4 = server.accept()
conn5, address5 = server.accept()
conn6, address6 = server.accept()
conn7, address7 = server.accept()
conn8, address8 = server.accept()



def send(fromC, toC):
    while True:
        data = fromC.recv(1024).decode()
        toC.send(data.encode())


if __name__ == '__main__':
    T = []
    for i in range(clients):
        T.append(threading.Thread(target = send, args= (conn+str(i), conn1)))
    conn1.close()
    conn2.close()