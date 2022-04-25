from asyncio import Queue
from asyncio import QueueFull
from asyncio import create_task
from contextlib import suppress
from typing import Any

from cv2 import COLOR_BGR2GRAY
from cv2 import CascadeClassifier
from cv2 import cvtColor
from cv2 import data
from cv2 import imdecode
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import WebSocketDisconnect
from numpy import frombuffer
from numpy import uint8
from pydantic import BaseModel


app = FastAPI()
cascade_classifier = CascadeClassifier()


class Faces(BaseModel):
    faces: list[tuple[int, int, int, int]]


async def receive(websocket: WebSocket, queue: Queue[Any]) -> None:
    bytes = await websocket.receive_bytes()
    with suppress(QueueFull):
        queue.put_nowait(bytes)


async def detect(websocket: WebSocket, queue: Queue[Any]) -> None:
    while True:
        bytes = await queue.get()
        data = frombuffer(bytes, dtype=uint8)
        img = imdecode(data, 1)
        gray = cvtColor(img, COLOR_BGR2GRAY)
        faces = cascade_classifier.detectMultiScale(gray)
        if len(faces) > 0:
            faces_output = Faces(faces=faces.tolist())
        else:
            faces_output = Faces(faces=[])
        await websocket.send_json(faces_output.dict())


@app.websocket("/face-detection")
async def face_detection(websocket: WebSocket) -> None:
    await websocket.accept()
    queue = Queue(maxsize=10)
    detect_task = create_task(detect(websocket, queue))
    try:
        while True:
            await receive(websocket, queue)
    except WebSocketDisconnect:
        _ = detect_task.cancel()
        await websocket.close()


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    cascade_classifier.load(
        data.haarcascades + "haarcascade_frontalface_default.xml"
    )
