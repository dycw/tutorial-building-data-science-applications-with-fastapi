from typing import Any

from fastapi import Body
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status


app = FastAPI()


@app.post("/password-1")
async def check_password_1(
    password: str = Body(...), password_confirm: str = Body(...)
) -> dict[str, Any]:
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, detail="Passwords don't match."
        )
    return {"message": "Passwords match."}


@app.post("/password-2")
async def check_password_2(
    password: str = Body(...), password_confirm: str = Body(...)
) -> dict[str, Any]:
    if password != password_confirm:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail={
                "message": "Passwords don't match.",
                "hints": ["Check the caps lock on your keyboard."],
            },
        )
    return {"message": "Passwords match."}
