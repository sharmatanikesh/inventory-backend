from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    """Standardized envelope response wrapper for all API success responses."""
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None

    @classmethod
    def ok(cls, data: T = None, message: str = "Operation completed successfully") -> "APIResponse[T]":
        """Helper to create a successful API response."""
        return cls(success=True, message=message, data=data)

    @classmethod
    def fail(cls, message: str) -> "APIResponse[None]":
        """Helper to create a failed API response wrapper."""
        return cls(success=False, message=message, data=None)
