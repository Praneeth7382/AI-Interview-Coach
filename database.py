import sqlite3
from datetime import datetime

connection = sqlite3.connect(
    "database/interview.db"
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(

id INTEGER PRIMARY KEY AUTOINCREMENT,
role TEXT,
difficulty TEXT,
score INTEGER,
date TEXT
)

""")

connection.commit()


def save_history(role,difficulty,score):

    date=str(datetime.now())

    cursor.execute(
        """
        INSERT INTO history
        (role,difficulty,score,date)

        VALUES (?,?,?,?)

        """,

        (
            role,
            difficulty,
            score,
            date
        )
    )

    connection.commit()


def get_history():

    cursor.execute(
        "SELECT * FROM history"
    )

    return cursor.fetchall()