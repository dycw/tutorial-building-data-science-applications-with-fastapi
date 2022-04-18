#!/usr/bin/env bash

uvicorn \
	--app-dir src \
	--reload app.chapter3.project.app:app
