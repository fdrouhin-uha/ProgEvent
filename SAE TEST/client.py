import pathlib
import socket, threading, sys

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800,400)
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
        self.__logs.adjustSize()
        self.__lstcmd = QComboBox()
        self.__lstcmd.setEnabled(False)
        self.__ok = QPushButton("Connexion")
        self.__status = QLabel("Statut : Déconnecté")
        self.__snd = QPushButton('Envoi commande')
        self.__snd.setEnabled(False)
        self.__open = QPushButton('Ouvrir')
        self.__open.setStyleSheet("border :5px solid ;"
                             "border-top-color : red; "
                             "border-left-color :blue;"
                             "border-right-color :blue;"
                             "border-bottom-color : red")
        self.__select = QComboBox()
        quit = QPushButton("Quitter")
        grid.addWidget(lab2,0, 0)
        grid.addWidget(lab, 1, 0)
        grid.addWidget(self.__status,0,2)
        grid.addWidget(self.__open, 0, 3)
        grid.addWidget(self.__host, 1, 1)
        grid.addWidget(self.__port, 1, 2)
        grid.addWidget(self.__select, 0, 1)
        grid.addWidget(self.__ok, 1, 3)
        grid.addWidget(self.__logs,2, 1)
        grid.addWidget(self.__lstcmd,2 ,0)
        grid.addWidget(self.__snd,2,2)
        for x in lstcmd:
            self.__lstcmd.addItem(x)
        grid.addWidget(quit, 4, 0)
        quit.clicked.connect(self.closeEvent)
        self.__ok.clicked.connect(self.initcon)
        self.__select.activated.connect(self.combobox)
        self.__snd.clicked.connect(self.sndmsg)
        self.__lstcmd.activated.connect(self.othercom)
        self.__open.clicked.connect(self.lstip)
        self.setWindowTitle("Monitoring")




    def initcon(self):
        self.conn=Client(str(self.__host.text()), int(self.__port.text()))
        try:
            self.conn.connect()
        except:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setIcon(QMessageBox.Critical)
            msg2.setText('Erreur de connexion')
            msg2.exec_()
        else:
            self.__status.setText('Statut : Connecté')
            self.__lstcmd.setEnabled(True)
            self.__snd.setEnabled(True)


    def lstip(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        last = pathlib.PurePath(path).name
        if last.lower().endswith('.txt'):
            y = []
            ip = open(path, "r")
            for x in ip:
                y.append(str(x).replace("\n", ""))
            for j in y:
                self.__select.addItem(j)
            self.combobox()
            self.__open.setStyleSheet('')
            self.__open.setEnabled(False)
        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setIcon(QMessageBox.Critical)
            msg2.setText('Le fichier n\'est pas un fichier texte (.txt) ! ')
            msg2.exec_()

    def othercom(self):
        if self.__lstcmd.currentText() == 'ping':
            text, ok = QInputDialog.getText(self, 'IP', 'Adresse IP à ping :')
            if ok:
                try:
                    cmd = 'ping ' + text
                    self.__logs.append(cmd)
                    self.conn.envoi(cmd)
                    self.__logs.append(self.conn.envoi(cmd))
                except:
                    msg2 = QMessageBox()
                    msg2.setWindowTitle('Erreur')
                    msg2.setIcon(QMessageBox.Critical)
                    msg2.setText('Adresse IP invalide !')
                    msg2.exec_()

    def sndmsg(self):
        if self.__status.text()=='Statut : Connecté':
            cmd = self.__lstcmd.currentText()
            try:
                self.__logs.append(cmd)
                self.conn.envoi(cmd)
                self.__logs.append(self.conn.envoi(cmd))
            except:
                pass
        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setIcon(QMessageBox.Critical)
            msg2.setText('Vous n\'êtes pas connecté !')
            msg2.exec_()


    def combobox(self):
        self.__host.setText(self.__select.currentText())

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

