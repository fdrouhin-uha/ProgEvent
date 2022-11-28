import socket
import subprocess
host = '127.0.0.1'
port = 6824


def socketsrv():
    server = socket.socket()
    server.bind((host, port))
    print("Serveur opérationnel")
    server.listen(2)
    conn, address = server.accept()
    print("Connection depuis : "+str(address))
    while True:
        data = conn.recv(1024).decode()
        if not data:
            conn.close()
            print('Utilisateur deconnecté, retour à l\'écoute')
            conn, address = server.accept()
        elif data =="disconnect":
            conn.close()
            print('Utilisateur deconnecté, retour à l\'écoute')
            conn, address = server.accept()
        elif data =="kill":
            break
        elif data =='reset':
            server.close()
            print('Redémarrage du serveur, veuillez patienter ...')
            socketsrv()
        elif data =="connInfo":
            info = ' Machine : ' + socket.gethostname() + ' | IP : ' + socket.gethostbyname(socket.gethostname())
            conn.send(info.encode())
        elif data == 'askOS':
            p = subprocess.getoutput('systeminfo | findstr /B /C:"Nom du système d’exploitation:"')
            print(p)
            conn.send(p.encode())
        print("Reçu d'un utilisateur connecté : "+str(data))
    server.close()

if __name__ == '__main__':
    socketsrv()
