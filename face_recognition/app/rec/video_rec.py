import base64
import cv2
import face_recognition
import numpy as np
from app.database import carregar_usuarios, salvar_auditoria

VERTICAL_REDUCTION = 0.25
HORIZONTAL_REDUCTION = 0.25
UNKNOWN_NAME = "Desconhecido"

def load_face_encodings():
    encodings, nomes = carregar_usuarios()
    return encodings, nomes

def check_frame(video_capture):
    ret, frame = video_capture.read()
    return frame if ret else None

def recognize_faces(frame, known_face_encodings, known_face_names):
    auditoria_id = None

    if not known_face_encodings:
        adapted_frame = adapt_frame(frame)
        face_locations = face_recognition.face_locations(adapted_frame)
        if face_locations:
            foto_bytes = capturar_foto(frame)
            auditoria_id = salvar_auditoria(foto_bytes, status='desconhecido')
            return ["Desconhecido"], draw_identifier(frame, face_locations, ["Desconhecido"]), auditoria_id
        return ["Nenhum rosto visível"], draw_identifier(frame, [], []), None

    adapted_frame = adapt_frame(frame)
    face_locations = face_recognition.face_locations(adapted_frame)
    face_encodings = face_recognition.face_encodings(adapted_frame, face_locations)
    face_names = []

    for face_encoding in face_encodings:
        name = get_match_name(known_face_encodings, known_face_names, face_encoding)
        if name == UNKNOWN_NAME:
            foto_bytes = capturar_foto(frame)
            auditoria_id = salvar_auditoria(foto_bytes, status='desconhecido')
        face_names.append(name)

    if not face_locations:
        face_names = ["Nenhum rosto visível"]

    return face_names, draw_identifier(frame, face_locations, face_names), auditoria_id

def adapt_frame(frame):
    small_frame = cv2.resize(
        frame, (0, 0), fx=VERTICAL_REDUCTION, fy=HORIZONTAL_REDUCTION
    )
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    return rgb_small_frame

def get_match_name(known_face_encodings, known_face_names, face_encoding):
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
    name = UNKNOWN_NAME
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
    best_match_index = np.argmin(face_distances)
    if matches[best_match_index]:
        name = known_face_names[best_match_index]
    return name

def draw_identifier(frame, face_locations, face_names):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)
    return frame

def capturar_foto(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()

def create_buffer(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    frame_bytes = buffer.tobytes()
    frame_b64 = base64.b64encode(frame_bytes).decode("utf-8")
    return frame_b64