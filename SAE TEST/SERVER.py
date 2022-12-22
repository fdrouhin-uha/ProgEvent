import os
import socket, subprocess, platform
import psutil as psutil
OS = platform.system()

def srv(server_socket,conn):
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
                conn, address = server_socket.accept()
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
                elif msg.startswith('ping'):
                    msgl = msg.split(' ')
                    host = msgl[1]
                    try:
                        ping(host,conn)
                    except:
                        conn.send('Ping échoué !'.encode())
                elif msg.lower().startswith('DOS:'):
                    if OS == 'DOS':
                        try:
                            msgl = msg.split(':')
                            cmd = msgl[1]
                            dos(conn,cmd)
                        except:
                            conn.send('Commande inconnue ou incorrecte'.encode())
                    else:
                        conn.send('L\'OS n\'est pas compatible avec la commande envoyée !'.encode())
                elif msg.lower().startswith('Linux:'):
                    if OS == 'Linux':
                        try:
                            msgl = msg.split(':')
                            cmd = msgl[1]
                            linux(conn,cmd)
                        except:
                            conn.send('Commande inconnue ou incorrecte'.encode())
                    else:
                        conn.send('L\'OS n\'est pas compatible avec la commande envoyée !'.encode())
                elif msg.lower().startswith('Powershell:'):
                    if OS == 'Windows':
                        try:
                            msgl = msg.split(':')
                            cmd = msgl[1]
                            powershell(conn, cmd)
                        except:
                            conn.send('Commande inconnue ou incorrecte'.encode())
                    else:
                        conn.send('L\'OS n\'est pas compatible avec la commande envoyée !'.encode())
                else:
                    conn.send('Commande non reconnue'.encode())
def connInfo(conn):
    info = 'Machine : ' + socket.gethostname() + ' | IP : ' + socket.gethostbyname(socket.gethostname())
    conn.send(info.encode())

def askOS(conn):
    os_name = platform.system()
    os_version = platform.release()
    os_info = f'Nom du système d’exploitation : {os_name}\nVersion du système d’exploitation : {os_version}'
    conn.send(os_info.encode())

def askRAM(conn):
    ram_used = psutil.virtual_memory().percent
    ram_available = psutil.virtual_memory().available
    ram_total = psutil.virtual_memory().total
    ram_used_str = f'{ram_used} %'
    ram_available_str = f'{round(ram_available / 1000000000, 1)} Go'
    ram_total_str = f'{round(ram_total / 1000000000, 1)} Go'
    conn.send(f'RAM totale : {ram_total_str} | RAM utilisée {ram_used_str} | RAM restante : {ram_available_str}'.encode())

def askCPU(conn):
    conn.send(f'Utilisation du CPU : {psutil.cpu_percent()} %'.encode())

def askIP(conn):
    ip_address = socket.gethostbyname(socket.gethostname())
    ip_address_str = f'Adresse IP : {ip_address}'
    conn.send(ip_address_str.encode())
def askNAME(conn):
    conn.send(f'Nom de la machine : {socket.gethostname()}'.encode())
def pythonver(conn):
    conn.send(subprocess.check_output('python --version', shell=True).decode('cp850').strip().encode())
def ping(host, conn):
    conn.send(subprocess.check_output('ping ' + host, shell=True).decode('cp850').strip().encode())

def dos(conn, cmd):
    result = os.system(cmd)
    conn.send(result)

def linux(conn,cmd):
    output = os.popen(cmd).read()
    conn.send(output)

def powershell(conn,cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    conn.send(completed.stdout)

def connect():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 6824))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    srv(server_socket,conn)

if __name__ == '__main__':
    connect()
