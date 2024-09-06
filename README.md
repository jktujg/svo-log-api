# International Airport Sheremetyevo (SVO) schedule API unofficial wrapper 
The API of the official [website](https://www.svo.aero/) provides access only to the current, past, and next days actual schedule (at least in open access), as well as information about the seasonal schedule (not yet implemented in the current API)

This wrapper, implemented using FastAPI, allows to save the history of changes and provides endpoints to access schedule entities with additional filtering parameters

For example, to get a list of airports with flights operated by Aeroflot (SU) to the Asian region between May 5, 2024, and May 7, 2024, inclusive:
```shell
curl 'https://svolog.ru/api/v1/airports/?order_by=name&page=0&limit=100&region=europe&date_start=2024-05-05%2000%3A00%3A00z&date_end=2024-05-08%2000%3A00%3A00z&company=SU&direction=departure'
```
To select flights to the obtained destinations:
```shell
curl 'https://svolog.ru/api/v1/flights/?order_type=asc&page=0&limit=100&date_start=2024-05-05%2000%3A00%3A00z&date_end=2024-05-08%2000%3A00%3A00z&direction=departure&company=SU&destination=MSQ%2CEVN'
```
To get data on a specific flight with a history of changes:
```shell
curl 'https://svolog.ru/api/v1/flights/24721?changelog=true'
```
For more details, see the  [OpenAPI](https://svolog.ru/api/v1/docs) and [Redoc](https://svolog.ru/api/v1/redoc) specifications

This API is used by the Telegram bot [@svologbot](https://t.me/svologbot) [GitHub](https://github.com/jktujg/svo-sked-bot)

## Stack
- Python3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL (psycopg3)
- Alembic
- Uvicorn / Gunicorn

## Requirements
- [Docker](https://www.docker.com/)
- Content population is carried out by a bot based on the [SDK](https://github.com/jktujg/aero-svo-api) **(not included in the project)**

## Local Development
- Replace the `changethis` values in the `./.env` file
- Start the stack with Docker Compose:
```shell
docker compose up -d
```
The default `docker-compose.override.yml` configured for local development to run a restartable Uvicorn server when local files are changed

To add flight data, a user with access rights to PUT methods will be created during startup

By default, access to the OpenAPI specification is available at http://127.0.0.1:8000/api/v1/docs and Redoc specification is available at http://127.0.0.1:8000/api/v1/redoc

To run on the Gunicorn WSGI server without restarting on local file changes, exclude the configuration in `docker-compose.override.yml`:
```shell
docker compose --file docker-compose.yml up -d
```

### Testing
To run tests in a container, use the script:
```shell
./scripts/tests-start.sh --cov=app/
```
Tests will be run using Pytest with the provided parameters passed through

To modify and add tests, use the `./tests directory`.
### Test running stack
To run tests on the running stack, use the script:
```shell
docker exec svolog-api ./scripts/tests-running.sh --cov=app/
```
Provided parameters will be passed to Pytest as well