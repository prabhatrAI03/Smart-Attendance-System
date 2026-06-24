

import os
import sqlite3

# paths
dataset_path = os.path.join("data", "attendance_dataset")
db_path = os.path.join("data", "attendance.db")

# connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# -----------------------------
# 1. delete old student records
# -----------------------------
cursor.execute("DELETE FROM students")

# optional: reset auto-increment id counter
cursor.execute("DELETE FROM sqlite_sequence WHERE name='students'")

# -----------------------------
# 2. read all student folders
# -----------------------------
student_folders = [
    folder for folder in os.listdir(dataset_path)
    if os.path.isdir(os.path.join(dataset_path, folder))
]

# sort folders so roll numbers are assigned in order
student_folders.sort()

# -----------------------------
# 3. insert students one by one
# -----------------------------
for i, folder_name in enumerate(student_folders, start=1):
    roll_no = f"STU{i:03d}"   # STU001, STU002, STU003 ...

    # convert folder name to readable name
    # Adrien_Brody -> Adrien Brody
    name = folder_name.replace("_", " ")

    cursor.execute("""
        INSERT INTO students (roll_no, name, folder_name)
        VALUES (?, ?, ?)
    """, (roll_no, name, folder_name))

    print(f"Inserted -> {roll_no} | {name} | {folder_name}")

# save changes
conn.commit()
conn.close()

print("\nAll students inserted successfully.")