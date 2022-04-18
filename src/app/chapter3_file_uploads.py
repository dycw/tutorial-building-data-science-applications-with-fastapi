from typing import Any

from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile


app = FastAPI()


@app.post("/files-1")
async def upload_file_1(file: bytes = File(...)) -> dict[str, Any]:
    return {"file_size": len(file)}


@app.post("/files-2")
async def upload_file_2(file: UploadFile = File(...)) -> dict[str, Any]:
    return {"file_name": file.filename, "content_type": file.content_type}


@app.post("/files-3")
async def upload_file_3(files: list[UploadFile] = File(...)) -> list[dict[str, Any]]:
    return [
        {"file_name": file.filename, "content_type": file.content_type}
        for file in files
    ]
