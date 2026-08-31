import cv2
import face_recognition
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import numpy as np
import base64

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
def home():
    return HTMLResponse(open("app/static/index.html").read())


@app.websocket("/ws")
async def websocket(websocket: WebSocket):
    await websocket.accept()

    video_capture = cv2.VideoCapture(0)

    # Carrega as imagens conhecidas
    me_image = face_recognition.load_image_file("../images/me.jpg")
    carlinhos_image = face_recognition.load_image_file("../images/carlinhos.png")

    known_face_encodings = [
        face_recognition.face_encodings(me_image)[0],
        face_recognition.face_encodings(carlinhos_image)[0], 
    ]
    known_face_names = ["Beckman", "Carlinhos"]

    process_this_frame = True

    try:
        while True:
            ret, frame = video_capture.read()
            if not ret:
                await asyncio.sleep(0.1)
                continue

            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations
                )

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding
                    )
                    name = "Unknown" 
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding
                    )
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)

                for (top, right, bottom, left), name in zip(face_locations, face_names):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                    cv2.rectangle(
                        frame,
                        (left, bottom - 35),
                        (right, bottom),
                        (0, 0, 255),
                        cv2.FILLED,
                    )
                    cv2.putText(
                        frame,
                        name,
                        (left + 6, bottom - 6),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1.0,
                        (255, 255, 255),
                        1,
                    ) 

                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()  # 🔹 converte ndarray para bytes
                frame_b64 = base64.b64encode(frame_bytes).decode("utf-8")

                await websocket.send_json({"frame": frame_b64, "names": face_names})

            process_this_frame = not process_this_frame
            await asyncio.sleep(0.05)

    except Exception as e:
        print("WebSocket closed:", e)
    finally:
        video_capture.release()
