from fastapi import status, Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    """Base exception class for application-specific errors."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message: str = "An unexpected error occurred."
    default_error_code: str = "INTERNAL_SERVER_ERROR"

    def __init__(self, message: str = None, error_code: str = None):
        self.message = message or self.default_message
        self.error_code = error_code or self.default_error_code
        super().__init__(self.message)


# Standard HTTP exceptions
class NotFoundException(AppException):
    status_code: int = status.HTTP_404_NOT_FOUND
    default_message: str = "Resource not found."
    default_error_code: str = "NOT_FOUND"


class BadRequestException(AppException):
    status_code: int = status.HTTP_400_BAD_REQUEST
    default_message: str = "Bad request."
    default_error_code: str = "BAD_REQUEST"


class UnauthorizedException(AppException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    default_message: str = "Unauthorized."
    default_error_code: str = "UNAUTHORIZED"


class ForbiddenException(AppException):
    status_code: int = status.HTTP_403_FORBIDDEN
    default_message: str = "Forbidden."
    default_error_code: str = "FORBIDDEN"


class ConflictException(AppException):
    status_code: int = status.HTTP_409_CONFLICT
    default_message: str = "Resource conflict."
    default_error_code: str = "CONFLICT"


class UnprocessableEntityException(AppException):
    status_code: int = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_message: str = "Unprocessable entity."
    default_error_code: str = "UNPROCESSABLE_ENTITY"


# Specific Domain Exceptions
class CustomerNotFoundException(NotFoundException):
    default_message: str = "Customer not found."
    default_error_code: str = "CUSTOMER_NOT_FOUND"


class ProductNotFoundException(NotFoundException):
    default_message: str = "Product not found."
    default_error_code: str = "PRODUCT_NOT_FOUND"


class OrderNotFoundException(NotFoundException):
    default_message: str = "Order not found."
    default_error_code: str = "ORDER_NOT_FOUND"


class InsufficientStockException(BadRequestException):
    default_message: str = "Insufficient product stock."
    default_error_code: str = "INSUFFICIENT_STOCK"


import structlog

logger = structlog.get_logger()

# Global handler for FastAPI
async def app_exception_handler(request: Request, exc: AppException):
    # Log 5xx errors as ERROR, and 4xx errors as WARNING
    log_func = logger.error if exc.status_code >= 500 else logger.warning
    log_func(
        "Application exception raised",
        status_code=exc.status_code,
        error_code=exc.error_code,
        message=exc.message,
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code
        }
    )
