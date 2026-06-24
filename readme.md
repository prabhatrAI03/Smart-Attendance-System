# Smart Attendance System

A **face-recognition based Smart Attendance System** built with **Python, SQLite, OpenCV, and face embeddings**.
The system registers students from a dataset, generates face embeddings for each student, identifies students from an image or webcam feed, and automatically marks attendance in a database.

---

## Overview

Traditional attendance systems are manual, time-consuming, and prone to proxy attendance. This project automates the process using **face recognition**.

The system works in two stages:

1. **Student Registration**

   * Student image folders are read from a dataset
   * Student details are inserted into an SQLite database
   * Face embeddings are extracted and stored for recognition

2. **Attendance Marking**

   * A test image or webcam frame is processed
   * Face embeddings are generated for the detected face
   * The face is matched against stored student embeddings
   * If a match is found, attendance is marked automatically

---

# Features

* **Student registration from image folders**
* **SQLite database integration**
* **Face embedding extraction using `face_recognition`**
* **Student recognition through embedding comparison**
* **Automatic attendance marking with date and time**
* **Duplicate attendance prevention for the same day**
* **Structured project pipeline for registration → recognition → attendance**

---

# Tech Stack

* **Python**
* **SQLite**
* **OpenCV**
* **face_recognition**
* **NumPy**
* **Pickle**

---

# Project Structure

```bash
Smart Attendance System/
│
├── data/
│   ├── attendance_dataset/      # Student image folders
│   ├── attendance.db            # SQLite database
│   └── embeddings.pkl           # Saved face embeddings
│
├── init_db.py                   # Creates students and attendance tables
├── insert_students.py           # Inserts students into the database
├── extract_embeddings.py        # Extracts and stores face embeddings
├── test_recognition.py          # Tests recognition on a single image
├── mark_attendance.py           # Inserts attendance into the DB
├── main.py                      # Main attendance pipeline
├── README.md
└── .gitignore
```

---

# How It Works

## 1. Prepare the dataset

Store student images inside `data/attendance_dataset/`.

### Example structure

```bash
data/attendance_dataset/
├── Abdullah_Gul/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
├── Adrien_Brody/
│   ├── img1.jpg
│   ├── img2.jpg
│   └── ...
```

Each folder corresponds to one student.

---

## 2. Create the database

Run:

```bash
python init_db.py
```

This creates:

* `students` table
* `attendance` table

---

## 3. Insert students into the database

Run:

```bash
python insert_students.py
```

This script reads all student folders from `attendance_dataset` and inserts them into the `students` table with generated roll numbers.

---

## 4. Extract face embeddings

Run:

```bash
python extract_embeddings.py
```

This script:

* reads student images
* generates face embeddings for each student
* stores them in:

```bash
data/embeddings.pkl
```

---

## 5. Test recognition on a single image

Run:

```bash
python test_recognition.py
```

This verifies whether the system can correctly identify a student from a test image by comparing embeddings.

---

## 6. Mark attendance

Run:

```bash
python mark_attendance.py
```

This inserts attendance into the database for a recognized student.

---

## 7. Run the main attendance pipeline

Run:

```bash
python main.py
```

The pipeline performs:

1. Load stored student embeddings
2. Read an image or webcam frame
3. Detect and encode the face
4. Compare with stored embeddings
5. Identify the student
6. Mark attendance in the database

---

# Database Schema

## Students Table

| Column      | Type    | Description                |
| ----------- | ------- | -------------------------- |
| id          | INTEGER | Primary key                |
| roll_no     | TEXT    | Unique student roll number |
| name        | TEXT    | Student name               |
| folder_name | TEXT    | Dataset folder name        |

---

## Attendance Table

| Column     | Type    | Description                            |
| ---------- | ------- | -------------------------------------- |
| id         | INTEGER | Primary key                            |
| student_id | INTEGER | Foreign key referencing students table |
| roll_no    | TEXT    | Student roll number                    |
| name       | TEXT    | Student name                           |
| date       | TEXT    | Attendance date                        |
| time       | TEXT    | Attendance time                        |
| status     | TEXT    | Attendance status                      |

---

# Example Attendance Record

```python
(3, 1, 'STU001', 'Abdullah Gul', '2026-06-24', '16:33:51', 'Present')
```

This means:

* **Student ID:** 1
* **Roll No:** STU001
* **Name:** Abdullah Gul
* **Date:** 2026-06-24
* **Time:** 16:33:51
* **Status:** Present

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/Smart-Attendance-System.git
cd Smart-Attendance-System
```

## 2. Create and activate a virtual environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```


```bash
pip install opencv-python face_recognition numpy
```

---

# Usage Order

Run the project files in this order:

```bash
python init_db.py
python insert_students.py
python extract_embeddings.py
python test_recognition.py
python mark_attendance.py
python main.py
```

---



# Future Improvements

* Real-time webcam attendance dashboard
* Attendance export to CSV / Excel
* Unknown face logging
* Multi-face attendance in a single frame
* Anti-spoofing / liveness detection
* Web deployment using Flask or FastAPI
* Admin interface for attendance records

---



# Author

**Prabhat Rai**

If you found this project useful, feel free to fork it or build on top of it.
