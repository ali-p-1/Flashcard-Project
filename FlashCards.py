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


class loginpage(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi(r".\login_page.ui", self)
        self.show()

        self.loginb.clicked.connect(self.login)
        self.createuser.clicked.connect(self.newuser)
        self.continueb.clicked.connect(self.connect)

        self.userid = 0
        self.__loggedIn = False


    def connect(self):
        if self.__loggedIn == True:
            QApplication.instance().quit()
            from set_page import setpage
        else:
            message = QMessageBox()
            message.setText("You need to log in first")
            message.exec()


    def login(self):
        user = self.uname.text()
        passw = self.passw.text()
        pass_hash = hash_password(passw)

        if not user or not passw:
            message = QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()

        else:
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Users WHERE username = ? AND password = ?", (user, pass_hash))
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

                sets = setpage(userid)
                widget.addWidget(sets)
                widget.setCurrentIndex(1)
                userid = self.userid
                print(userid)
                return userid

            else:
                message = QMessageBox()
                message.setText("Login failed, please try again")
                message.exec()


    def newuser(self):
        new_user = self.uname.text()
        new_passw = self.passw.text()
        userInputValid = self.newUserValidation(new_user, new_passw)

        if not userInputValid:
            message = QMessageBox()
            message.setText("Please enter a username or password")
            message.exec()

        else:
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM Users WHERE username = ?", (new_user,))
            existing_user = cursor.fetchone()

            if existing_user is not None:
                message = QMessageBox()
                message.setText(
                    "Username already exists, please enter another")
                message.exec()

            else:
                pass_hash = hash_password(new_passw)
                new_passw = ""
                cursor.execute(
                    "INSERT INTO Users (username, password) VALUES (?, ?)", (new_user, pass_hash))
                connection.commit()
                message = QMessageBox()
                message.setText("Registration successful")
                message.exec()


    def newUserValidation(self, username, password):
        valid = True
        if len(username) > 10 or len(username) < 3:
            valid = False
        if len(password) < 6:
            valid = False
        return valid


def hash_password(password):
    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return pass_hash


class setpage(QMainWindow):
    def __init__(self, userid):
        super().__init__()
        uic.loadUi(r".\set_page.ui", self)
        self.show()
        self.userid = userid
        self.load_sets(userid)

        self.createb.clicked.connect(self.create_set)
        self.display_sets.setColumnWidth(0, 250)
        self.display_sets.setHorizontalHeaderLabels(["Set Name"])
        self.nextb.clicked.connect(self.next_page)
        self.display_sets.itemClicked.connect(self.on_item_clicked)
        

    def load_sets(self, userid):
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        query = "SELECT set_name FROM Sets WHERE user_id = ?"
        cursor.fetchall()

        self.display_sets.setRowCount(50)
        tablerow = 0

        for row in cursor.execute(query, (userid,)):
            self.display_sets.insertRow(tablerow)
            self.display_sets.setItem(
                tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
            tablerow = tablerow + 1
            print(row)

        cursor.close()
        connection.close()

    def create_set(self):
        set_name = self.newset.text()
        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Sets (set_name, user_id) VALUES (?, ?)", (set_name, userid))
        connection.commit()
        cursor.close()
        connection.close()


    def next_page(self):
        flashcards_instance = flashcards()
        flashcards_instance.show()
        widget.addWidget(flashcards_instance)
        widget.setCurrentIndex(2)


    def on_item_clicked(self, item):
        row = item.row()
        col = item.column()
        self.selectedset_name = item.text()
        set_name = item.text()
        self.set_name = set_name
        print(set_name)

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        setid = cursor.execute("SELECT set_id FROM Sets WHERE set_name = ? ", (set_name,))
        setid = cursor.fetchall()
        setid = setid[0]

        result = cursor.execute("SELECT front_text , back_text , diff_level FROM Flashcards WHERE set_id = ? ", (setid))
        print(cursor.fetchall())
        # testing = flashcards_page(self.set_name)
        widget.setCurrentIndex(3)

        cursor.close()
        connection.close()



class flashcards(QMainWindow):

    def __init__(self):
        super().__init__()
        self.show()




# class flashcards_page(QMainWindow):

#     def __init__(self, set_name):
#         super().__init__()
#         uic.loadUi(r".\flashcard_page.ui", self)

#         self.title.setText(set_name)
#         self.pushbutton.clicked.connect(card_clicked)

#     def card_clicked(self):
#         print("ok")


















app = QApplication(sys.argv)
widget = QStackedWidget()
login = loginpage()
userid = login.userid

sets = setpage(userid)

# abc = setpage.set_name
# cards = flashcards()
# testing = flashcards_page(sets.set_name)


widget.addWidget(login)
widget.addWidget(sets)
# widget.addWidget(cards)
widget.setCurrentWidget(login)
# widget.addWidget(testing)

widget.setFixedSize(800, 600)
widget.show()


sys.exit(app.exec_())


# connection = sqlite3.connect("Flashcard_Project.db")
# cursor = connection.cursor()
# cursor.execute("INSERT INTO Flashcards (front_text, back_text, diff_level, flashcard_id, set_id) VALUES ('test', 'test 2', 1, 1, 2);")
# connection.commit()
