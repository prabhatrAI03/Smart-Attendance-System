import sqlite3
import os
from datetime import datetime

db_path = os.path.join("data", "attendance.db")

def mark_attendance(student_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # current date and time
    today_date = datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H:%M:%S")

    # -----------------------------------------
    # 1. get roll_no and name from students table
    # -----------------------------------------
    cursor.execute("""
        SELECT roll_no, name
        FROM students
        WHERE id = ?
    """, (student_id,))
    
    student = cursor.fetchone()

    if student is None:
        print(f"No student found with student_id {student_id}")
        conn.close()
        return

    roll_no, name = student

    # -----------------------------------------
    # 2. check if attendance already marked today
    # -----------------------------------------
    cursor.execute("""
        SELECT * FROM attendance
        WHERE student_id = ? AND date = ?
    """, (student_id, today_date))

    existing_record = cursor.fetchone()

    if existing_record:
        print(f"Attendance already marked for {name} ({roll_no}) today.")
    else:
        # -----------------------------------------
        # 3. insert attendance with roll_no and name
        # -----------------------------------------
        cursor.execute("""
            INSERT INTO attendance (student_id, roll_no, name, date, time, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (student_id, roll_no, name, today_date, current_time, "Present"))

        conn.commit()
        print(f"Attendance marked for {name} ({roll_no}) at {current_time}")

    conn.close()


# -----------------------------
# test the function directly
# -----------------------------
if __name__ == "__main__":
    test_student_id = 1   # change if needed
    mark_attendance(test_student_id)