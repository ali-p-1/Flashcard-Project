from PyQt5 import QtSql
import sqlite3
# Define the path to the SQLite database
db_path = "C:/Users/Ali Pirzada/Documents/Projects/CourseWork/Flashcard_Project.db"

def user_Table():
    # Connect to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # User Table
    id = 1
    admin = "admin"
    adminpass = "pass"
    create_userTable = """
        -- Create the Users table if it doesn't exist
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY ,
            username TEXT NOT NULL UNIQUE ,
            password TEXT NOT NULL 
        )
    """
    cursor.execute(create_userTable)
    
    # Insert the default admin user if it doesn't exist
    cursor.execute("INSERT OR IGNORE INTO Users (user_id, username, password) VALUES (?,?,?)", (id, admin, adminpass))

    # Commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

# def folder_table():
#     # Connect to the database
#     connection = sqlite3.connect(db_path)
#     cursor = connection.cursor()

#     # Folder Table
#     create_folderTable = """
#         -- Create the Folders table if it doesn't exist
#         CREATE TABLE IF NOT EXISTS Folders (
#             folder_name TEXT NOT NULL,
#             folder_id INTEGER PRIMARY KEY,
#             user_id INTEGER,
#             -- Reference the Users table for user_id
#             FOREIGN KEY (user_id) REFERENCES Users (user_id)
#         )
#     """
#     cursor.execute(create_folderTable)

#     # Commit changes and close the connection
#     connection.commit()
#     cursor.close()
#     connection.close()

def set_table():
    # Connect to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Set Table
    create_setTable = """
        -- Create the Sets table if it doesn't exist
        CREATE TABLE IF NOT EXISTS Sets (
            set_name TEXT NOT NULL,
            set_id INTEGER PRIMARY KEY,
            user_id INTEGER,
            -- Reference the Users table for user_ID
            FOREIGN KEY (user_ID) REFERENCES Users (user_id)
        )
    """
    cursor.execute(create_setTable)

    # Commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def flashcards_table():
    # Connect to the database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Flashcards Table
    create_flashcardTable = """
        -- Create the Flashcards table if it doesn't exist
        CREATE TABLE Flashcards (
            front_text TEXT NOT NULL,
            back_text TEXT NOT NULL,
            diff_level INTEGER,
            flashcard_id INTEGER PRIMARY KEY,
            set_id INTEGER,
            -- Reference the Sets table for set_id
            FOREIGN KEY (set_id) REFERENCES Sets (set_id)
        )
    """
    cursor.execute(create_flashcardTable)

    # Commit changes and close the connection
    connection.commit()
    cursor.close()
    connection.close()

def create_database():
    # Create all required tables
    user_Table()
    # folder_table()
    set_table()
    flashcards_table()

# Execute the database creation function
create_database()
