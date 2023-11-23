import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import hashlib

try:
    from DB import create_database
    create_database() 
except:
    pass 


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
        pass_hash = hash_password(passw)
        if not user or not passw:
            message=QMessageBox()
            message.setText("Username and password are required")
            message.exec()
        else:    
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?" , (user, pass_hash))
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
        pass_hash = hash_password(new_passw)
        if not new_user or not new_passw:
            message=QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()
        else:
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ?" , (new_user,))        
            existing_user = cursor.fetchone()
            if existing_user is not None :
                message=QMessageBox()
                message.setText("Username already exists please enter another")        
                message.exec()
            else:
                connection = sqlite3.connect("Flashcard_Project.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)" , (new_user, pass_hash))
                connection.commit()
                message = QMessageBox()
                message.setText("Registration successful")
                message.exec()

def hash_password(password):
    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pass_hash


def main():
    app = QApplication([])
    window = GUI()
    app.exec_()

main()




# connection = sqlite3.connect("Flashcard_Project.db")
# cursor = connection.cursor()
# cursor.execute("DELETE FROM Users")
# connection.commit()
# connection.close()
