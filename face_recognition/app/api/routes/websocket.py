import cv2
import asyncio
from fastapi import APIRouter, WebSocket
from app.rec import video_rec

router = APIRouter()


@router.websocket("/")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    video_capture = cv2.VideoCapture(0)
    process_this_frame = True
    known_face_names = video_rec.load_face_names()
    known_face_encodings = video_rec.load_face_encodings()
    try:
        while True:
            frame = video_rec.check_frame(video_capture)
            if not frame:
                await asyncio.sleep(0.1)
                continue
            if process_this_frame:
                face_names, frame = video_rec.recognize_faces(
                    frame, known_face_encodings, known_face_names
                )
                frame_b64 = video_rec.create_buffer(frame)
                await websocket.send_json({"frame": frame_b64, "names": face_names})
            process_this_frame = not process_this_frame
            await asyncio.sleep(0.05)
    except Exception as e:
        print("WebSocket closed:", e)
    finally:
        video_capture.release()
