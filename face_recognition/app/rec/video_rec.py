import cv2
from cv2.gapi import video
import face_recognition
import numpy as np

PROCESS_THIS_FRAME = True
VERTICAL_REDUCTION = 0.25
HORIZONTAL_REDUCTION = 0.25
UNKNOWN_NAME = "Desconhecido"


def face_rec(video_capture):
    known_face_encodings = load_face_encodings()

    known_face_names = load_face_names()


def load_face_encodings():
    me_image = face_recognition.load_image_file("../../images/me.jpg")
    carlinhos_image = face_recognition.load_image_file("../../images/carlinhos.png")

    known_face_encodings = [
        face_recognition.face_encodings(me_image),
        face_recognition.face_encodings(carlinhos_image),
    ]
    return known_face_encodings


def load_face_names():
    return ["Beckman", "Carlinhos"]


def check_frame(video_capture):
    ret, frame = video_capture.read()
    return frame if ret else None


def recognize_faces(frame, known_face_encodings, know_face_names):
    adapted_frame = adapt_frame(frame)
    face_locations = face_recognition.face_locations(adapted_frame)
    face_encodings = face_recognition.face_encodings(adapted_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        face_names.append(
            get_match_name(known_face_encodings, know_face_names, face_encoding)
        )


def adapt_frame(frame):
    small_frame = cv2.resize(
        frame, (0, 0), fx=VERTICAL_REDUCTION, fy=HORIZONTAL_REDUCTION
    )
    rgb_small_frame = (small_frame, cv2.COLOR_BGR2RGB)
    return rgb_small_frame


def get_match_name(known_face_encodings, known_face_names, face_encoding):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = UNKNOWN_NAME

    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)

    best_match_index = np.argmin(face_distances)

    if matches[best_match_index]:
        name = known_face_names[best_match_index]
    return name
