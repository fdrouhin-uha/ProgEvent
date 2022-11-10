import socket
import threading

host = '127.0.0.1'
port = 6824
server = socket.socket()
server.bind((host, port))
server.listen(2) # Nombre de clients max qui seront connectés
conn1, address1 = server.accept()
conn2, address2 = server.accept()

def send(fromC, toC):
    while True:
        data = fromC.recv(1024).decode()
        toC.send(data.encode())


if __name__ == '__main__':
    t1 = threading.Thread(target= send, args= (conn1, conn2))
    t2 = threading.Thread(target= send, args= (conn2, conn1))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    conn1.close()
    conn2.close()