FROM python:3.11-alpine

WORKDIR /svo-log-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn src.svo_log_api.main_dev:app --workers ${WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:${SERVE_PORT}