from abc import ABC, abstractmethod
from uuid import UUID
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.models.refresh_token import UserRefreshToken

class UserRefreshTokenRepositoryInterface(ABC):
    @abstractmethod
    def create(self, user_id: UUID, token_hash: str, expires_at: datetime) -> UserRefreshToken:
        """Create and persist a new user refresh token hash."""
        pass

    @abstractmethod
    def get_by_hash(self, token_hash: str) -> Optional[UserRefreshToken]:
        """Retrieve refresh token record by its token hash."""
        pass

    @abstractmethod
    def delete_by_hash(self, token_hash: str) -> None:
        """Delete refresh token record by its hash."""
        pass

    @abstractmethod
    def delete_all_for_user(self, user_id: UUID) -> None:
        """Delete all active refresh tokens for a user (force logout)."""
        pass


class SQLAlchemyUserRefreshTokenRepository(UserRefreshTokenRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: UUID, token_hash: str, expires_at: datetime) -> UserRefreshToken:
        refresh_token = UserRefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_by_hash(self, token_hash: str) -> Optional[UserRefreshToken]:
        return self.db.query(UserRefreshToken).filter(
            UserRefreshToken.token_hash == token_hash
        ).first()

    def delete_by_hash(self, token_hash: str) -> None:
        token_record = self.get_by_hash(token_hash)
        if token_record:
            self.db.delete(token_record)
            self.db.commit()

    def delete_all_for_user(self, user_id: UUID) -> None:
        self.db.query(UserRefreshToken).filter(
            UserRefreshToken.user_id == user_id
        ).delete()
        self.db.commit()
