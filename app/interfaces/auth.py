from abc import ABC, abstractmethod
from uuid import UUID
from typing import Tuple
from app.models.user import User

class AuthServiceInterface(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate a user using their email and password."""
        pass

    @abstractmethod
    def create_session(self, user: User) -> Tuple[str, str, str]:
        """Create a new session (Access Token, Refresh Token, Role) for a user."""
        pass

    @abstractmethod
    def refresh_session(self, refresh_token: str) -> Tuple[str, str, str]:
        """Verify an existing refresh token, delete it, and issue new tokens with user role."""
        pass


    @abstractmethod
    def revoke_session(self, refresh_token: str) -> None:
        """Revoke a refresh token (logout)."""
        pass
