import time
import uuid
import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger()

class StructuredLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generate a unique request ID for distributed tracing/observability
        request_id = str(uuid.uuid4())
        
        # Bind the request ID to the task/thread context.
        # Any log calls within this request context will automatically include request_id.
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)
        
        start_time = time.perf_counter()
        
        # Log request receipt
        logger.info(
            "Incoming request",
            method=request.method,
            path=request.url.path,
            client_host=request.client.host if request.client else None,
            query_params=str(request.query_params) if request.query_params else None,
        )
        
        try:
            response = await call_next(request)
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            # Log response success status
            logger.info(
                "Request completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
            )
            
            # Return response with tracing headers
            response.headers["X-Request-ID"] = request_id
            return response
            
        except Exception as e:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            
            # Log failure with traceback
            logger.error(
                "Request failed",
                method=request.method,
                path=request.url.path,
                exception=str(e),
                duration_ms=duration_ms,
                exc_info=True
            )
            raise e
