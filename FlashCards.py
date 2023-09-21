import PyQt5 as py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi("./HomePage.ui", self)
        self.show()

        self.loginb.clicked.connect(self.login)

    def login(self):
        if self.username.text() == "test1" and self.password.text() == "pass1":
            self.success.setEnabled(True)
            message2 = QMessageBox()
            message2.setText("Login Successful")
            message2.exec()
        else:
            message = QMessageBox()
            message.setText("Invalid Login")
            message.exec()

def main():
    app = QApplication([])
    window = GUI()
    app.exec_()

main()
