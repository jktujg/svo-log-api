#!/bin/sh

alembic upgrade head
python -m scripts.create_admin --email ${UPLOAD_LOGIN} --password ${UPLOAD_PASSWORD}
gunicorn app.main:app --workers ${WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:${SERVE_PORT}