run_dev:
	python -m src.svo_log_api.main_dev

run_prod:
	python -m src.svo_log_api.main

restart_db:
	python restart_database.py

test:
	python -m unittest