from PyQt5 import QtSql
import sqlite3
db_path=("C:/Users/Ali Pirzada/Documents/Projects/CourseWork/Flashcard_Project.db")

def user_Table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    id = 1
    admin = "admin"
    adminpass = "pass"
    create_userTable = """
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY ,
            username TEXT NOT NULL UNIQUE ,
            password TEXT NOT NULL 
        )
        """
    cursor.execute(create_userTable)
    cursor.execute("INSERT OR IGNORE INTO Users (user_id, username, password) VALUES (?,?,?)", (id, admin, adminpass))
    connection.commit()
    cursor.close()
    connection.close()

def folder_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_folderTable = """
    CREATE TABLE IF NOT EXISTS Folders (
        folder_name TEXT NOT NULL,
        folder_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """
    cursor.execute (create_folderTable)
    connection.commit()
    cursor.close()
    connection.close()

def set_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_setTable = """
    CREATE TABLE IF NOT EXISTS Sets (
        set_name TEXT NOT NULL,
        set_id INTEGER PRIMARY KEY,
        folder_id INTEGER,
        FOREIGN KEY (folder_id) REFERENCES Folders (folder_id)
    )
    """
    cursor.execute (create_setTable)
    connection.commit()
    cursor.close()
    connection.close()

def flashcards_table():
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_flashcardTable = """
    CREATE TABLE Flashcards (
        front_text TEXT NOT NULL,
        back_text TEXT NOT NULL,
        diff_level INTEGER,
        flashcard_id INTEGER PRIMARY KEY,
        set_id INTEGER,
        FOREIGN KEY (set_id) REFERENCES Sets (set_id)
    )
    """
    cursor.execute (create_flashcardTable)
    connection.commit()
    cursor.close()
    connection.close()


def create_database():
    user_Table()
    folder_table()
    set_table()
    flashcards_table()

create_database()

