#!/bin/bash

alembic upgrade head
export $(grep -v '^#' .env | xargs)
uvicorn --factory src.main:setup_app --host ${UVICORN_HOST} --port ${UVICORN_PORT} --reload