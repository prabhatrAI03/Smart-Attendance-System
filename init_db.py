import sqlite3
import os

# make sure data folder exists
os.makedirs("data", exist_ok=True)

# path of database file
db_path = os.path.join("data", "attendance.db")

# connect to SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# create students table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE,
    name TEXT NOT NULL,
    folder_name TEXT NOT NULL
)
""")

# create attendance table
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    time TEXT,
    status TEXT DEFAULT 'Present',
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# save changes and close
conn.commit()
conn.close()

print("attendance.db created and tables are ready.")