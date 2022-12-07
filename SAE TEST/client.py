import socket, threading, sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


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
            print("Serveur non lancé ou mauvaises informations")
            return -1
        except ConnectionError:
            print("Erreur de connexion")
            return -1
        else:
            print("Connexion réalisée")
            return 0

    def dialogue(self):
        msg = ""
        self.__thread = threading.Thread(target=self.__reception, args=[self.__sock, ])
        self.__thread.start()
        while msg != "kill" and msg != "disconnect" and msg != "reset":
            msg = self.__envoi()
        self.__thread.join()
        self.__sock.close()

    def __envoi(self):
        msg = input()
        try:
            self.__sock.send(msg.encode())
        except BrokenPipeError:
            print("erreur, socket fermé")
        return msg

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
        self.__host = QLineEdit()
        self.__port = QLineEdit()
        ok = QPushButton("Connexion")
        self.__result = QLabel("")
        quit = QPushButton("Quitter")
        grid.addWidget(lab, 0, 0)
        grid.addWidget(self.__host, 0, 1)
        grid.addWidget(self.__port, 0, 2)
        grid.addWidget(ok, 0, 3)
        grid.addWidget(quit, 3, 0)
        quit.clicked.connect(self.actionQuitter)
        ok.clicked.connect(self.initcon)
        self.setWindowTitle("Monitoring")

    def initcon(self):
        if str(self.__host.text()) == '' or int(self.__port.text()) == '':
            raise OSError
        client=Client(str(self.__host.text()), int(self.__port.text()))
        try:
            client.connect()
        except OSError:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setText('Serveur déconnecté ou mauvaises données !')
            msg2.exec_()
        else:
            client.dialogue()


    def actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()



