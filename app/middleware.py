import time
from .logger import access_logger, default_logger

from fastapi import Request, Response


async def log_requests(request: Request, call_next):
    start_time = time.perf_counter_ns()
    try:
        response: Response = await call_next(request)
        access_logger.info(msg='Success request',
                         extra={
                             'status_code': response.status_code,
                             'client_host': request.client.host if request.client is not None else None,
                             'client_port': request.client.port if request.client is not None else None,
                             'method': request.method,
                             'query_path': request.url.path,
                             'query_params': request.query_params,
                             'path_params': request.path_params,
                             'headers': request.headers,
                             'response_ns': f'{time.perf_counter_ns() - start_time}',
                         })
        return response
    except Exception as e:
        default_logger.error(msg=f'Exception `{e.__class__.__name__}` in ASGI application', exc_info=True)
        raise
