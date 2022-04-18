from pathlib import Path

from fastapi import FastAPI
from fastapi import status
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import Response


app = FastAPI()


@app.get("/html", response_class=HTMLResponse)
async def get_html() -> str:
    return """
        <html>
            <head>
                <title>Hello world!</title>
            </head>
            <body>
                <h1>Hello world!</h1>
            </body>
        </html>
    """


@app.get("/text", response_class=PlainTextResponse)
async def get_text() -> str:
    return "Hello world!"


@app.get("/redirect-1")
async def redirect_1() -> RedirectResponse:
    return RedirectResponse("/new-url")


@app.get("/redirect-2")
async def redirect_2() -> RedirectResponse:
    return RedirectResponse(
        "/new-url", status_code=status.HTTP_301_MOVED_PERMANENTLY
    )


@app.get("/cat")
async def get_cat() -> FileResponse:
    path = (
        Path(__file__)
        .resolve()
        .parent.parent.parent.joinpath("assets", "cat.jpg")
    )
    return FileResponse(path)


@app.get("/xml")
async def get_xml() -> Response:
    content = """<?xml version="1.0" encoding="UTF-8"?>
        <Hello>World</Hello>
    """
    return Response(content=content, media_type="application/xml")
