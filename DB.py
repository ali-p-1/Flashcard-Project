from PyQt5 import QtSql
import sqlite3

def db_creation():
    db_path=("./Flashcard_Project.db")
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

db_creation()
