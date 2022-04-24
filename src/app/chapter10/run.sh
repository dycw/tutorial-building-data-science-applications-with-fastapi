#!/usr/bin/env bash

docker run \
	-p 8000:80 \
	-e ENVIRONMENT=production \
	-e DATABASE_URL=sqlite://./app.db \
	fastapi-app
