import socket, threading, sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
y = []
ip = open("fich.txt", "r")
for x in ip:
  y.append(str(x).replace("\n", ""))

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

    def __reception(self, conn):
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
        self.__host = QLineEdit()
        self.__port = QLineEdit("6824")
        self.__msgcmd = QLineEdit()
        ok = QPushButton("Connexion")
        snd = QPushButton('Test')
        self.__select = QComboBox()
        self.__select.addItem(y[0])
        self.__select.addItem(y[1])
        self.__select.addItem(y[2])
        self.__result = QLabel("")
        quit = QPushButton("Quitter")
        grid.addWidget(lab2,0, 0)
        grid.addWidget(lab, 1, 0)
        grid.addWidget(self.__host, 1, 1)
        grid.addWidget(self.__port, 1, 2)
        grid.addWidget(self.__select, 0, 1)
        grid.addWidget(ok, 1, 3)
        grid.addWidget(quit, 4, 0)
        self.combobox()
        quit.clicked.connect(self.actionQuitter)
        ok.clicked.connect(self.initcon)
        self.__select.activated.connect(self.combobox)
        self.setWindowTitle("Monitoring")


    def combobox(self):
        if self.__select.currentText() == y[0]:
            self.__host.setText(y[0])
        elif self.__select.currentText() == y[1]:
            self.__host.setText(y[1])
        else:
            self.__host.setText(y[2])


    def initcon(self):
        client=Client(str(self.__host.text()), int(self.__port.text()))
        try:
            client.connect()
        except:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setText('Erreur de connexion')
            msg2.exec_()



    def actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

# fichier : lire (contient differenttes ip serveur) il faut lire le fichier (on peut utiliser un open pr choisir le fichier. Lister les serveurs sur le cote

