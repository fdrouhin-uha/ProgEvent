import socket
import subprocess
import psutil
import platform
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
            data = ''
            conn, address = server.accept()
        elif data =="kill":
            break
        elif data =='reset':
            server.close()
            print('Redémarrage du serveur, veuillez patienter ...')
            data=''
            socketsrv()
        elif data =="connInfo":
            info = 'Machine : ' + socket.gethostname() + ' | IP : ' + socket.gethostbyname(socket.gethostname())
            conn.send(info.encode())
        elif data == 'askOS':
            p = subprocess.getoutput('systeminfo | findstr /B /C:"Nom du système d’exploitation:"')
            p2 = subprocess.getoutput('systeminfo | findstr /B /C:"Version du syst"')
            if p =='':
                p = subprocess.getoutput('systeminfo | findstr /B /C:"OS Name : "')
                conn.send(p.encode())
            conn.send(p.encode())
            conn.send(p2.encode())
        elif data =='askRAM':
            ram = psutil.virtual_memory().percent
            ram2 = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
            ram3 = psutil.virtual_memory().total / 1000000000
            conn.send(f'RAM totale : {round(ram3,1)} Go | RAM utilisée {ram} % | RAM restante : {round(ram2,1)} %'.encode())
        elif data == 'askCPU':
            conn.send(f'Utilisation du CPU : {psutil.cpu_percent()} %'.encode())
        elif data == 'askIP':
            conn.send(subprocess.getoutput('ipconfig | findstr /i "Adresse IPv4"').encode())
        elif data == 'askNAME':
            conn.send(f'Nom de la machine : {socket.gethostname()}'.encode())
        elif data =='pythonver':
            conn.send(subprocess.getoutput('python --version').encode())
        elif data =='ping 192.168.197.1':
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', '192.168.197.1']
            return subprocess.call(command) == 0
        print("Reçu d'un utilisateur connecté : "+str(data))
    server.close()

if __name__ == '__main__':
    socketsrv()
