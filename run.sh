#!/usr/bin/env bash

# cd src/app/chapter13 || exit
# uvicorn --reload app.app:app
gunicorn \
	-w 4 \
	-k uvicorn.workers.UvicornWorker \
	--reload \
	src.app.chapter13.async_not_async:app
