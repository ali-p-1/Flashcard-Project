import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import hashlib

try:
    # Try to import the create_database function from DB module
    from DB import create_database
    create_database() 
except:
    # If there is a database already created, ignore it and continue
    pass 

class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the user interface from the specified file
        uic.loadUi(r"C:\Users\Ali Pirzada\Documents\Projects\CourseWork\gui.ui" , self)
        self.show()
        # Connect buttons to their respective functions
        self.loginb.clicked.connect(self.login)
        self.createuser.clicked.connect(self.newuser)

    def login(self):
        # Get the username and password from the input fields
        user = self.uname.text()
        passw = self.passw.text()
        # Hash the password
        pass_hash = hash_password(passw)
        if not user or not passw:
            # Display an error message if either the username or password is empty
            message=QMessageBox()
            message.setText("Username and password are required")
            message.exec()
        else:    
            # Connect to the database
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            # Execute a SELECT query to check if the user exists with the provided username and hashed password
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?" , (user, pass_hash))
            result = cursor.fetchone()
            if result is not None : 
                # Display a success message if login is successful
                message2 = QMessageBox()
                message2.setText("Login Successful")
                message2.exec()
            else:
                # Display an error message if login fails
                message = QMessageBox()
                message.setText("Login failed, please try again")
                message.exec()

    def newuser(self):
        # Get the new username and password from the input fields
        new_user = self.uname.text()
        new_passw = self.passw.text()  
        # Hash the password
        pass_hash = hash_password(new_passw)
        if not new_user or not new_passw:
            # Display an error message if either the new username or password is empty
            message=QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()
        else:
            # Connect to the database
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            # Execute a SELECT query to check if the new username already exists
            cursor.execute("SELECT * FROM Users WHERE username = ?" , (new_user,))        
            existing_user = cursor.fetchone()
            
            if existing_user is not None :
                # Display an error message if the new username already exists
                message=QMessageBox()
                message.setText("Username already exists, please enter another")        
                message.exec()
            else:
                # Insert the new user into the database
                cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)" , (new_user, pass_hash))
                connection.commit()
                # Display a success message for registration
                message = QMessageBox()
                message.setText("Registration successful")
                message.exec()

# Function to hash a password using SHA-256
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
