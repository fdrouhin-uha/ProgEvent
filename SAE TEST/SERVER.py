import socket, subprocess, platform
import psutil as psutil


def data(server_socket,conn):
    while True:
        try:
         msg = conn.recv(1024).decode()
        except OSError:
            return ('Socket non connecté')
        else:
            if msg =='disconnect':
                conn.send(msg.encode())
                print('Deconnexion du socket')
                conn.close()
            else:
                print("Client : ",msg)
            if msg == 'kill':
                conn.send(msg.encode())
                print('Fermeture du serveur')
                conn.close()
                server_socket.close()
            elif msg == 'reset':
                conn.send(msg.encode())
                conn.close()
                server_socket.close()
                print('Reset du serveur')
                connect()
            else:
                if msg == 'connInfo':
                    connInfo(conn)
                elif msg == 'askOS':
                    askOS(conn)
                elif msg == 'askRAM':
                    askRAM(conn)
                elif msg == 'askCPU':
                    askCPU(conn)
                elif msg == 'askIP':
                    askIP(conn)
                elif msg == 'askNAME':
                    askNAME(conn)
                elif msg == 'pythonver':
                    pythonver(conn)
                elif msg[0:4] == 'ping':
                    msgl = msg.split(' ')
                    host = msgl[1]
                    ping(host,conn)

def connInfo(conn):
    info = 'Machine : ' + socket.gethostname() + ' | IP : ' + socket.gethostbyname(socket.gethostname())
    conn.send(info.encode())

def askOS(conn):
    p = subprocess.getoutput('systeminfo | findstr /B /C:"Nom du système d’exploitation:"')
    p2 = subprocess.getoutput('systeminfo | findstr /B /C:"Version du syst"')
    if p == '':
        p = subprocess.getoutput('systeminfo | findstr /B /C:"OS Name : "')
        conn.send(p.encode())
    conn.send(p.encode())
    conn.send(p2.encode())

def askRAM(conn):
    ram = psutil.virtual_memory().percent
    ram2 = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    ram3 = psutil.virtual_memory().total / 1000000000
    print(ram + ram2 + ram3)
    conn.send(f'RAM totale : {round(ram3, 1)} Go | RAM utilisée {ram} % | RAM restante : {round(ram2, 1)} %'.encode())


def askCPU(conn):
    conn.send(f'Utilisation du CPU : {psutil.cpu_percent()} %'.encode())
def askIP(conn):
    conn.send(subprocess.getoutput('ipconfig | findstr /i "Adresse IPv4"').encode())
def askNAME(conn):
    conn.send(f'Nom de la machine : {socket.gethostname()}'.encode())
def pythonver(conn):
    conn.send(subprocess.getoutput('python --version').encode())
def ping(host, conn):
    conn.send(subprocess.getoutput('ping ' + host).encode())

def connect():
    server_socket = socket.socket()
    server_socket.bind(('127.0.0.1', 6824))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    data(server_socket,conn)

if __name__ == '__main__':
    connect()