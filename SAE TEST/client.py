import pathlib, socket, threading, sys, re
import qdarkstyle
from PyQt5.QtGui import QCloseEvent, QIcon, QPalette, QColor
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
lstcmd = ['connInfo','askOS', 'askRAM', 'askCPU', 'askIP', 'askNAME', 'pythonver', 'ping', 'kill', 'reset', 'Commande personnalisée']

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
        rep = self.__sock.recv(8192).decode()
        return rep
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200,400)
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        widget.setLayout(grid)
        lab = QLabel("Connexion (IP - PORT)")
        lab2 = QLabel("Liste des machines : ")
        self.conn=Client('127.0.0.1',6824)
        self.__host = QLineEdit()
        self.__port = QLineEdit("6824")
        self.__logs = QTextEdit()
        self.__path = QLabel()
        self.__cmdman = QLineEdit()
        self.__logscmd = QTextEdit()
        self.__logscmd.setFixedSize(150,300)
        self.__logs.setReadOnly(True)
        self.__logscmd.setReadOnly(True)
        self.__lstcmd = QComboBox()
        self.__lstcmd.setEnabled(False)
        self.__ok = QPushButton("Connexion")
        self.__status = QLabel("Statut : Déconnecté")
        self.__status.setStyleSheet('color:red;' "border :2px solid;"
                                    "border-top-color : red;"
                                    "border-left-color :red;"
                                    "border-right-color :red;"
                                    "border-bottom-color : red;"
                                    "border-radius: 10px;")
        self.__status.setAlignment(Qt.AlignCenter)
        self.__snd = QPushButton('Envoi commande')
        self.__snd.setEnabled(False)
        self.__open = QPushButton('Ouvrir')
        self.__open.setStyleSheet("border :2px solid ;"
                             "border-top-color : green;"
                             "border-left-color :green;"
                             "border-right-color :green;"
                             "border-bottom-color : green;")
        self.__select = QComboBox()
        labhistory = QLabel('Historique des commandes')
        labhistory.setAlignment(Qt.AlignCenter)
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
        grid.addWidget(self.__logscmd, 2,3 )
        for x in lstcmd:
            self.__lstcmd.addItem(x)
        self.__lstcmd.setItemData(0, "Permet de recevoir des informations sur la connexion", Qt.ToolTipRole)
        self.__lstcmd.setItemData(1, "Demande l'OS et le type d'OS", Qt.ToolTipRole)
        self.__lstcmd.setItemData(2, "Demande la mémoire totale, mémoire utilisée et mémoire libre restante", Qt.ToolTipRole)
        self.__lstcmd.setItemData(3, "Demande l'utilisation de la CPU", Qt.ToolTipRole)
        self.__lstcmd.setItemData(4, "Renvoie l'adresse IP de la connexion", Qt.ToolTipRole)
        self.__lstcmd.setItemData(5, "Renvoie le nom de la machine", Qt.ToolTipRole)
        self.__lstcmd.setItemData(6, "Renvoie la version de python", Qt.ToolTipRole)
        self.__lstcmd.setItemData(7, "Ping vers une adresse IP définit ensuite", Qt.ToolTipRole)
        self.__lstcmd.setItemData(8, "Tue le serveur", Qt.ToolTipRole)
        self.__lstcmd.setItemData(9, "Redémarre le serveur", Qt.ToolTipRole)
        self.__lstcmd.setItemData(10, "Permet d\'envoyer une commande personnalisée", Qt.ToolTipRole)
        self.__cmdman.setPlaceholderText('Entrez une commande personnalisée')
        self.__logs.setPlaceholderText('Historique des résultats des commandes')
        grid.addWidget(quit, 4, 0)
        grid.addWidget(self.__cmdman,4 ,1)
        grid.addWidget(labhistory,4, 3)
        quit.clicked.connect(self.closeEvent)
        self.__ok.clicked.connect(self.initcon)
        self.__select.activated.connect(self.combobox)
        self.__snd.clicked.connect(self.sndmsg)
        self.__lstcmd.activated.connect(self.othercom)
        self.__open.clicked.connect(self.lstip)
        self.__cmdman.returnPressed.connect(self.cmdpers)
        self.setWindowTitle("Monitoring")

    def is_valid_ip(self, ip):
        regex = "^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
        if re.search(regex, ip):
            numbers = ip.split(".")
            for number in numbers:
                if int(number) > 255:
                    return False
            return True
        return False
    def initcon(self):
        if self.__ok.text()=='Connexion':
            self.conn=Client(self.__host.text(), int(self.__port.text()))
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
                self.__status.setStyleSheet('color: green;' "border :2px solid;"
                                            "border-top-color : lightgreen;"
                                            "border-left-color :lightgreen;"
                                            "border-right-color :lightgreen;"
                                            "border-bottom-color : lightgreen;"
                                            "border-radius: 10px;")
                self.__lstcmd.setEnabled(True)
                self.__snd.setEnabled(True)
                self.__cmdman.setEnabled(True)
                self.__ok.setText('Deconnexion')
        else:
            self.conn.envoi('disconnect')
            self.__ok.setText('Connexion')
            self.__lstcmd.setEnabled(False)
            self.__snd.setEnabled(False)
            self.__cmdman.setEnabled(False)
            self.__status.setText('Statut : Déconnecté')
            self.__status.setStyleSheet('color:red;' "border :2px solid;"
                                        "border-top-color : red;"
                                        "border-left-color :red;"
                                        "border-right-color :red;"
                                        "border-bottom-color : red;"
                                        "border-radius: 10px;")
    def lstip(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        self.__path.setText(path)
        last = pathlib.PurePath(path).name
        self.__select.clear()
        if path:
            if last.lower().endswith('.txt'):
                y = []
                ip = open(path, "r")
                for x in ip:
                    y.append(str(x).replace("\n", ""))
                for j in y:
                    self.__select.addItem(j)
                self.__select.addItem('Ajouter un hôte')
                self.combobox()
                self.__open.setStyleSheet('')
            else:
                msg2 = QMessageBox()
                msg2.setWindowTitle('Erreur')
                msg2.setIcon(QMessageBox.Critical)
                msg2.setText('Le fichier n\'est pas un fichier texte (.txt) ! ')
                msg2.exec_()

    def othercom(self):
        if self.__lstcmd.currentText() == 'ping':
            text, ok = QInputDialog.getText(self, 'IP', 'Adresse IP à ping :')
            if ok and self.is_valid_ip(text):
                try:
                    cmd = 'ping ' + text
                    self.__logscmd.append(cmd)
                    self.conn.envoi(cmd)
                    self.__logs.append(self.conn.envoi(cmd))
                except:
                    msg2 = QMessageBox()
                    msg2.setWindowTitle('Erreur')
                    msg2.setIcon(QMessageBox.Critical)
                    msg2.setText('Le ping ne passe pas !')
                    msg2.exec_()
            else:
                msg2 = QMessageBox()
                msg2.setWindowTitle('Erreur')
                msg2.setIcon(QMessageBox.Critical)
                msg2.setText('Adresse IP invalide !')
                msg2.exec_()
        elif self.__lstcmd.currentText() == 'Commande personnalisée':
            cmdpers, ok = QInputDialog.getText(self, 'Commande personnalisée', 'Commande')
            if ok:
                try:
                    self.__logscmd.append(cmdpers)
                    self.conn.envoi(cmdpers)
                    self.__logs.append(self.conn.envoi(cmdpers))
                except:
                    msg2 = QMessageBox()
                    msg2.setWindowTitle('Erreur')
                    msg2.setIcon(QMessageBox.Critical)
                    msg2.setText('Commande non reconnue par l\'OS !')
                    msg2.exec_()


    def cmdpers(self):
        cmd = self.__cmdman.text()
        if cmd:
            try:
                self.__logscmd.append(cmd)
                self.conn.envoi(cmd)
                self.__logs.append(self.conn.envoi(cmd))
                if cmd =='disconnect':
                    self.__ok.setText('Connexion')
                    self.__lstcmd.setEnabled(False)
                    self.__snd.setEnabled(False)
                    self.__cmdman.setEnabled(False)
                    self.__status.setText('Statut : Déconnecté')
                    self.__status.setStyleSheet('color:red;' "border :2px solid;"
                                                "border-top-color : red;"
                                                "border-left-color :red;"
                                                "border-right-color :red;"
                                                "border-bottom-color : red;"
                                                "border-radius: 10px;")
            except:
                msg2 = QMessageBox()
                msg2.setWindowTitle('Erreur')
                msg2.setIcon(QMessageBox.Critical)
                msg2.setText('Commande non reconnue!')
                msg2.exec_()
        else:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setIcon(QMessageBox.Critical)
            msg2.setText('Vous n\'avez pas entré de commande !')
            msg2.exec_()

    def sndmsg(self):
        if self.__status.text()=='Statut : Connecté':
            cmd = self.__lstcmd.currentText()
            try:
                self.__logscmd.append(cmd)
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
        if self.__select.currentText() == 'Ajouter un hôte':
            text, ok = QInputDialog.getText(self, 'Ajout d\'un hôte', 'Adresse IP à ajouter')
            if ok:
                if self.is_valid_ip(text):
                    self.__select.insertItem(self.__select.count() -1 ,text)
                    path = self.__path.text()
                    with open(path, 'a') as f:
                        f.write("\n" + text)
                else:
                    msg2 = QMessageBox()
                    msg2.setWindowTitle('Erreur')
                    msg2.setIcon(QMessageBox.Critical)
                    msg2.setText('Format d\'adresse IP invalide !')
                    msg2.exec_()
        self.__host.setText(self.__select.currentText())

    def closeEvent(self, _e: QCloseEvent):
        box = QMessageBox()
        box.setWindowTitle("Quitter ?")
        box.setText("Voulez vous quitter ?")
        box.addButton(QMessageBox.Yes)
        box.addButton(QMessageBox.No)
        ret = box.exec()

        if ret == QMessageBox.Yes:
            self.__select.clear()
            self.conn.envoi('disconnect')
            QCoreApplication.exit(0)
        else:
            _e.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


