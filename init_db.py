import sqlite3
import os

# make sure data folder exists
os.makedirs("data", exist_ok=True)

# database path
db_path = os.path.join("data", "attendance.db")

# connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# -------------------------
# 1. Create students table
# -------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll_no TEXT UNIQUE,
    name TEXT NOT NULL,
    folder_name TEXT NOT NULL
)
""")

# ---------------------------
# 2. Create attendance table
# ---------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    roll_no TEXT,
    name TEXT,
    date TEXT,
    time TEXT,
    status TEXT DEFAULT 'Present',
    FOREIGN KEY(student_id) REFERENCES students(id)
)
""")

# save changes
conn.commit()
conn.close()

print("Database and tables are ready.")