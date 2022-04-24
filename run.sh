#!/usr/bin/env bash

cd src/app/chapter10 || exit
# uvicorn --reload app.app:app
gunicorn -w 4 -k uvicorn.workers.UvicornWorker --reload app.app:app
