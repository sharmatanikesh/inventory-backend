from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        """Retrieve a customer by their ID."""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Customer]:
        """Retrieve a customer by email address."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Retrieve all customers with pagination."""
        pass

    @abstractmethod
    def create(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        """Create and persist a new customer."""
        pass


class SQLAlchemyCustomerRepository(CustomerRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_by_email(self, email: str) -> Optional[Customer]:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        # Implementation skeleton - actual db query code excluded
        pass

    def create(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        # Implementation skeleton - actual db query code excluded
        pass
