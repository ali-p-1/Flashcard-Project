import PyQt5 as py
import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import *




class setpage(QMainWindow):
        def __init__(self, userid):
                super().__init__()
                # Load the user interface from the specified file
                uic.loadUi(r".\set_page.ui" , self)
                self.show()
                self.load_sets(userid)
                self.createb.clicked.connect(self.create_set)
                self.setlist.itemClicked.connect(self.on_set_clicked)


        def load_sets(self, userid):
                connection = sqlite3.connect("Flashcard_Project.DB")
                cursor = connection.cursor()
                cursor.execute("SELECT set_name FROM Sets WHERE user_id = ?" , (userid,))
                result = cursor.fetchall()
                cursor.close()
                connection.close()

                self.setlist.clear()
                for result in result:
                        set = result[0]
                        item= QListWidget(set)
                        self.setlist.addItem(item)

                
        def create_set(self):
                set = self.newset.text()
                connection = sqlite3.connect("Flashcard_Project.db")
                cursor = connection.cursor()
                cursor.execute("INSERT INTO Sets (set_name ,user_id) VALUES (?, ?)", (set, ffs))
                connection.commit()
                cursor.close()
                connection.close()


        def on_set_clicked(self, item):
        # This method will be called when an item in the listWidget is clicked
                selected_set_name = item.text()
                print(f"Clicked on set: {selected_set_name}")
 


          

 



