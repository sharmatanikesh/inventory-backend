from abc import ABC, abstractmethod
from uuid import UUID
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Retrieve a user by their ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email address."""
        pass

    @abstractmethod
    def create(self, email: str, password_hash: str, role: str) -> User:
        """Create and persist a new user."""
        pass


class SQLAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        return self.db.query(User).filter(
            User.id == user_id,
            User.deleted_at.is_(None)
        ).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(
            User.email == email,
            User.deleted_at.is_(None)
        ).first()

    def create(self, email: str, password_hash: str, role: str) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            role=role,
            is_active=True
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
