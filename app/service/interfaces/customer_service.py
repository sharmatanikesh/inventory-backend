from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.models.customer import Customer

class CustomerServiceInterface(ABC):
    @abstractmethod
    def get_customer(self, customer_id: UUID) -> Optional[Customer]:
        """Fetch a single customer."""
        pass

    @abstractmethod
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Fetch a single customer by email."""
        pass

    @abstractmethod
    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        """Fetch all customers."""
        pass

    @abstractmethod
    def register_customer(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        """Register a new customer."""
        pass
