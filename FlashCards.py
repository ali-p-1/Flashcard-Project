import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
from DB import db_creation

db_creation()

class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        uic.loadUi("./HomePage.ui", self)
        self.show()
        self.loginb.clicked.connect(self.login)

    def login(self): 
        user = self.username.text()
        passw = self.password.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE Username = ? AND Password = ? ", (user, passw))
        result = cursor.fetchone()
        if result:
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
