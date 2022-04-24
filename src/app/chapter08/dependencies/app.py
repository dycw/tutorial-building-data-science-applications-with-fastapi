from fastapi import Cookie
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi import status
from fastapi.websockets import WebSocketDisconnect


API_TOKEN = "SECRET_API_TOKEN"  # noqa: S105

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str = "Anonymous",
    token: str | None = Cookie(None),
) -> None:
    if token != API_TOKEN:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await websocket.accept()
    await websocket.send_text(f"Hello, {username}!")
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        await websocket.close()
