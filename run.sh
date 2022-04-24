#!/usr/bin/env bash

# cd src/app/chapter13 || exit
# uvicorn --reload app.app:app
gunicorn \
	-w 4 \
	-k uvicorn.workers.UvicornWorker \
	--reload \
	app.chapter13.prediction_endpoint.app:app
