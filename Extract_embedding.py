import os
import sqlite3
import pickle
import face_recognition

# -----------------------------
# paths
# -----------------------------
db_path = os.path.join("data", "attendance.db")
dataset_path = os.path.join("data", "Attendance_dataset")
embeddings_path = os.path.join("data", "embeddings.pkl")

valid_ext = (".jpg", ".jpeg", ".png")

# -----------------------------
# connect to database
# -----------------------------
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# get all students from DB
cursor.execute("SELECT id, roll_no, name, folder_name FROM students")
students = cursor.fetchall()

# embeddings dictionary
all_embeddings = {}

# -----------------------------
# process each student
# -----------------------------
for student in students:
    student_id, roll_no, name, folder_name = student
    student_folder = os.path.join(dataset_path, folder_name)

    if not os.path.isdir(student_folder):
        print(f"Folder not found: {student_folder}")
        continue

    student_embeddings = []

    # read all images in student folder
    for img_name in os.listdir(student_folder):
        if not img_name.lower().endswith(valid_ext):
            continue

        img_path = os.path.join(student_folder, img_name)

        try:
            # load image
            image = face_recognition.load_image_file(img_path)

            # get face encodings
            encodings = face_recognition.face_encodings(image)

            if len(encodings) == 0:
                print(f"No face found in: {img_path}")
                continue

            # take first face encoding
            student_embeddings.append(encodings[0])

            print(f"Encoded: {roll_no} | {img_name}")

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

    # save only if at least one embedding exists
    if len(student_embeddings) > 0:
        all_embeddings[student_id] = {
            "roll_no": roll_no,
            "name": name,
            "folder_name": folder_name,
            "embeddings": student_embeddings
        }
    else:
        print(f"No valid embeddings for {roll_no} - {name}")

# close DB connection
conn.close()

# -----------------------------
# save embeddings to file
# -----------------------------
with open(embeddings_path, "wb") as f:
    pickle.dump(all_embeddings, f)

print("\nEmbeddings saved successfully to data/embeddings.pkl")