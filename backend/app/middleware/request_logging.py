import logging
from time import perf_counter
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import (
    BaseHTTPMiddleware,
)
from starlette.responses import Response

from app.core.request_context import (
    request_id_context,
)


logger = logging.getLogger(
    "NeuroTwin.Request"
)


class RequestLoggingMiddleware(
    BaseHTTPMiddleware
):
    """
    Assign request IDs, measure API
    execution time, and log request
    performance information.
    """

    SLOW_REQUEST_THRESHOLD_MS = (
        1000.0
    )

    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        """
        Trace and measure one complete
        HTTP request-response lifecycle.
        """

        request_id = (
            request.headers.get(
                "X-Request-ID"
            )
            or str(
                uuid4()
            )
        )

        context_token = (
            request_id_context.set(
                request_id
            )
        )

        start_time = (
            perf_counter()
        )

        logger.info(
            "Request started | "
            "request_id=%s | "
            "method=%s | "
            "path=%s",
            request_id,
            request.method,
            request.url.path,
        )

        try:

            response = await call_next(
                request
            )

            duration_ms = (
                (
                    perf_counter()
                    - start_time
                )
                * 1000
            )

            response.headers[
                "X-Request-ID"
            ] = request_id

            response.headers[
                "X-Process-Time-MS"
            ] = (
                f"{duration_ms:.2f}"
            )

            if (
                duration_ms
                >= (
                    self
                    .SLOW_REQUEST_THRESHOLD_MS
                )
            ):

                logger.warning(
                    "Slow request detected | "
                    "request_id=%s | "
                    "method=%s | "
                    "path=%s | "
                    "status_code=%s | "
                    "duration_ms=%.2f | "
                    "threshold_ms=%.2f",
                    request_id,
                    request.method,
                    request.url.path,
                    response.status_code,
                    duration_ms,
                    (
                        self
                        .SLOW_REQUEST_THRESHOLD_MS
                    ),
                )

            else:

                logger.info(
                    "Request completed | "
                    "request_id=%s | "
                    "method=%s | "
                    "path=%s | "
                    "status_code=%s | "
                    "duration_ms=%.2f",
                    request_id,
                    request.method,
                    request.url.path,
                    response.status_code,
                    duration_ms,
                )

            return response

        except Exception:

            duration_ms = (
                (
                    perf_counter()
                    - start_time
                )
                * 1000
            )

            logger.exception(
                "Request failed | "
                "request_id=%s | "
                "method=%s | "
                "path=%s | "
                "duration_ms=%.2f",
                request_id,
                request.method,
                request.url.path,
                duration_ms,
            )

            raise

        finally:

            request_id_context.reset(
                context_token
            )