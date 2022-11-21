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
        lab = QLabel("Température")
        self.__lab2 = QLabel("")
        self.__lab3= QLabel("")
        self.__lab4=QLabel("")
        self.__text = QLineEdit("")
        self.__select = QComboBox()
        self.__select.addItem('C -> K')
        self.__select.addItem('K -> C')
        ok = QPushButton("Convertir")
        convert = QLabel("Conversion")
        self.__result = QLabel("")
        quit = QPushButton("Quitter")
        help = QPushButton('?')
        grid.addWidget(lab, 0, 0)
        grid.addWidget(self.__text, 0, 1)
        grid.addWidget(self.__lab3, 0, 2)
        grid.addWidget(ok, 1, 1)
        grid.addWidget(self.__select, 1, 2)
        grid.addWidget(convert, 2, 0)
        grid.addWidget(self.__result,2, 1)
        grid.addWidget(self.__lab4, 2, 2)
        grid.addWidget(quit, 3, 0)
        grid.addWidget(self.__lab2, 2, 0)
        grid.addWidget(help, 3, 2)
        self.combobox()
        quit.clicked.connect(self.actionQuitter)
        ok.clicked.connect(self.convert)
        self.__select.activated.connect(self.combobox)
        help.clicked.connect(self.popup)
        self.setWindowTitle("Température")

    def combobox(self):
        if self.__select.currentText() == 'K -> C':
            self.__lab3.setText('K')
            self.__lab4.setText('° C')
        else:
            self.__lab3.setText('° C')
            self.__lab4.setText('K')

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

    def popup(self):
        msg = QMessageBox()
        msg.setWindowTitle('Aide')
        msg.setText('Permet de convertir un nombre soit de Kelvin vers Celsius, soit de Celsius vers Kelvin.')
        msg.exec_()

    def actionQuitter(self):
        QCoreApplication.exit(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()