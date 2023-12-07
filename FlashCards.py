import PyQt5 as py
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *

import sys
import sqlite3
import hashlib
from datetime import datetime, timedelta

# Attempt to create the database using the 'create_database' function from the 'DB' module
try:
    from DB import create_database
    create_database()
except:
    pass

# Global variable to store the set name
global set_name
set_name = "None"

# Login page class
class loginpage(QMainWindow):

    def __init__(self):
        super().__init__()
        # Load the UI from the file 'login_page.ui'
        uic.loadUi(r".\login_page.ui", self)
        self.show()

        # Connect signals to slots
        self.loginb.clicked.connect(self.login)
        self.createuser.clicked.connect(self.newuser)
        self.continueb.clicked.connect(self.connect)

        self.userid = 0
        self.__loggedIn = False

    def connect(self):
        if self.__loggedIn == True:
            # Quit the application instance if logged in
            QApplication.instance().quit()
            # Import 'setpage' from 'set_page' module
            from set_page import setpage
        else:
            # Display a message if not logged in
            message = QMessageBox()
            message.setText("You need to log in first")
            message.exec()

    def login(self):
        user = self.uname.text()
        passw = self.passw.text()
        pass_hash = hash_password(passw)

        if not user or not passw:
            # Display a message if username or password is empty
            message = QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()
        else:
            # Validate user credentials from the database
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (user, pass_hash))
            result = cursor.fetchone()

            if result is not None:
                self.__loggedIn = True

                # Retrieve user ID
                cursor.execute("SELECT user_id FROM Users WHERE username = ?", (user,))
                self.userid = cursor.fetchone()[0]

                global userid
                userid = self.userid

                # Display login successful message
                message2 = QMessageBox()
                message2.setText("Login Successful")
                message2.exec()

                # Create and display 'setpage'
                sets = setpage(userid)
                widget.addWidget(sets)
                widget.setCurrentIndex(1)
                userid = self.userid
                return userid
            else:
                # Display login failed message
                message = QMessageBox()
                message.setText("Login failed, please try again")
                message.exec()

    def newuser(self):
        new_user = self.uname.text()
        new_passw = self.passw.text()
        userInputValid = self.newUserValidation(new_user, new_passw)

        if not userInputValid:
            # Display a message if username or password is invalid
            message = QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()
        else:
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Users WHERE username = ?", (new_user,))
            existing_user = cursor.fetchone()

            if existing_user is not None:
                # Display a message if the username already exists
                message = QMessageBox()
                message.setText("Username already exists, please enter another")
                message.exec()
            else:
                pass_hash = hash_password(new_passw)
                new_passw = ""
                cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (new_user, pass_hash))
                connection.commit()
                # Display a message for successful registration
                message = QMessageBox()
                message.setText("Registration successful")
                message.exec()

    def newUserValidation(self, username, password):
        valid = True
        if len(username) > 10 or len(username) < 3:
            # Validate username length
            valid = False
        if len(password) < 4:
            # Validate password length
            valid = False
        return valid

# Function to hash the password using SHA-256 algorithm
def hash_password(password):
    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pass_hash

# Class representing the set page
class setpage(QMainWindow):
    def __init__(self, userid):
        super().__init__()
        # Load the UI from the file 'set_page.ui'
        uic.loadUi(r".\set_page.ui", self)
        self.show()
        self.userid = userid
        self.load_sets(userid)

        # Connect signals to slots
        self.createb.clicked.connect(self.create_set)
        self.display_sets.setColumnWidth(0, 250)
        self.display_sets.setHorizontalHeaderLabels(["Set Name"])
        self.nextb.clicked.connect(self.next_page)
        self.display_sets.itemClicked.connect(self.on_item_clicked)

        self.get_setname.clicked.connect(self.get_set)
        self.createcardb.clicked.connect(self.flashcardcreation)
        self.setid = 0

    def load_sets(self, userid):
        # Load sets for the given user from the database
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        query = "SELECT set_name FROM Sets WHERE user_id = ?"
        cursor.fetchall()

        # Set up the table for displaying sets
        self.display_sets.setRowCount(50)
        tablerow = 0

        # Populate the table with sets
        for row in cursor.execute(query, (userid,)):
            self.display_sets.insertRow(tablerow)
            self.display_sets.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            tablerow += 1

        cursor.close()
        connection.close()

    def create_set(self):
        # Create a new set and add it to the database
        set_name = self.newset.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Sets (set_name, user_id) VALUES (?, ?)", (set_name, userid))
        connection.commit()
        cursor.close()
        connection.close()

    def next_page(self):
        # Switch to the next page (flashcards)
        flashcards_instance = flashcards()
        flashcards_instance.show()
        widget.addWidget(flashcards_instance)
        widget.setCurrentIndex(4)

    def on_item_clicked(self, item):
        # Handle the event when a set item is clicked
        global set_name
        row = item.row()
        col = item.column()
        self.selectedset = item.text()
        set_name = item.text()

        # Retrieve set ID based on the set name
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        setid = cursor.execute(
            "SELECT set_id FROM Sets WHERE set_name = ? ", (set_name,))
        setid = cursor.fetchall()
        setid = setid[0]

        # Retrieve flashcards related to the selected set
        result = cursor.execute(
            "SELECT front_text , back_text , diff_level FROM Flashcards WHERE set_id = ? ", (setid))
        selectedset = self.selectedset
        flashcards_instance = flashcards_page(selectedset)
        widget.setCurrentIndex(3)

        cursor.close()
        connection.close()

    def flashcardcreation(self):
        # Create a new flashcard and add it to the database
        question = self.newquestion.text()
        answer = self.newanswer.text()
        diff = self.difflevel.text()

        if not question or not answer:
            # Display a message if details are not provided
            message = QMessageBox()
            message.setText("Please enter details")
            message.exec()
        else:
            # Retrieve the actual set ID and add the flashcard
            actual = self.set_id[0]
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO Flashcards (front_text, back_text, set_id, diff_level) VALUES (? , ? , ?, ?)",
                           (question, answer, actual, diff))

            # Display success message
            message = QMessageBox()
            message.setText("Success")
            message.exec()

            # Clear input fields
            self.newquestion.clear()
            self.newanswer.clear()
            self.difflevel.clear()

            connection.commit()
            connection.close()

    def get_set(self):
        # Retrieve the set ID based on the provided set name
        set_name = self.set.text()
        self.set_id = 0

        if not set_name:
            # Display a message if details are not provided
            message = QMessageBox()
            message.setText("Please enter details")
            message.exec()
        else:
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT set_id FROM Sets WHERE set_name = ?", (set_name,))
            result = cursor.fetchone()
            self.set_id = result
            # Display success message
            message = QMessageBox()
            message.setText("Success")
            message.exec()
            connection.commit()
            connection.close()

# Class representing the flashcards page
class flashcards(QMainWindow):

    def __init__(self):
        super().__init__()
        self.show()

# Class representing the flashcards page with more functionalities
class flashcards_page(QMainWindow):
    def __init__(self, set_name):
        super().__init__()
        # Load the UI from the file 'flashcard_page.ui'
        uic.loadUi(r".\flashcard_page.ui", self)

        # Connect signals to slots
        self.question.mousePressEvent = self.questionclicked
        self.answer.mousePressEvent = self.answerclicked
        self.nextcardb.clicked.connect(self.nextcard)
        self.previouscardb.clicked.connect(self.previouscard)

        self.question.setAlignment(Qt.AlignCenter)
        self.answer.setAlignment(Qt.AlignCenter)
        self.title.setAlignment(Qt.AlignCenter)

        self.question.setText("Press next button to start")
        self.answer.setText("Press next button to start")
        self.difflevel.setText("NA")
        self.count = 0

        self.correct.clicked.connect(self.correct_ans)
        self.incorrect.clicked.connect(self.incorrect_ans)

        self.start_time = None
        self.start.clicked.connect(self.spacedAlgo)

        self.flist = []
        self.blist = []
        self.difflist = []

        self.editb.clicked.connect(self.edit)

    def questionclicked(self, event):
        # Handle the event when the question is clicked
        self.answer.raise_()
        self.difflevel.raise_()

    def answerclicked(self, event):
        # Handle the event when the answer is clicked
        self.question.raise_()

    def nextcard(self):
        # Display the next flashcard in the set
        self.title.setText(set_name)

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        set_id = 0
        cursor.execute(
            "SELECT set_id FROM Sets WHERE set_name = ?", (set_name,))
        set_id = cursor.fetchone()

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT front_text FROM Flashcards WHERE set_id = ?", (set_id))
        front = cursor.fetchall()
        self.flist = []

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT back_text FROM Flashcards WHERE set_id = ?", (set_id))
        back = cursor.fetchall()
        self.blist = []

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute(
            "SELECT diff_level FROM Flashcards WHERE set_id = ?", (set_id))
        diff = cursor.fetchall()
        self.difflist = []

        # Function to sort flashcards based on difficulty level
        def sort_flashcards(front, back, diff):
            difforder = list(zip(front, back, diff))
            sorted_flashcards = sorted(difforder, key=lambda x: int(x[2]))
            return zip(*sorted_flashcards)

        for i in range(len(back)):
            self.blist.append(" ".join(map(str, back[i])))
            self.flist.append(" ".join(map(str, front[i])))
            self.difflist.append(" ".join(map(str, diff[i])))

        self.flist, self.blist, self.difflist = sort_flashcards(self.flist, self.blist, self.difflist)

        if self.count < len(self.flist):
            self.question.setText(str(self.flist[self.count]))
            self.answer.setText(str(self.blist[self.count]))
            self.difflevel.setText(str(self.difflist[self.count]))
            self.count += 1
        else:
            # Display a message when the end of the set is reached
            message = QMessageBox()
            message.setText("End of set")
            message.exec()


    def spacedAlgo(self):
        # Function to implement spaced repetition algorithm for flashcards

        # Check if the algorithm is started for the first time
        if self.start_time == None:
            self.start_time = datetime.now()
            return

        # Calculate the time spent on the current flashcard
        time_spent = datetime.now() - self.start_time
        seconds_spent = time_spent.total_seconds()

        # Adjust difficulty based on time spent
        if seconds_spent < 5:
            current_difficulty = int(self.difflist[self.count - 1])
            new_difficulty = max(1, current_difficulty - 1)
        elif seconds_spent < 10:
            new_difficulty = int(self.difflist[self.count - 1])
        else:
            current_difficulty = int(self.difflist[self.count - 1])
            new_difficulty = min(5, current_difficulty + 2)

        # Update UI with the new difficulty level
        self.difflevel.setText(str(new_difficulty))

        # Print debugging information
        print("New Diff", new_difficulty)
        print("Time =", seconds_spent)

        # Retrieve set and flashcard information from the database
        title = self.title.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT set_id FROM Sets WHERE set_name = ?", (title,))
        setid = cursor.fetchone()
        setid = setid[0]

        cursor.execute("SELECT flashcard_id FROM Flashcards WHERE front_text = ?", (
            self.flist[(self.count - 1)],))
        fid = cursor.fetchone()
        fid = fid[0]

        # Update the difficulty level in the database
        cursor.execute("UPDATE Flashcards SET diff_level = ? WHERE set_id = ? AND flashcard_id = ?",
                       (new_difficulty, setid, fid))
        connection.commit()
        connection.close()

        # Reset the timer for the next flashcard
        self.start_time = None

    def correct_ans(self):
        # Function to handle correct answer button click

        # Decrease difficulty level
        current_difficulty = int(self.difflist[self.count - 1])
        new_difficulty = max(1, current_difficulty - 1)

        # Update UI with the new difficulty level
        self.difflevel.setText(str(new_difficulty))

        # Retrieve set and flashcard information from the database
        title = self.title.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT set_id FROM Sets WHERE set_name = ?", (title,))
        setid = cursor.fetchone()
        setid = setid[0]

        cursor.execute("SELECT flashcard_id FROM Flashcards WHERE front_text = ?", (
            self.flist[(self.count - 1)],))
        fid = cursor.fetchone()
        fid = fid[0]

        # Update the difficulty level in the database
        cursor.execute("UPDATE Flashcards SET diff_level = ? WHERE set_id = ? AND flashcard_id = ?",
                       (new_difficulty, setid, fid))
        connection.commit()
        connection.close()

    def incorrect_ans(self):
        # Function to handle incorrect answer button click

        # Decrease difficulty level
        current_difficulty = int(self.difflist[self.count - 1])
        new_difficulty = max(1, current_difficulty - 1)

        # Update UI with the new difficulty level
        self.difflevel.setText(str(new_difficulty))

        # Retrieve set and flashcard information from the database
        title = self.title.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT set_id FROM Sets WHERE set_name = ?", (title,))
        setid = cursor.fetchone()
        setid = setid[0]

        cursor.execute("SELECT flashcard_id FROM Flashcards WHERE front_text = ?", (
            self.flist[(self.count - 1)],))
        fid = cursor.fetchone()
        fid = fid[0]

        # Update the difficulty level in the database
        cursor.execute("UPDATE Flashcards SET diff_level = ? WHERE set_id = ? AND flashcard_id = ?",
                       (new_difficulty, setid, fid))
        connection.commit()
        connection.close()

    def previouscard(self):
        # Function to handle going to the previous flashcard

        if self.count > 0:
            # Decrement the count and update the UI with the previous flashcard details
            self.count -= 1
            self.question.setText(str(self.flist[self.count]))
            self.answer.setText(str(self.blist[self.count]))
            self.difflevel.setText(str(self.difflist[self.count]))

        else:
            # Display a message if at the beginning of the flashcard set
            message = QMessageBox()
            message.setText("Beginning of set")
            message.exec()

    def edit(self):
        # Function to handle editing flashcard details


        # Retrieve set and flashcard information from the database
        title = self.title.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT set_id FROM Sets WHERE set_name = ?", (title,))
        result = cursor.fetchone()
        result = result[0]


        cursor.execute("SELECT flashcard_id FROM Flashcards WHERE front_text = ?", (
            self.flist[(self.count - 1)],))
        fid = cursor.fetchone()
        fid = fid[0]


        # Retrieve new flashcard details from the UI
        newquestion = self.question.text()
        newanswer = self.answer.text()
        newdiff = self.difflevel.text()


        # Update flashcard details in the database
        cursor.execute("UPDATE Flashcards SET front_text=?, back_text=?, diff_level=? WHERE set_id=? AND flashcard_id = ?",
                       (newquestion, newanswer, newdiff, result, fid))
        connection.commit()
        connection.close()


# The code below is used to create and run the application
app = QApplication(sys.argv)
widget = QStackedWidget()
login = loginpage()
userid = login.userid
sets = setpage(userid)
cards = flashcards()
testing = flashcards_page(set_name)

widget.addWidget(login)
widget.addWidget(sets)
widget.addWidget(cards)
widget.setCurrentWidget(login)
widget.addWidget(testing)

widget.setFixedSize(800, 600)
widget.show()

sys.exit(app.exec_())
