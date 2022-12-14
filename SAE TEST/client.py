import socket, threading, sys

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
y = []
ip = open("fich.txt", "r")
for x in ip:
  y.append(str(x).replace("\n", ""))
lstcmd = ['connInfo','askOS', 'askRAM', 'askCPU', 'askIP', 'askNAME', 'pythonver', 'ping', 'kill', 'reset']


class Client():
    def __init__(self, host, port):
        self.__host = host
        self.__port = port
        self.__sock = socket.socket()
        self.__thread = None

    def connect(self) -> int:
        try:
            self.__sock.connect((self.__host, self.__port))
        except ConnectionRefusedError:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setText('Serveur déconnecté ou mauvaises données !')
            msg2.exec_()
            return -1
        except ConnectionError:
            print("Erreur de connexion")
            return -1
        else:
            print("Connexion réalisée")
            return 0

    def envoi(self,msg):
        self.__sock.send(msg.encode())
        rep = self.__sock.recv(1024).decode()
        return rep

    def reception(self, conn):
        msg = ""
        try:
            while msg != "kill" and msg != "disconnect" and msg != "reset":
                msg = conn.recv(1024).decode()
                print(msg)
        except:
            print('Serveur deconnecté !')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Connexion (IP - PORT)")
        lab2 = QLabel("Liste des machines : ")
        self.conn=Client('127.0.0.1',6824)
        self.__host = QLineEdit()
        self.__port = QLineEdit("6824")
        self.__logs = QTextEdit()
        self.__logs.setReadOnly(True)
        self.__lstcmd = QComboBox()
        self.__ok = QPushButton("Connexion")
        self.__status = QLabel("Statut : Déconnecté")
        snd = QPushButton('Send command')
        self.__select = QComboBox()
        for j in y:
            self.__select.addItem(j)
        quit = QPushButton("Quitter")
        grid.addWidget(lab2,0, 0)
        grid.addWidget(lab, 1, 0)
        grid.addWidget(self.__status,0,2)
        grid.addWidget(self.__host, 1, 1)
        grid.addWidget(self.__port, 1, 2)
        grid.addWidget(self.__select, 0, 1)
        grid.addWidget(self.__ok, 1, 3)
        grid.addWidget(self.__logs,2, 1)
        grid.addWidget(self.__lstcmd,2 ,0)
        grid.addWidget(snd,2,2)
        for x in lstcmd:
            self.__lstcmd.addItem(x)
        grid.addWidget(quit, 4, 0)
        self.combobox()
        quit.clicked.connect(self.closeEvent)
        self.__ok.clicked.connect(self.initcon)
        self.__select.activated.connect(self.combobox)
        snd.clicked.connect(self.sndmsg)
        self.setWindowTitle("Monitoring")



    def initcon(self):
        self.conn=Client(str(self.__host.text()), int(self.__port.text()))
        try:
            self.conn.connect()
        except:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setText('Erreur de connexion')
            msg2.exec_()
        else:
            self.__status.setText('Statut : Connecté')

    def sndmsg(self):
        if self.__status.text()=='Statut : Connecté':
            cmd = self.__lstcmd.currentText()
            try:
                self.__logs.append(cmd)
                self.conn.envoi(cmd)
                self.__logs.append(self.conn.envoi(cmd))
            except:
                pass

    def combobox(self):
        if self.__select.currentText() == y[0]:
            self.__host.setText(y[0])
        elif self.__select.currentText() == y[1]:
            self.__host.setText(y[1])
        else:
            self.__host.setText(y[2])

    def closeEvent(self, _e: QCloseEvent):
        box = QMessageBox()
        box.setWindowTitle("Quitter ?")
        box.setText("Voulez vous quitter ?")
        box.addButton(QMessageBox.Yes)
        box.addButton(QMessageBox.No)

        ret = box.exec()

        if ret == QMessageBox.Yes:
            QCoreApplication.exit(0)
        else:
            _e.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

# fichier : lire (contient differenttes ip serveur) il faut lire le fichier (on peut utiliser un open pr choisir le fichier. Lister les serveurs sur le cote

