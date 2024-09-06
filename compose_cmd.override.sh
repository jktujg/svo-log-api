#!/bin/sh

alembic upgrade head
python -m scripts.create_admin --email ${UPLOAD_LOGIN} --password ${UPLOAD_PASSWORD}
uvicorn --host 0.0.0.0 --port ${SERVE_PORT} --reload app.main:app
