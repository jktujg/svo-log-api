import json
import logging
import os
from logging.config import dictConfig
from pathlib import Path

from ..config import settings


def create_dir(config: dict):
    dirs = set()
    for h_name, h_values in config.get('handlers', {}).items():
        if file_path := h_values.get('filename'):
            dirs.add(Path(file_path).parent)

    for log_dir in dirs:
        if not log_dir.exists():
            os.mkdir(log_dir)


with open(Path(__file__).parent / 'log_config.json') as file:
    config = json.load(file)
    create_dir(config)
    dictConfig(config)


main_logger = logging.getLogger('svolog')
access_logger = logging.getLogger('svolog.access')
default_logger = logging.getLogger('svolog.default')

for logger in (main_logger, access_logger):
    logger.setLevel(settings.LOG_LEVEL)
