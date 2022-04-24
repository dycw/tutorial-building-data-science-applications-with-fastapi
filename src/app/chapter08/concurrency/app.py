from asyncio import FIRST_COMPLETED
from asyncio import create_task
from asyncio import sleep
from asyncio import wait
from datetime import datetime

from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.websockets import WebSocketDisconnect


app = FastAPI()


async def echo_message(websocket: WebSocket) -> None:
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")


async def send_time(websocket: WebSocket) -> None:
    _ = await sleep(10)
    await websocket.send_text(f"It is: {datetime.utcnow().isoformat()}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            echo_message_task = create_task(echo_message(websocket))
            send_time_task = create_task(send_time(websocket))
            done, pending = await wait(
                {echo_message_task, send_time_task}, return_when=FIRST_COMPLETED
            )
            for task in pending:
                _ = task.cancel()
            for task in done:
                task.result()
    except WebSocketDisconnect:
        await websocket.close()
