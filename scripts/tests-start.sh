#!/bin/sh -x

docker compose down -v --remove-orphans
docker compose up --build -d
docker exec svolog-api ./scripts/tests-running.sh "$@"
docker compose down
docker compose down -v --remove-orphans
