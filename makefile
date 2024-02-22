run_dev:
	uvicorn src.svo_log_api.main_dev:app --reload --port 8091

run_prod:
	uvicorn src.svo_log_api.main:app --port 8092

test:
	python -m unittest