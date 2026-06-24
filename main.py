import cv2
import os
import pickle
import numpy as np
import face_recognition

from mark_attendance import mark_attendance

# -----------------------------
# paths
# -----------------------------
embeddings_path = os.path.join("data", "embeddings.pkl")

# -----------------------------
# load saved embeddings
# -----------------------------
with open(embeddings_path, "rb") as f:
    all_embeddings = pickle.load(f)

# recognition threshold
threshold = 0.50

# to avoid repeatedly marking same student in one run
marked_students_in_session = set()

# -----------------------------
# start webcam
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Could not open webcam.")
    exit()

print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
        break

    # convert BGR (OpenCV) to RGB (face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect face locations
    face_locations = face_recognition.face_locations(rgb_frame)

    # get embeddings for all detected faces
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # process each detected face
    for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):

        best_match = None
        best_distance = float("inf")

        # compare against all stored embeddings
        for student_id, student_data in all_embeddings.items():
            for emb in student_data["embeddings"]:
                distance = np.linalg.norm(face_encoding - emb)

                if distance < best_distance:
                    best_distance = distance
                    best_match = {
                        "student_id": student_id,
                        "roll_no": student_data["roll_no"],
                        "name": student_data["name"]
                    }

        # decide if known or unknown
        if best_match is not None and best_distance < threshold:
            student_id = best_match["student_id"]
            roll_no = best_match["roll_no"]
            name = best_match["name"]

            label = f"{name} ({roll_no})"

            # mark attendance only once per session
            if student_id not in marked_students_in_session:
                mark_attendance(student_id)
                marked_students_in_session.add(student_id)

        else:
            label = "Unknown"

        # draw rectangle around face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # draw label
        cv2.putText(
            frame,
            label,
            (left, top - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    # show webcam frame
    cv2.imshow("Smart Attendance System", frame)

    # press q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# release resources
cap.release()
cv2.destroyAllWindows()