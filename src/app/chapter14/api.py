from cv2 import COLOR_BGR2GRAY
from cv2 import IMREAD_UNCHANGED
from cv2 import CascadeClassifier
from cv2 import cvtColor
from cv2 import data
from cv2 import imdecode
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile
from numpy import fromfile
from numpy import uint8
from pydantic import BaseModel


app = FastAPI()
cascade_classifier = CascadeClassifier()


class Faces(BaseModel):
    faces: list[tuple[int, int, int, int]]


@app.post("/face-detection", response_model=Faces)
async def face_detection(image: UploadFile = File(...)) -> Faces:
    data = fromfile(image.file, dtype=uint8)
    image = imdecode(data, IMREAD_UNCHANGED)
    gray = cvtColor(image, COLOR_BGR2GRAY)
    faces = cascade_classifier.detectMultiScale(gray)
    if len(faces) > 0:
        faces_output = Faces(faces=faces.tolist())
    else:
        faces_output = Faces(faces=[])
    return faces_output


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    cascade_classifier.load(
        data.haarcascades + "haarcascade_frontalface_default.xml"
    )
