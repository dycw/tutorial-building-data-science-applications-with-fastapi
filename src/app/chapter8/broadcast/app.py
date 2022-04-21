from asyncio import FIRST_COMPLETED
from asyncio import create_task
from asyncio import wait

from broadcaster import Broadcast
from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect
from pydantic import BaseModel


app = FastAPI()
broadcast = Broadcast("redis://localhost:6379")
CHANNEL = "CHAT"


class MessageEvent(BaseModel):
    username: str
    message: str


async def receive_message(websocket: WebSocket, username: str) -> None:
    async with broadcast.subscribe(channel=CHANNEL) as subscriber:
        async for event in subscriber:
            message_event = MessageEvent.parse_raw(event.message)
            # Discard user's own messages
            if message_event.username != username:
                await websocket.send_json(message_event.dict())


async def send_message(websocket: WebSocket, username: str) -> None:
    data = await websocket.receive_text()
    event = MessageEvent(username=username, message=data)
    await broadcast.publish(channel=CHANNEL, message=event.json())


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, username: str = "Anonymous"
) -> None:
    await websocket.accept()
    try:
        while True:
            receive_message_task = create_task(
                receive_message(websocket, username)
            )
            send_message_task = create_task(send_message(websocket, username))
            done, pending = await wait(
                {receive_message_task, send_message_task},
                return_when=FIRST_COMPLETED,
            )
            for task in pending:
                _ = task.cancel()
            for task in done:
                _ = task.result()
    except WebSocketDisconnect:
        await websocket.close()


@app.on_event("startup")  # type: ignore
async def startup() -> None:
    await broadcast.connect()


@app.on_event("shutdown")  # type: ignore
async def shutdown() -> None:
    await broadcast.disconnect()
