import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        widget = QWidget()
        self.setCentralWidget(widget)
        grid = QGridLayout()
        widget.setLayout(grid)
        lab = QLabel("Commandes")
        self.__text = QLineEdit("")
        self.__select = QComboBox()
        self.__select.addItem('OS')
        self.__select.addItem('RAM')
        self.__select.addItem('CPU')
        self.__select.addItem('IP')
        self.__select.addItem('NAME')
        self.__select.addItem('DISCONNECT')
        self.__select.addItem('KILL')
        self.__select.addItem('RESET')
        self.__select.addItem('Python version')
        self.__select.addItem('Ping IP')
        ok = QPushButton("Send Command")
        convert = QLabel("Résultat")
        self.__result = QLabel("")
        quit = QPushButton("Quitter")
        grid.addWidget(lab, 0, 0)
        grid.addWidget(ok, 1, 1)
        grid.addWidget(self.__select, 1, 0)
        grid.addWidget(convert, 2, 0)
        grid.addWidget(self.__result,2, 1)
        grid.addWidget(quit, 3, 0)
        quit.clicked.connect(self.actionQuitter)
        ok.clicked.connect(self.convert)
        self.setWindowTitle("Monitoring")


    def convert(self):
        try:
            if self.__select.currentText() == 'K -> C':
                x = float(self.__text.text()) - 273.15
                self.__result.setText(str(x))
            else:
                x = float(self.__text.text()) + 273.15
                self.__result.setText(str(x))
        except ValueError:
            msg2 = QMessageBox()
            msg2.setWindowTitle('Erreur')
            msg2.setText('Entrez un nombre !')
            msg2.exec_()

    def actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()