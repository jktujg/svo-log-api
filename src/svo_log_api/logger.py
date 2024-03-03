import logging
import logging.handlers
import atexit
import json
from queue import Queue
from pathlib import Path
from datetime import (
    datetime as dt,
    timezone as tz,
)


LOG_RECORD_BUILTIN_ATTRS = {
    'args',
    'asctime',
    'created',
    'exc_info',
    'filename',
    'funcName',
    'levelname',
    'levelno',
    'lineno',
    'message',
    'module',
    'msg',
    'name',
    'pathname',
    'process',
    'processName',
    'relativeCreated',
    'stack_info',
    'thread',
    'threadName',
    'taskName',
    'exc_text',
    'msecs',
}


class CustomQueueHandler(logging.handlers.QueueHandler):
    def __init__(self,respect_handler_level: bool = False, **kw):
        self._queue = Queue(maxsize=-1)
        super().__init__(self._queue)
        self.listener = logging.handlers.QueueListener(self._queue, *kw.values(), respect_handler_level=respect_handler_level)
        self.listener.start()
        atexit.register(self.listener.stop)

    def prepare(self, record):
        return record


class JSONFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str]):
        super().__init__()
        self.fmt_keys = fmt_keys or {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._prepare_message(record)
        self._add_extras(record, message)
        return json.dumps(message, default=str)

    def _prepare_message(self, record: logging.LogRecord) -> dict:
        always_fields = dict(
            message=record.getMessage(),
            timestamp=dt.fromtimestamp(record.created, tz=tz.utc).isoformat()
        )
        if record.exc_info is not None:
            always_fields['exc_info'] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            always_fields['stack_info'] = self.formatStack(record.stack_info)

        message = {key: getattr(record, val, None) for key, val in self.fmt_keys.items()}
        message.update(always_fields)

        return message

    def _add_extras(self, record: logging.LogRecord, message: dict) -> None:
        for key, val in vars(record).items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                message[key] = val


log_config = json.load(open(Path(__file__).parent / 'log_config.json', 'r'))
