import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
# from DB import create_database

# create_database() 
 
class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(r"C:\Users\Ali Pirzada\Documents\Projects\CourseWork\gui.ui" , self)
        self.show()
        self.loginb.clicked.connect(self.login)
        self.createuser.clicked.connect(self.newuser)


    def login(self):
        user = self.uname.text()
        passw = self.passw.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?" , (user, passw))
        result = cursor.fetchone()
        if result is not None : 
            message2 = QMessageBox()
            message2.setText("Login Successful")
            message2.exec()
        else:
            message = QMessageBox()
            message.setText("Login failed, please try again")
            message.exec()

    def newuser(self):
        new_user = self.uname.text()
        new_passw = self.passw.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)" , (new_user, new_passw))
        connection.commit()
        message = QMessageBox()
        message.setText("Registration successful")
        message.exec()












def main():
    app = QApplication([])
    window = GUI()
    app.exec_()

main()

