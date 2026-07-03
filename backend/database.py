import sqlite3

# Create Database
def create_database():

    conn = sqlite3.connect("dashboard.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS upload_history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        total_rows INTEGER,

        total_columns INTEGER

    )
    """)

    conn.commit()

    conn.close()


# Save Upload History
def save_history(filename, rows, columns):

    conn = sqlite3.connect("dashboard.db")

    cursor = conn.cursor()

    cursor.execute(

        "INSERT INTO upload_history(filename,total_rows,total_columns) VALUES(?,?,?)",

        (filename, rows, columns)

    )

    conn.commit()

    conn.close()


# Read History
def get_history():

    conn = sqlite3.connect("dashboard.db")

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM upload_history")

    data = cursor.fetchall()

    conn.close()

    return data