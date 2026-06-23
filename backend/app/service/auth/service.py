import hashlib
from uuid import UUID
from datetime import datetime, timedelta, timezone
from typing import Tuple
from app.interfaces.auth import AuthServiceInterface
from app.models.user import User
from app.repository.user.repository import UserRepositoryInterface
from app.repository.refresh_token.repository import UserRefreshTokenRepositoryInterface
from app.utils.auth import (
    verify_password,
    create_access_token,
    generate_refresh_token,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from app.utils.exceptions import UnauthorizedException

class AuthService(AuthServiceInterface):
    def __init__(
        self,
        user_repo: UserRepositoryInterface,
        token_repo: UserRefreshTokenRepositoryInterface
    ):
        self.user_repo = user_repo
        self.token_repo = token_repo

    def _hash_token(self, token: str) -> str:
        """Utility method to hash a token string using SHA-256."""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def authenticate_user(self, email: str, password: str) -> User:
        user = self.user_repo.get_by_email(email)
        if not user or not user.is_active:
            raise UnauthorizedException("Invalid email or password.")
        
        if not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password.")
            
        return user

    def create_session(self, user: User) -> Tuple[str, str, str]:
        # Create Access Token (stateless JWT containing role & sub claims)
        access_token_data = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role
        }
        access_token = create_access_token(data=access_token_data)

        # Create Refresh Token (secure random string)
        refresh_token = generate_refresh_token()
        token_hash = self._hash_token(refresh_token)
        expires_at = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)

        # Store in database
        self.token_repo.create(
            user_id=user.id,
            token_hash=token_hash,
            expires_at=expires_at
        )

        return access_token, refresh_token, user.role

    def refresh_session(self, refresh_token: str) -> Tuple[str, str, str]:
        token_hash = self._hash_token(refresh_token)
        token_record = self.token_repo.get_by_hash(token_hash)
        
        # Verify exists
        if not token_record:
            raise UnauthorizedException("Invalid refresh token.")
            
        # Verify not expired
        # Ensure token_record.expires_at is timezone-aware
        expires_at = token_record.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if datetime.now(timezone.utc) > expires_at:
            self.token_repo.delete_by_hash(token_hash)
            raise UnauthorizedException("Expired refresh token.")

        # Get User
        user = self.user_repo.get_by_id(token_record.user_id)
        if not user or not user.is_active:
            self.token_repo.delete_by_hash(token_hash)
            raise UnauthorizedException("User session is inactive.")

        # Delete the old refresh token (rotation)
        self.token_repo.delete_by_hash(token_hash)

        # Create new session (new Access & new Refresh token & role)
        return self.create_session(user)


    def revoke_session(self, refresh_token: str) -> None:
        token_hash = self._hash_token(refresh_token)
        self.token_repo.delete_by_hash(token_hash)
