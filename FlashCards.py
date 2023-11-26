import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import hashlib

# Attempt to import the create_database function from the DB module
try:
    from DB import create_database
    create_database() 
except:
    # If there is a database already created, ignore it and continue
    pass 


# Class for the login page
class loginpage(QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the user interface from the specified file
        uic.loadUi(r".\login_page.ui", self)
        self.show()
        # Connect buttons to their respective functions
        self.loginb.clicked.connect(self.login)
        self.createuser.clicked.connect(self.newuser)
        self.continueb.clicked.connect(self.connect)
        self.userid = 0
        self.__loggedIn = False

    def connect(self):
        if self.__loggedIn == True:
            # If logged in, quit the application
            QApplication.instance().quit()
            from set_page import setpage
        else:
            # If not logged in, show a message
            message = QMessageBox()
            message.setText("You need to log in first")
            message.exec()

    def login(self):
        # Get the username and password from the input fields
        user = self.uname.text()
        passw = self.passw.text()
        # Hash the password
        pass_hash = hash_password(passw)
        if not user or not passw:
            # Display an error message if either the username or password is empty
            message = QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()
        else:    
            # Connect to the database
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            # Execute a SELECT query to check if the user exists with the provided username and hashed password
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (user, pass_hash))
            result = cursor.fetchone()
            if result is not None:
                self.__loggedIn = True
                connection = sqlite3.connect("Flashcard_Project.db")
                cursor = connection.cursor()
                cursor.execute("SELECT user_id FROM Users WHERE username = ?", (user,))
                self.userid = cursor.fetchone()[0]
                global userid
                print(self.userid)
                userid = self.userid
                message2 = QMessageBox()
                message2.setText("Login Successful")
                message2.exec()
                flashcards = setpage(userid=userid)
                widget.addWidget(flashcards)
                widget.setCurrentIndex(1)
                userid = self.userid
                print(userid)
                return userid
            else:
                # Display an error message if login fails
                message = QMessageBox()
                message.setText("Login failed, please try again")
                message.exec()

    def newuser(self):
        # Get the new username and password from the input fields
        new_user = self.uname.text()
        new_passw = self.passw.text()  
        # Validate the new username and password
        userInputValid = self.newUserValidation(new_user, new_passw)
        if not userInputValid:
            # Display an error message if either the new username or password is empty
            message = QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()
        else:
            # Connect to the database
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            # Execute a SELECT query to check if the new username already exists
            cursor.execute("SELECT * FROM Users WHERE username = ?", (new_user,))        
            existing_user = cursor.fetchone()
            if existing_user is not None:
                # Display an error message if the new username already exists
                message = QMessageBox()
                message.setText("Username already exists, please enter another")        
                message.exec()
            else:
                # Insert the new user into the database
                pass_hash = hash_password(new_passw)  # Password is hashed
                new_passw = ""  # Plaintext password is reset, so it can't be read anymore in memory
                cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (new_user, pass_hash))
                connection.commit()
                # Display a success message for registration
                message = QMessageBox()
                message.setText("Registration successful")
                message.exec()

    def newUserValidation(self, username, password):
        # Initialize the validation status as True
        valid = True
        # Check if the username length is within the acceptable range (3 to 10 characters)
        if len(username) > 10 or len(username) < 3:
            valid = False  # If not, set the validation status to False
        # Check if the password length is at least 6 characters
        if len(password) < 6:
            valid = False  # If not, set the validation status to False
        # Return the final validation status
        return valid

# Function to hash a password using SHA-256
def hash_password(password):
    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pass_hash

# Class for the set page
class setpage(QMainWindow):
    def __init__(self, userid):
        super().__init__()
        # Load the user interface from the specified file
        uic.loadUi(r".\set_page.ui", self)
        self.show()
        self.userid = userid
        self.load_sets(userid)
        self.createb.clicked.connect(self.create_set)
        self.display_sets.setColumnWidth(0,250)
        self.display_sets.setHorizontalHeaderLabels(["Set Name"])

    def load_sets(self, userid):
        # Connect to the database and load sets for the given user ID
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        query = "SELECT set_name FROM Sets WHERE user_id = ?"
        cursor.fetchall()
        self.display_sets.setRowCount(50)
        tablerow = 0
        for row in cursor.execute(query, (2,)): #fix userid thing
            self.display_sets.insertRow(tablerow)
            self.display_sets.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            tablerow = tablerow + 1
            print(row)
        cursor.close()
        connection.close()


    def create_set(self):
        # Create a new set in the database for the given user ID
        set_name = self.newset.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Sets (set_name, user_id) VALUES (?, ?)", (set_name, userid))
        connection.commit()
        cursor.close()
        connection.close()












# Create the application instance
app = QApplication(sys.argv)

# Create a stacked widget to manage different pages
widget = QStackedWidget()

# Create instances of login and set pages
login = loginpage()
userid = login.userid
flashcards = setpage(userid=userid)

# Add login and set pages to the stacked widget
widget.addWidget(login)
widget.addWidget(flashcards)

# Set the initial widget to be shown
widget.setCurrentWidget(login)
widget.setFixedSize(800, 600)  

# Show the widget and start the application event loop
widget.show()
sys.exit(app.exec_())



# connection = sqlite3.connect("Flashcard_Project.db")
# cursor = connection.cursor()
# cursor.execute("DELETE FROM Users")
# connection.commit()