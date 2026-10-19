import sqlite3

DB_NAME = "game_database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nick TEXT NOT NULL,
            Status BOOLEAN NOT NULL,
            TimeOfGame INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def addUser(nick, status, timeGame):
    init_db()

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO Users (Nick, Status, TimeOfGame) VALUES (?, ?, ?)", (nick, status, timeGame))
    conn.commit()
    conn.close()