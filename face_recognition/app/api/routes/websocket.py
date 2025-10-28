from typing import final
import cv2
import asyncio
from fastapi import APIRouter, WebSocket
from app.rec import video_rec
router = APIRouter()


@router.websocket("/")
async def websocket(websocket: WebSocket):
    await websocket.accept()
    video_capture = cv2.VideoCapture(0)
    process_this_frame =True
    known_face_names = video_rec.load_face_names()
    known_face_encodings = video_rec.load_face_encodings()
    try:
        while True:
            frame = video_rec.check_frame(video_capture)
            if not frame:
                await asyncio.sleep(0.1)
                continue
            if process_this_frame:
                frame = video_rec.recognize_faces(frame, known_face_encodings, known_face_names)
            


    except Exception as e:
        print("WebSocket closed:",e)
    finally:
        video_capture.release()

def create_buffer(frame):

