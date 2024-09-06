FROM python:3.11-alpine

WORKDIR /svo-log-api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x compose_cmd.sh compose_cmd.override.sh

CMD gunicorn app.main:app --workers ${WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:${SERVE_PORT}