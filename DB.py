from PyQt5 import QtSql
import sqlite3
db_path=("C:/Users/Ali Pirzada/Documents/Projects/CourseWork/Flashcard_Project.db")

def db_creation():
    global db_path
    admin = "admin"
    adminpass = "pass"
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        Username TEXT NOT NULL UNIQUE,  -- Add UNIQUE constraint ,
        Password TEXT NOT NULL
    )
    """
    cursor.execute(create_table_query)
    cursor.execute("INSERT OR IGNORE INTO users (Username, Password) VALUES (?, ?)" , (admin, adminpass))
    connection.commit()
    cursor.close()
    connection.close()

def folder_table():
    global db_path
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_folders_table_query = """
    CREATE TABLE IF NOT EXISTS Folders (
        FolderID INTEGER PRIMARY KEY,
        user_id INTEGER,
        fname TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """
    cursor.execute(create_folders_table_query)
    connection.commit()
    cursor.close()
    connection.close()


def sets_table():
    global db_path
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_sets_table_query = """
    CREATE TABLE IF NOT EXISTS Sets (
        SetID INTEGER PRIMARY KEY,
        FolderID INTEGER,
        set_name TEXT,
        FOREIGN KEY (FolderID) REFERENCES Folders(FolderID) 
    )
    """
    cursor.execute(create_sets_table_query)
    connection.commit()
    cursor.close()
    connection.close()

def flashcard():
    global db_path
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    create_flashcards_table_query = """
    CREATE TABLE IF NOT EXISTS Flashcards (
        flashcard_ID INTEGER PRIMARY KEY,
        set_id INTEGER,
        front_text TEXT,
        back_text TEXT,
        FOREIGN KEY(set_id) REFERENCES Sets(SetID)
        )
        """
    cursor.execute(create_flashcards_table_query)
    connection.commit()
    cursor.close()
    connection.close()


db_creation()
folder_table()
sets_table()
flashcard()