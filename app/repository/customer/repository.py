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
        """Retrieve all active customers with pagination."""
        pass

    @abstractmethod
    def create(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        """Create and persist a new customer."""
        pass

    @abstractmethod
    def delete(self, customer_id: UUID) -> None:
        """Soft-delete a customer."""
        pass

    @abstractmethod
    def count_active(self) -> int:
        """Count total active customers."""
        pass


from sqlalchemy import func

class SQLAlchemyCustomerRepository(CustomerRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, customer_id: UUID) -> Optional[Customer]:
        return self.db.query(Customer).filter(
            Customer.id == customer_id,
            Customer.deleted_at.is_(None)
        ).first()

    def get_by_email(self, email: str) -> Optional[Customer]:
        return self.db.query(Customer).filter(
            Customer.email == email,
            Customer.deleted_at.is_(None)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.db.query(Customer).filter(
            Customer.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def create(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer_id: UUID) -> None:
        customer = self.get_by_id(customer_id)
        if customer:
            customer.deleted_at = func.now()
            self.db.commit()

    def count_active(self) -> int:
        return self.db.query(Customer).filter(
            Customer.deleted_at.is_(None)
        ).count()
