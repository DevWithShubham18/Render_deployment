import logging
import sys
import time
import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from utils.config import settings


def log_setup():

    is_prod = settings.ENV == "prod"

    renderer = (
        structlog.processors.JSONRenderer()
        if is_prod
        else structlog.dev.ConsoleRenderer(colors=True)
    )
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S"),
            structlog.processors.add_log_level,
            renderer,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        structlog.contextvars.clear_contextvars()

        request_id = str(uuid.uuid4())

        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method,
        )

        start = time.time()

        try:
            response = await call_next(request)
            duration = time.time() - start

            structlog.get_logger("request").info(
                "request_completed",
                status_code=response.status_code,
                duration_ms=round(duration * 1000, 2),
            )

            return response

        except Exception:
            structlog.get_logger("request").exception("request_failed")
            raise
