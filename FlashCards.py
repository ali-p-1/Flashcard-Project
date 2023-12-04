import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *
import hashlib
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtCore import Qt


try:
    from DB import create_database
    create_database()
except:
    pass

global set_name
set_name = "None"

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
                userid = self.userid

                message2 = QMessageBox()
                message2.setText("Login Successful")
                message2.exec()

                sets = setpage(userid)
                widget.addWidget(sets)
                widget.setCurrentIndex(1)
                userid = self.userid
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
        if len(password) < 4:
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

        self.get_setname.clicked.connect(self.get_set)

        self.createcardb.clicked.connect(self.flashcardcreation)
        self.setid = 0









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
        widget.setCurrentIndex(4)


    def on_item_clicked(self, item):
        global set_name
        row = item.row()
        col = item.column()
        self.selectedset = item.text()
        set_name = item.text()


        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        setid = cursor.execute("SELECT set_id FROM Sets WHERE set_name = ? ", (set_name,))
        setid = cursor.fetchall()
        setid = setid[0]

        result = cursor.execute("SELECT front_text , back_text , diff_level FROM Flashcards WHERE set_id = ? ", (setid))
        selectedset = self.selectedset
        flashcards_instance = flashcards_page(selectedset) 
        widget.setCurrentIndex(3)

        cursor.close()
        connection.close()


    def flashcardcreation (self):
        question = self.newquestion.text()
        answer = self.newanswer.text()
        diff = self.difflevel.text()

        if not question or not answer:

            message = QMessageBox()
            message.setText("Please enter details")
            message.exec()

        else:

            actual = self.set_id[0]
            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute ("INSERT INTO Flashcards (front_text, back_text, set_id, diff_level) VALUES (? , ? , ?, ?)" , (question, answer, actual, diff))

            message = QMessageBox()
            message.setText("Success")
            message.exec()

            self.newquestion.clear()
            self.newanswer.clear()
            self.difflevel.clear()

            connection.commit()
            connection.close()

    def get_set (self):

        set_name = self.set.text()
        self.set_id = 0

        if not set_name:

            message = QMessageBox()
            message.setText("Please enter details")
            message.exec()

        else:

            connection = sqlite3.connect("Flashcard_Project.db")
            cursor = connection.cursor()
            cursor.execute ("SELECT set_id FROM Sets WHERE set_name = ?", (set_name,))
            result = cursor.fetchone()
            self.set_id = result
            message = QMessageBox()
            message.setText("Success")
            message.exec()
            connection.commit()
            connection.close()



class flashcards(QMainWindow):

    def __init__(self):
        super().__init__()
        self.show()




class flashcards_page(QMainWindow):
    def __init__(self, set_name): 
            super().__init__()
            uic.loadUi(r".\flashcard_page.ui", self)


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


            self.lvl1 = []
            self.lvl2 = []
            self.lvl3 = []

            self.flist = []
            self.blist = []
            self.difflist = []

            self.editb.clicked.connect(self.edit)

    def questionclicked(self, event):

        self.answer.raise_()
        self.difflevel.raise_()

    def answerclicked(self, event):

        self.question.raise_()

    def nextcard(self):  

        self.title.setText(set_name)

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        set_id = 0 
        cursor.execute ("SELECT set_id FROM Sets WHERE set_name = ?" , (set_name,))   
        set_id = cursor.fetchone()


        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute ("SELECT front_text FROM Flashcards WHERE set_id = ?" , (set_id))   
        front = cursor.fetchall()
        self.flist = []

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute ("SELECT back_text FROM Flashcards WHERE set_id = ?" , (set_id))   
        back = cursor.fetchall()
        self.blist = []

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute ("SELECT diff_level FROM Flashcards WHERE set_id = ?" , (set_id))   
        diff = cursor.fetchall()
        self.difflist = []



        def sort_flashcards(front, back, diff):
            difforder = list(zip(front, back, diff))
            sorted_flashcards = sorted(difforder, key=lambda x: int(x[2]))
            return zip(*sorted_flashcards)

            # lvl1 = []
            # lvl2 = []
            # lvl3 = []
            # newlist = []

            # connection = sqlite3.connect("Flashcard_Project.db")
            # cursor = connection.cursor()
            # cursor.execute ("SELECT front_text, back_text, diff_level FROM Flashcards WHERE set_id = ? AND diff_level = 3" , (set_id))   
            # lvl3 = cursor.fetchall()

            # connection = sqlite3.connect("Flashcard_Project.db")
            # cursor = connection.cursor()
            # cursor.execute ("SELECT front_text, back_text, diff_level FROM Flashcards WHERE set_id = ? AND diff_level = 2" , (set_id))   
            # lvl2 = cursor.fetchall()

            # connection = sqlite3.connect("Flashcard_Project.db")
            # cursor = connection.cursor()
            # cursor.execute ("SELECT front_text, back_text, diff_level FROM Flashcards WHERE set_id = ? AND diff_level = 1" , (set_id))   
            # lvl1 = cursor.fetchall()

            # connection.commit()
            # connection.close()




        for i in range (len(back)):

            self.blist.append(" ".join(map(str, back[i])))
            self.flist.append(" ".join(map(str, front[i])))
            self.difflist.append(" ".join(map(str,diff[i])))


        self.flist, self.blist, self.difflist = sort_flashcards(self.flist, self.blist, self.difflist)





        if self.count < len(self.flist):

            self.question.setText(str(self.flist[self.count]))
            self.answer.setText(str(self.blist[self.count]))
            self.difflevel.setText(str(self.difflist[self.count]))
            self.count +=1

        else:

            message = QMessageBox()
            message.setText("End of set")
            message.exec()



    def previouscard(self):

        if self.count > 0:
            self.count -= 1
            self.question.setText(str(self.flist[self.count]))
            self.answer.setText(str(self.blist[self.count]))
            self.difflevel.setText(str(self.difflist[self.count]))


        else:
            message = QMessageBox()
            message.setText("Beginning of set")
            message.exec()


    def edit(self):

        newquestion = self.flist[(self.count - 1)]
        newanswer =  self.blist[(self.count - 1)]
        newdiff =  self.difflist[(self.count - 1)]
        print(self.count - 1)

        title = self.title.text()


        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT set_id FROM Sets WHERE set_name = ?" , (title,))
        result = cursor.fetchone()
        result = result[0]

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("SELECT flashcard_id FROM Flashcards WHERE front_text = ?" , ((self.flist[(self.count - 1)]),))
        fid = cursor.fetchone()
        fid = fid[0]
        print(fid)

        newquestion = self.question.text()
        newanswer = self.answer.text()
        newdiff = self.difflevel.text()

        connection = sqlite3.connect("Flashcard_Project.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE Flashcards SET front_text=?, back_text=?, diff_level=? WHERE set_id=? AND flashcard_id = ?", (newquestion, newanswer, newdiff, result, fid)) 
        connection.commit()
        connection.close()




 #test
# add validation for diff level
# spaced repetition algorithm 

# get rid of continue button
# implement a button to switch between pages


# connection = sqlite3.connect("Flashcard_Project.db")
# cursor = connection.cursor()
# # cursor.execute("INSERT INTO Flashcards (front_text, back_text, diff_level, flashcard_id, set_id) VALUES ('7+', 'tesdtt', 2, 8, 3);")
# cursor.execute("DELETE FROM Sets")
# connection.commit()


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


